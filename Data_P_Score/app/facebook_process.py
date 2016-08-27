import requests, json
from google_process import grab_facebook_alias,try_keys,google_search

APP_ID = '1743374732605331'
VERSION = 'v2.7'
APP_SECRET = '1e131da888dc7593ca39bf5a9c5647e6'
ACCESS_TOKEN = 'EAAYxlwZBlt5MBAJ2oafH5p9I69DGH4usQVlRxUjazzRZBQCZBZC6kOiwFxko8icNJMw5l6KtF3Dqud25ZBCp5wZCZAj7wmuW9ZBHlz3ExjXksnZAVBHYnKDMU6eZBdvsJWNhVpe39S9TfZCRBSuoEq6RMvKApKxzHho3dEZD'
business_name = grab_facebook_alias("Mayfield",'brooklyn')

#url = 'https://graph.facebook.com/v2.7/'+business_name+'?access_token='+ACCESS_TOKEN+'?fields=id%2Cname%2Cbusiness%2Ccan_checkin%2Ccategory%2Ccategory_list%2Ccheckins%2Ccompany_overview%2Ccontact_address%2Ccontext%2Cabout%2Cattire%2Cawards%2Caffiliation%2Cculinary_team%2Cfan_count%2Cfood_styles%2Cfounded%2Cgeneral_info%2Cgeneral_manager%2Chours%2Cis_always_open%2Cis_community_page%2Cis_permanently_closed%2Cis_published%2Cis_unclaimed%2Cis_verified%2Clast_used_time%2Clink%2Clocation%2Cnew_like_count%2Coffer_eligible%2Cowner_business%2Cparking%2Cpayment_options%2Cpersonal_info%2Cpersonal_interests%2Cphone%2Cplace_type%2Cprice_range%2Crestaurant_services%2Crestaurant_specialties%2Csingle_line_address%2Cstore_location_descriptor%2Ctalking_about_count%2Cwebsite%2Cwere_here_count%2Cposts'
url = 'https://graph.facebook.com/v2.7/'+business_name+'?access_token='+ACCESS_TOKEN
headers = {'content-type': 'application/json; charset=UTF-8','connection':'Keep-Alive'}
params = {'fields':'id,name,business,can_checkin,category,category_list,checkins,company_overview,contact_address,context,about,attire,awards,affiliation,culinary_team,fan_count,food_styles,founded,general_info,general_manager,hours,is_always_open,is_community_page,is_permanently_closed,is_published,is_unclaimed,is_verified,last_used_time,link,location,new_like_count,offer_eligible,owner_business,parking,payment_options,personal_info,personal_interests,phone,place_type,price_range,restaurant_services,restaurant_specialties,single_line_address,store_location_descriptor,talking_about_count,website,were_here_count,posts'}

#params = {'fields':'id,name,business,category,category_list'}

try:
	r = requests.get(url,params=params)
	decoded_data = json.loads(r.text)
#r = requests.get(url)
except:
	decoded_data = None
print decoded_data['name']
if decoded_data['location']['city']=='Brooklyn':
	print decoded_data
else:
	print "wrong"

#graph = facebook.GraphAPI(access_token='EAACEdEose0cBAPniNXbPfUn9WZC8D8z22h9nMRXRXC9QIsFCAAIXQpMZAujnZBN1nEuedb0JLAJlIFdZAMIRDvdz6Fj1xkTc16upVlYmMD8DPygKZCWyxAFpck9shohUcLRQYuh9ZCQOGhQDY2OdqSHsmT87hdTBMGDv0qpiwZBagZDZD', version='2.7')
#r = graph.get_object(name="Mayfield Restaurant", fields=params['fields'])
print decoded_data

# https://graph.facebook.com/oauth/access_token?client_id=1743374732605331&client_secret=1e131da888dc7593ca39bf5a9c5647e6&grant_type=fb_exchange_token&fb_exchange_token=EAAYxlwZBlt5MBANhjPGmsZCkxYW6dxR7FWL3tOCQlgW8shI1k87ZC2PqkwyQD7uxkZCb9JpaznnIOyZCz1wuPyROnosaukZAy0XKtkiuQFoVLY6ruwOWPF7xijyRBNIE34ufu8rZBzbTj6BcjuZCOlf98NcizA3FbhqDCFh3aEfacAZDZD