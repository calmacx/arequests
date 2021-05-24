import pymongo
import requests
import datetime
import json
from urllib.parse import urlparse

import boto3
s3 = boto3.resource('s3')
bucket = s3.Bucket("exploits-ai1wm")
objs =  bucket.objects.all()
print ('retrieved')
file_names = [file_obj.key for file_obj in objs]
print (json.dumps(file_names,indent=6))
