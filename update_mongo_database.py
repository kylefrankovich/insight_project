import json
from pymongo import MongoClient
import datetime
import os

# make connection with MongoClient:
client = MongoClient('localhost', 27017)

# creating/opening database:
db = client.insight_database

# opening collection (instagram posts):
collection = db.posts

current_date = datetime.datetime.now()

# code for looping through shop/artist posts, add to database

rootdir = '/Users/kylefrankovich/Desktop/insight_project_data'

insta_url = 'https://www.instagram.com/p/'

for root, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith('.json'):
            current_account_data = json.load(open(os.path.join(root, file))) # load current account .json (shop or artist)
            account_name = os.path.basename(root)
            for post in current_account_data: # loop throough all posts for account
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
                temp_dict['contains_tattoo'] = 1 # need to update here with model when ready
                if collection.find({"URL": temp_dict['URL']}).count() == 0: # only add current post if not in database
                    collection.insert_one(temp_dict)
