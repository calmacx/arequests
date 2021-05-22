import pymongo
import requests
import json

import boto3
lambda_client = boto3.client('lambda')

def chunk(l, n):
    for i in range(0, len(l), n): 
        yield l[i:i + n]

from dotenv import dotenv_values
config = dotenv_values(".env")

lambda_arn = config['lambda_arn']
db_ip = config['db_ip']
db_port = config['db_port']
db_client = config['db_client']
db_collection = config['db_collection']
username = config['username']
password = config['password']

client = pymongo.MongoClient(f"mongodb://{username}:{password}@{db_ip}:{db_port}/")
db = client[db_client]
wp_attack = db[db_collection]

for i in range(100):
    print (f"working on {i}/100")
    available = list(
        wp_attack.aggregate([
            {'$match':{'response':None}},
            {'$sample': { 'size': 1000 } }
        ])
    )
    all_urls = [x['url'] for x in available]
    batch_urls = list(chunk(all_urls,10))
    
    for j,urls in enumerate(batch_urls):
        data = json.dumps(dict(config,**{'urls':urls}))
        
        response = lambda_client.invoke(
            FunctionName=,
            InvocationType='Event',
            Payload=data
        )
        print (f"\t {j}/{len(batch_urls)} of length {len(urls)}")
        print (response)
