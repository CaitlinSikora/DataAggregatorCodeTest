from googleapiclient.discovery import build
from app import app
from nltk.sentiment.vader import SentimentIntensityAnalyzer

search_engine_id = app.config['GOOGLE_KEYS']['search_engine_id']
apis = app.config['GOOGLE_KEYS']['apis']

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

def owner_score(owner, location, business_type):
    owner_score = 0.5
    search_term = business_name+' '+location+' '+business_type
    results = try_keys(search_term,apis)

    # get total number of results
    head = results['queries']['request']
    num_hits = head[0]['totalResults']
    print num_hits

    # parse data for news articles and sentiment
    sent_total = 0
    sid = SentimentIntensityAnalyzer()
    count_news = 0
    news_names = {'http://ny.eater.com':0,
                    'http://www.nytimes.':0,
                    'http://www.grubstre':0,
                    'http://www.newyorke':0,
                    'http://observer.com':0,
                    'http://www.villagev':0,
                    'http://www.brownsto':0}
    for item in results['items']:
        # try to count news articles
        if item['link'][:19]in news_names:
            count_news+=1 
        else:
            for element in item['pagemap']:
                if element == "review" or element == "newsarticle" or element == "article":
                    count_news+=1

        # sentiment analysis of snippets
        ss = sid.polarity_scores(item['snippet'])
        listing_sent = ss["compound"]
        sent_total += listing_sent

    ave_sent = sent_total / len(results['items'])

