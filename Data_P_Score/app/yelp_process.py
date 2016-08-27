from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from app import app
import re

def make_id(business_name):
	regex = re.compile('[%s]' % re.escape(string.punctuation))
	return regex.sub('-', business_name.lower())

def search_yelp(business_name,location):
	creds = app.config['YELP_KEY']
	auth = Oauth1Authenticator(**creds)
	client = Client(auth)
	params = {
		'term':business_name,
	    'location':location
	}
	business_id_response = client.search(**params)
	business_id = business_id_response.businesses[0].id
	categories = business_id_response.businesses[0].categories
	zip_code = business_id_response.businesses[0].location.postal_code
	#print business_id, business_id_response.businesses[0].categories
	#print len(business_id_response.businesses)
	#for business in business_id_response.businesses:
		#print business.name
	response = client.get_business(business_id)
	print response.business
	#print response.business.is_claimed, response.business.is_closed, response.business.menu_date_updated
	#print response.business.name, response.business.rating, response.business.review_count
	#print response.business.reviews[0].time_created,response.business.reviews[0].excerpt
	#print response.business.categories
	# peer_response={}
	# for category in categories:
	# 	print category.name
	# 	params = {
	# 		'term':category.name,
	# 	    'location':zip_code
	# 	}
	# 	peer_response[category.name] = client.search(**params)
	# 	print len(peer_response[category.name].businesses)
	# 	ratings_sum = 0
	# 	for listing in peer_response[category.name].businesses:
	# 		ratings_sum += listing.rating
	# 		print category.name, listing.name, listing.rating, listing.review_count, listing.location.postal_code
	# 	print ratings_sum/len(peer_response[category.name].businesses)