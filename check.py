import pymongo
import requests
import json

import boto3
lambda_client = boto3.client('lambda')

from dotenv import dotenv_values
config = dotenv_values(".env")

db_ip = config['db_ip']
db_port = config['db_port']
db_client = config['db_client']
db_collection = config['db_collection']
username = config['username']
password = config['password']

client = pymongo.MongoClient(f"mongodb://{username}:{password}@{db_ip}:{db_port}/")
db = client[db_client]
wp_attack = db[db_collection]

print (wp_attack.find({'response':{'$ne':None}}).count())
print (wp_attack.count())
exit(0)
available = wp_attack.aggregate([
    {'$project': { '_id': 0,'response':1, 'url':1 } },
    {'$sample': { 'size': 10000 } },
    {'$match': { 'response':None }  },
    {'$sample': { 'size': 100 } }
])
print (available)
all_urls = [x['url'] for x in list(available)]
print (all_urls)

