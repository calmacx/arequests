import pymongo
import requests
import datetime
import json
from urllib.parse import urlparse
from dotenv import dotenv_values
import boto3
s3 = boto3.resource('s3')
bucket = s3.Bucket("exploits-ai1wm")

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

#wp_attack.create_index( [('url',pymongo.ASCENDING )] )


objs =  bucket.objects.all()
for file_obj in objs:
    name = file_obj.key
    temp = name.split("/")
    url = "/".join(temp[:-1])
    response = temp[-1]
    print (url,response)
    wp_attack.update_one(
        { 'url': url},
        { '$inc': {'ntries':1}, '$set':{'response':response}}
    )
    print (wp_attack.find_one({"url":url}))
    print ("-------------")
