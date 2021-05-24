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

#client = pymongo.MongoClient(f"mongodb://{username}:{password}@{db_ip}:{db_port}/")
client = pymongo.MongoClient(f"mongodb://{username}:{password}@localhost:{db_port}/")
db = client[db_client]
wp_attack = db[db_collection]

n=100
for i in range(n):
    print (f"working on {i}/{n}")
    available = wp_attack.aggregate([
        {'$project': { '_id': 0,'response':1, 'url':1 } },
        {'$sample': { 'size': 1000 } },
        {'$match': { 'response':None }  },
        {'$sample': { 'size': 100 } }
    ])
    all_urls = [x['url'] for x in list(available)]
    print ('got all urls')
    
    batch_urls = list(chunk(all_urls,10))
    print ('start the batch process')
    
    for j,urls in enumerate(batch_urls):
        data = json.dumps(dict(config,**{'urls':urls}))
        response = lambda_client.invoke(
            FunctionName=lambda_arn,
            InvocationType='Event',
            Payload=data
        )
        print (f"\t {j}/{len(batch_urls)} of length {len(urls)}")
        print (response)
        if 'Payload' in response:
            print (response['Payload'].read())
