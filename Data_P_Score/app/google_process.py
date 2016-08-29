from googleapiclient.discovery import build
from app import app
from nltk.sentiment.vader import SentimentIntensityAnalyzer

search_engine_id = app.config['GOOGLE_KEYS']['search_engine_id']
apis = app.config['GOOGLE_KEYS']['apis']

alerts = ["This business could not be found on Google.",
        "This business owner does not have a positive reputation in this industry.",
        "The yelp ratings appear to be declining for this business."]

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

    own_score = owner_score(owner, business_type)
    final_score = own_score
    return {
                'x': "Google %.2f"% final_score,
                'y': final_score,
                'z': send_alerts
            }

def owner_score(owner, business_type):
    score = 0.5
    search_term = owner+' '+business_type
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

