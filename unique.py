import pymongo
import requests
import json
import time
from dotenv import dotenv_values
import boto3
lambda_client = boto3.client('lambda')

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
#responses = wp_attack.aggregate([
#    {'$project': { '_id': 0,'response':1, 'url':1 } },
#    {'$match': { 'response': {'$ne':None }  }},
#])

bad=0
for obj in list(wp_attack.find({'response': 200},
                               {'_id':0,'url':1,'response':1})):
    if 'innovatie.devolksbank' in obj['url']:
        bad+=1
    else:
        print (obj)

print (bad)
print (wp_attack.find({ 'response': {'$ne':None }}).distinct('response'))

result = wp_attack.aggregate([
    {'$project': { '_id': 0,'response':1, 'url':1 } },
    {'$match': { 'response': {'$ne':None }}},
    {"$group": {"_id": "$response", "count":{"$sum": 1}}}
])
print (result)
print (dir(result))
print (list(result))
                             
                                
