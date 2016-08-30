from googleapiclient.discovery import build
from app import app
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime
import numpy

search_engine_id = app.config['GOOGLE_KEYS']['search_engine_id']
apis = app.config['GOOGLE_KEYS']['apis']

alerts = ["This business could not be found on Google.",
        "This business owner does not have a long-standing, positive reputation in this industry."]

def google_search(key_term, api, search_engine_id):
    search_term = key_term
    num_requests = 1
    search_engine_id = search_engine_id
    api_key = api
    service = build('customsearch', 'v1', developerKey=api_key)
    collection = service.cse()

    try:
        request = collection.list(q=search_term,
            num=10,
            start=1,
            cx=search_engine_id
        )
        response = request.execute()
        if response:
            return response
    except:
        return None

def try_keys(key_word,apis):
    # This is a hacky solution to the limit of API calls for Google Custom Search.
    # I would never use this for a publicly deployed application, but it was useful for testing/debugging.
    apis = apis
    print "Searched", key_word
    google = None
    for i,key in enumerate(apis):
        if not google:
            print "key", i
            google = google_search(key_word,apis[i], search_engine_id)
    return google

def grab_facebook_alias(business_name,location):
    search_term = business_name+' '+location+' facebook'
    results = try_keys(search_term,apis)
    for item in results['items']:
        if item['link'][:25]=='https://www.facebook.com/':
            alias = item['link'][25:]
            if alias[-1:]=='/':
                alias = alias[:-1]
            print alias
            return alias
    return None

def google_score(business_name,owner,business_type,location):
    send_alerts = ["Google is used to assess the business owner's reputation in the industry and project future yelp ratings."]

    # calculate scores
    try: 
        own_score = owner_score(owner,business_type,business_name)
        proj_score = projection_score(business_name,location)
        scores = [own_score, proj_score[0]]
    except:
        print "not found"
        send_alerts.append(alerts[0])
        return {
                'x': "Google %.2f"% 0.2,
                'y': 0.2,
                'z': send_alerts
            }

    # add customized alerts
    alerts.append("With a projected rating of %.1f in 3 years, this business appears to be declining." % proj_score[1])
    alerts.append("With a projected rating of %.1f in 3 years and a positive owner reputation in the industry, this business appears to be strong." % proj_score[1])

    # calculate average of different scores
    score_total=0
    for i, score in enumerate(scores):
        print score
        score_total += score
        if score < 0.7:
            send_alerts.append(alerts[i+1])
    final_score = score_total * 0.5
    if final_score > 1.0:
        final_score = 1.0
    if len(send_alerts) == 1:
        send_alerts.append(alerts[3])
    print final_score, send_alerts
    return {
                'x': "Google %.2f"% final_score,
                'y': final_score,
                'z': send_alerts
            }

def owner_score(owner, business_type, business_name):
    score = 0.5
    search_term = owner+' '+business_type+' '+business_name
    results = try_keys(search_term,apis)

    # get total number of results and raise score for more results
    head = results['queries']['request']
    num_hits = int(head[0]['totalResults'])
    print num_hits
    score+=(num_hits-20)/500
    print (num_hits-20)/500

    # parse data for news articles and sentiment
    sent_total = 0
    sid = SentimentIntensityAnalyzer()
    count_news = 0
    news_sent = 0
    news_names = {'http://ny.eater.com':0,
                    'http://www.nytimes.':0,
                    'http://www.grubstre':0,
                    'http://www.newyorke':0,
                    'http://observer.com':0,
                    'http://www.villagev':0,
                    'http://www.brownsto':0}
    for item in results['items']:
        news = False
        # try to count news articles
        if item['link'][:19]in news_names:
            news = True
        else:
            for element in item['pagemap']:
                if element == "review" or element == "newsarticle" or element == "article":
                    news=True
                    print element
        if news == True:
            count_news += 1
        print "news counts",count_news

        # sentiment analysis of snippets
        ss = sid.polarity_scores(item['snippet'])
        listing_sent = ss["compound"]
        print item['snippet'],listing_sent
        sent_total += listing_sent
        # keep track of sentiment of news snippets
        if news == True:
            news_sent+=listing_sent

    # calculate average sentiment of snippets and news snippets and adjust score accordingly
    ave_sent = sent_total / len(results['items'])
    ave_news_sent = news_sent/count_news
    score += ave_sent / 5.0
    score += ave_news_sent / 4.0
    score += count_news / 30.0
    
    return score

def projection_score(business_name,location):
    # get current date in unix, we will handle unix timecodes
    current_date = int(datetime.strftime(datetime.now(), '%Y%m%d'))
    # get projection date in 3 years and convert to unix
    proj_date = str(current_date+30000)
    proj_date = int(datetime.strptime(proj_date, '%Y%m%d').strftime("%s"))

    # get search data to look at recent yelp ratings
    search_term = business_name+' '+location
    results = try_keys(search_term,apis)
    dates = []
    ratings_data = []
    for item in results['items']:
        if item['link'][:20]=='https://www.yelp.com':
            reviews = item['pagemap']['review']
            ratings = item['pagemap']['rating']
            for review in reviews:
                if 'datepublished' in review:
                    date = int(datetime.strptime(review['datepublished'], '%Y-%m-%d').strftime("%s"))
                    print date
                    dates.append(date)
            print dates
            for rating in ratings:
                if 'ratingvalue' in rating:
                    ratings_data.append(float(rating['ratingvalue']))
            print ratings_data
    # use numpy to calculate the regression, linear was the most appropriate, though this is obviously ridiclous, especially with only 20 data points
    degree = 1
    coefficients = numpy.polyfit(dates, ratings_data, degree)
    # calculate projected rating in 3 years
    projected_rating = coefficients[0]*proj_date + coefficients[1]
    print projected_rating

    # assign score based on projected rating
    if projected_rating > 5.0:
        projected_rating = 5.0
    score = projected_rating / 5
    return score, projected_rating