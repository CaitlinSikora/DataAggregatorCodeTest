from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from app import app
import re
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer

alerts = ["This business does not appear to have a page on Yelp.",
		"This business appears to be permanently closed according to Yelp.",
		"The Yelp page for this business is missing vital information."]

def search_yelp(business_name,location):
	# create empty list of alerts to send
	send_alerts = []
	# set up client to do the search
	creds = app.config['YELP_KEYS']
	auth = Oauth1Authenticator(**creds)
	client = Client(auth)
	params = {
		'term':business_name,
	    'location':location
	}
	# search to get the business id for your business
	try:
		response = client.search(**params)
	except:
		send_alerts.append(alerts[0])
		return 0.3, send_alerts
	mentions = len(response.businesses)
	business_id = response.businesses[0].id
	categories = response.businesses[0].categories
	postal_code = response.businesses[0].location.postal_code
	current_date = datetime.strftime(datetime.now(), '%Y%m%d')
	rating = response.businesses[0].rating
	review_count = response.businesses[0].review_count

	# search for specifics for your business
	response = client.get_business(business_id)

	# run score calculator functions
	peer_score = peer_to_peer(client, categories, postal_code, rating, review_count, mentions)
	scores = [is_open(response), 
				contact_info(response, current_date),
				reviews_ratings(response, current_date),
				peer_score[0]]
	
	# add customized alerts
	alerts.append("The Yelp rating "+str(rating)+" and record of "+str(review_count)+" reviews do not provide a consistent track record of customer satisfaction.")
	alerts.append("With a comparative score of "+str(peer_score[0])+", this business has not performed competitively amongst a group of "+str(peer_score[1])+" nearby similar businesses.")

	# calculate average of different scores
	score_total=0
	for i, score in enumerate(scores):
		print score
		score_total += score
		if score < 0.7:
			send_alerts.append(alerts[i+1])
	final_score = score_total * 0.25
	print final_score, send_alerts
	return final_score, send_alerts

def is_open(response):
	# if business is listed as permanently closed, it has either failed already 
	# or it is likely to fail due to a lack of online information for consumers
	if response.business.is_closed==False:
		return 0.7
	else:
		return 0.3

def contact_info(response, current_date):
	score = 0.5
	# if business has been claimed, information is more reliable for consumers
	# and well-managed online presence suggests that the owner cares
	if response.business.is_claimed==True:
		score+=0.1
	else:
		score-=0.1
	# if more information about the business is available, 
	# consumers are more likely to pursue engage with this business
	if response.business.name and response.business.phone and response.business.location.address:
		score+=0.1
	else:
		score-=0.1
	if response.business.menu_provider:
		score+=0.1
	else:
		score-=0.1
	if response.business.snippet_text:
		score+=0.1
	if response.business.menu_date_updated:
		menu_update = datetime.strftime(datetime.fromtimestamp(response.business.menu_date_updated), '%Y%m%d')
	else:
		menu_update = int(current_date)+20000
	if int(current_date)-int(menu_update)<=10000:
		score+=0.1
	return score

def reviews_ratings(response, current_date):
	score = 0.5
	# business performing above a certain threshold receive higher scores
	if response.business.rating < 3.5:
		score-=0.2
	if response.business.rating >= 4.0:
		score+=0.1
	if response.business.rating >= 4.5:
		score+=0.1
	# more reviews and more recent reviews suggest greater reliability of ratings
	if response.business.review_count >= 50:
		score+=0.1
	review_time = datetime.strftime(datetime.fromtimestamp(response.business.reviews[0].time_created), '%Y%m%d')
	if int(current_date)-int(review_time)<=400:
		score+=0.1
	# tone of most recent review sets consumer's interpretation of information
	sid = SentimentIntensityAnalyzer()
	ss = sid.polarity_scores(response.business.reviews[0].excerpt)
	review_sent = 0.1*ss["compound"]
	score += review_sent
	return score

def peer_to_peer(client,categories,postal_code,rating,review_count, mentions):
	score = 0.5
	ratings_sum = 0
	review_count_sum = 0
	postal_count = 0
	for category in categories:
		print category.name
		params = {
			'term':category.name,
		    'location':postal_code
		}
		peer_response = client.search(**params)
		for listing in peer_response.businesses:
			if listing.location.postal_code == postal_code:
				ratings_sum += listing.rating * listing.review_count
				review_count_sum += listing.review_count
				postal_count += 1
	ave_rating = float(ratings_sum)/review_count_sum
	ave_reviews = float(review_count_sum)/postal_count
	score += 0.2 * (rating-ave_rating)/4
	score += 0.2 * (review_count-ave_reviews)/ave_reviews
	if postal_count < 7:
		score += (7.0 - postal_count) / 28
		print "#competition",(7.0 - postal_count) / 28, postal_count
	if mentions > 0.35*postal_count:
		score += 0.1
	return score, postal_count

# Can you get open_date of business? Is more info available in search api? pricerange? owners? website?




