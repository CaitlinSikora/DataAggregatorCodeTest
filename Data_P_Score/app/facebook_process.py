import requests, json
from google_process import grab_facebook_alias,try_keys,google_search
from app import app
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import math

APP_ID = app.config['FACEBOOK_KEYS']['APP_ID']
VERSION = app.config['FACEBOOK_KEYS']['VERSION']
APP_SECRET = app.config['FACEBOOK_KEYS']['APP_SECRET']
ACCESS_TOKEN = app.config['FACEBOOK_KEYS']['ACCESS_TOKEN']

alerts = ["This business does not appear to have a page on Facebook.",
		"This business appears to be permanently closed according to Facebook.",
		"The Facebook page for this business is missing vital information."]

def get_facebook(business_name,location):
	# create empty list of alerts to send
	send_alerts = []
	
	# get the facebook alias via a google search
	alias = grab_facebook_alias(business_name,location)
	if not alias:
		print "not found"
		send_alerts.append(alerts[0])
		return 0.3, send_alerts
	
	# set up parameters for the request
	url = 'https://graph.facebook.com/v2.7/'+alias+'?access_token='+ACCESS_TOKEN
	headers = {'content-type': 'application/json; charset=UTF-8','connection':'Keep-Alive'}
	params = {'fields':'id,name,business,can_checkin,category,category_list,checkins,company_overview,contact_address,context,about,attire,awards,affiliation,culinary_team,fan_count,food_styles,founded,general_info,general_manager,hours,is_always_open,is_community_page,is_permanently_closed,is_published,is_unclaimed,is_verified,last_used_time,link,location,new_like_count,offer_eligible,owner_business,parking,payment_options,personal_info,personal_interests,phone,place_type,price_range,restaurant_services,restaurant_specialties,single_line_address,store_location_descriptor,talking_about_count,website,were_here_count,posts'}
	
	# request the data from facebook
	try:
		r = requests.get(url,params=params)
		response = json.loads(r.text)
	except:
		print "not found"
		send_alerts.append(alerts[0])
		return 0.3, send_alerts
	if 'name' not in response or response['location']['city'].lower()!=location.lower():
		print "not found"
		send_alerts.append(alerts[0])
		return 0.3, send_alerts

	# calculate the scores
	checkin_score = checkins_fans(response)
	posting = posting_habits(response)
	scores = [is_open(response),
		verified_info(response),
		checkin_score[0],
		posting[0]]

	# add customized alerts
	alerts.append("With %d checkins, %d fans, and %d people talking about this business, community support is not strong enough." % (checkin_score[1],checkin_score[2],checkin_score[3]))
	alerts.append("With an average of %.1f days between posts and an overall %s %s posting mood, this business does not maintain a postive enough presence on Facebook." % (posting[1],posting[2],posting[3]))
	alerts.append("With %d checkins, %d fans, an average of %.1f days between posts, and %d people talking about it, this business has a strong, positive presence on Facebook." % (checkin_score[1],checkin_score[2],posting[1],checkin_score[3]))

	# calculate average of different scores
	score_total=0
	for i, score in enumerate(scores):
		print score
		score_total += score
		if score < 0.7:
			send_alerts.append(alerts[i+1])
	final_score = score_total * 0.25
	if len(send_alerts) == 0:
		send_alerts.append(alerts[5])
	print final_score, send_alerts
	return final_score, send_alerts

def is_open(response):
	# if business is listed as permanently closed, it has either failed already 
	# or it is likely to fail due to a lack of online information for consumers
	if response['is_permanently_closed']==False:
		return 0.7
	else:
		return 0.3

def verified_info(response):
	score = 0.5
	# if business has been claimed, information is more reliable for consumers
	# and well-managed online presence suggests that the owner cares
	if response['is_unclaimed']==False:
		score+=0.1
	else:
		score-=0.1
	if response['is_verified']==True:
		score+=0.05
	if response['is_published']==True:
		score+=0.05
	# if more information about the business is available, 
	# consumers are more likely to pursue engage with this business
	if 'location' in response and 'phone' in response and 'website' in response:
		score+=0.1
	else:
		score-=0.1
	# more details about the experience encourage more customers
	if 'hours' in response and 'price_range' in response and 'attire' in response:
		score+=0.1
	payment_score = 0
	# more payment options is more convenient
	if 'payment_options' in response:
		for item in response['payment_options']:
			if item!='cash_only':
				payment_score+=response['payment_options'][item]
			else:
				if response['payment_options'][item] == 1:
					score-=0.1
		score+=(0.1*(payment_score/4.0))
	return score

def checkins_fans(response):
	score = 0.5
	# adjust score to be higher for more checkings, fans, and talking about
  	if response['can_checkin']==True:
  		checkins = response['checkins']
  		score+=(checkins-50)/40000.0
  		fans = response['fan_count']
	  	score+=float(fans)/(2*checkins)
	  	talking = response['talking_about_count']
		score+=talking/400.0
	return score, checkins, fans, talking

def posting_habits(response):
	# get current date in unix, we will handle unix timecodes to get accurate differences
	current_date = int(datetime.now().strftime("%s"))

	# setup initial values
	score = 0.5
	prev_date = current_date
	spacing_total = 0
	sent_total = 0
	sid = SentimentIntensityAnalyzer()

	# run through the posts and tally spacing and sentiment
	if 'posts' in response:
		messages_total = len(response['posts']['data'])
		for i, message in enumerate(response['posts']['data']):
			raw_date = message['created_time'].split('+')[0]
			date = int(datetime.strptime(raw_date, '%Y-%m-%dT%H:%M:%S').strftime("%s"))
			spacing = int(prev_date)-int(date)
			spacing_total+=spacing
			if i == 0:
				recent = spacing
			prev_date = date
			if 'message' in message:
				ss = sid.polarity_scores(message['message'])
				post_sent = ss["compound"]
				sent_total += post_sent

	# calculate average post spacing and sentiment
	ave_sent = sent_total / messages_total
	ave_spacing = spacing_total / messages_total / 86400.0 # convert to days from seconds
	print ave_spacing

	# adjust score to be higher for high sentiment and frequent posts
	score += (31-ave_spacing)/(10.0*ave_spacing)
	score += ave_sent / 4.0

	sent_report = str(int(math.floor(ave_sent * 100)))+"%"
	print sent_report
	if sent_report>=0:
		mood = "positive"
	else:
		mood = "negative"
	
	return score, ave_spacing, sent_report, mood