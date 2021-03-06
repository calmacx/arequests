import random
import pymongo
import requests
import json
import time

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
wp_attack.drop()
exit(0)

def move_to_backup():
    new_wp_attack = db['backup']
    found = wp_attack.find({'response':{'$ne':None}},{'_id':0,'url':1,'response':1})
    n=found.count()
    print (n)
    documents = []
    for i,obj in enumerate(list(found)):
        url = obj['url']
        response = obj['response']
        documents.append({'url':url,'ntries':1,'response':response})
        if i%1000 == 0 :
            print (f"{i}/{n} done")
    print ("now registering")
    new_wp_attack.insert_many(documents)


exit(0)

checks = wp_attack.aggregate([{'$sample':{'size':10}}])#,{'_id':0,'url':1})
checks = wp_attack.find({})
nrecords = checks.count()
print (f"looking in {nrecords} for duplicates...")
for i,check in enumerate(checks):
    url = check['url']
    #print (url)
    #count = wp_attack.find({'url':url}).count()
    if i%1000 == 0:
        print (f"{i}/{nrecords} done")
    #for item in list(wp_attack.find({'url':url})):
    #    print ("\t",item)
    
