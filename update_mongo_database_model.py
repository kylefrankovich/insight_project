# update mongo database posts w/ model classification
import json
from pymongo import MongoClient
import datetime
import os
from PIL import Image
from io import StringIO
from io import BytesIO
from urllib.parse import urlparse
import pandas as pd
import pickle
import csv
import urllib
import urllib.request
import requests
import sys
from SVM_functions import process_image_url, process_image

# load classifier:

model_filename = '/home/ubuntu/insight_project/trained_models/svm_model_1000.sav'
loaded_model = pickle.load(open(model_filename, 'rb'))


# make connection with MongoClient:
client = MongoClient('localhost', 27017)

# creating/opening database:
db = client.insight_database

# opening collection (instagram posts):
collection = db.gram_posts_TEST

current_date = datetime.datetime.now()

# code for looping through shop/artist posts, add to database

rootdir = '/home/ubuntu/insight_project_data'

insta_url = 'https://www.instagram.com/p/'

for root, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith('.json'):
            current_account_data = json.load(open(os.path.join(root, file))) # load current account .json (shop or artist)
            account_name = os.path.basename(root)
            for post in current_account_data: # loop throough all posts for account
                if collection.find({"URL": post['display_url']}).count() == 0: # only add current post if not in database
                    try:
                        # older scrapes may have outdated direct URLs, check them here
                        features = process_image_url(post['display_url'])
                        prediction = loaded_model.predict([features])[0]
                    except:
                        continue
                    print()
                    print('current URL:', post['display_url'])
                    temp_dict = {}
                    temp_dict['account'] = account_name
                    temp_dict['URL'] = post['display_url']
                    temp_dict['link_to_post'] = insta_url + post['shortcode']
                    temp_dict['likes'] = post['edge_media_preview_like']['count']
                    temp_dict['owner_id'] = post['owner']['id']
                    temp_dict['dimensions'] = post['dimensions']
                    if 'tags' in post.keys():
                        temp_dict['tags'] = post['tags']
                    else:
                        temp_dict['tags'] = []
                    if post['edge_media_to_caption']['edges']:
                        temp_dict['caption'] = post['edge_media_to_caption']['edges'][0]['node']['text']
                    else:
                        temp_dict['caption'] = 'no caption'
                    temp_dict['date_added'] = current_date

                    if prediction.astype(int) == 1: # weird encoding thing with mongo, doesn't like numpy
                        temp_dict['contains_tattoo'] =  1 # need to update here with model when ready
                    elif prediction.astype(int) == 0:
                        temp_dict['contains_tattoo'] =  0
                    print(temp_dict)
                    collection.insert_one(temp_dict)

print('posts in database:',collection.count())
