from googleapiclient.discovery import build
from app import app

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
        print item['link']
        if item['link'][:25]=='https://www.facebook.com/':
            alias = item['link'][25:]
            if alias[-1:]=='/':
                alias = alias[:-1]
            print alias
            return alias
    return None

def grab_wide(results):
    if results == None:
        return None
    parsed = results
    tester = results['queries']['request']
    # print tester
    if tester[0]['totalResults']!='0'and tester[0]['totalResults']>0:
        links = []
        for item in parsed['items']:
            if (item['image']['width']/item['image']['height'])>1.5:
              links.append(item['link'])
        if len(links)==0:
            return grab_widest(results)
        else:
            ind = randint(0,len(links)-1)
            return links[ind]
    else:
        return None