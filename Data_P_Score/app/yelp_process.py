from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from app import app
import re
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def search_yelp(business_name,location):
	# set up client to do the search
	creds = app.config['YELP_KEYS']
	auth = Oauth1Authenticator(**creds)
	client = Client(auth)
	params = {
		'term':business_name,
	    'location':location
	}
	# search to get the business id for your business
	response = client.search(**params)
	business_id = response.businesses[0].id
	categories = response.businesses[0].categories
	postal_code = response.businesses[0].location.postal_code
	current_date = datetime.strftime(datetime.now(), '%Y%m%d')

	# search for specifics for that business?
	#response = client.get_business(business_id)

	# run score calculator functions
	open_score = is_open(response)
	contact_score = contact_info(response, current_date)
	reviews_ratings_score = reviews_ratings(response, current_date)
	peer_score = peer_to_peer(client, categories,postal_code,rating,review_count)

	# calculate average of different scores
	score_total = open_score + contact_score + reviews_ratings_score + peer_score 
	final_score = score_total * 0.25
	return final_score

def is_open(response):
	if response.business.is_closed==False:
		return 0.8
	else:
		return 0.2

def contact_info(response, current_date):
	score = 0.5
	if response.business.is_claimed==True:
		score+=0.1
	else:
		score-=0.1
	if response.business.name and response.business.phone and response.business.location.address:
		score+=0.1
	else:
		score-=0.1
	if response.business.menu_provider:
		score+=0.1
	if response.business.snippet_text:
		score+=0.1
	menu_update = datetime.strftime(datetime.fromtimestamp(response.business.menu_date_updated), '%Y%m%d')
	if int(current_date)-int(menu_update)<=10000:
		score+=0.1
	return score

def reviews_ratings(response, current_date):
	score = 0.5
	if response.business.rating >= 4.0:
		score+=0.2
	else:
		score-=0.2
	if response.business.review_count >= 50:
		score+=0.1
	review_time = datetime.strftime(datetime.fromtimestamp(response.business.reviews[0].time_created), '%Y%m%d')
	if int(current_date)-int(review_time)<=100:
		score+=0.1
	sid = SentimentIntensityAnalyzer()
	ss = sid.polarity_scores(response.business.reviews[0].excerpt)
	review_sent = 0.1*ss["compound"]
	score += review_sent
	return score

def peer_to_peer(client,categories,postal_code,rating,review_count):
	score = 0.5
	ratings_sum = 0
	review_count_sum = 0
	postal_count = 0
	for category in categories:
		print category.name
		params = {
			'term':category.name,
		    'location':zip_code
		}
		peer_response = client.search(**params)
		for listing in peer_response.businesses:
			if listing.location.postal_code == postal_code:
				ratings_sum += listing.rating
				review_count_sum += listing.review_count
				postal_count += 0
	ave_rating = float(ratings_sum)/postal_count
	ave_reviews = float(review_count_sum)/postal_count
	score += 0.4 * (rating-ave_rating)/4
	return score

# Can you get open_date of business? Is more info available in search api? pricerange? owners? website?




