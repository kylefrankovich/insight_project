# script to pull artist instagram handles from shops within a given city,
# provided by *city*_shops.txt

import os
import json
import csv

artist_list = []

def get_insta_handle(caption):
    return [word for word in caption.split() if word.startswith('@')]

for root, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith(".json"):
            current_shop_data = json.load(open(os.path.join(root, file))) # load current shop .json
            for post in current_shop_data: # loop through all posts w/in a shop
                if post['edge_media_to_caption']['edges']: # only check for artists if there's a comment
                    insta_handles = get_insta_handle(post['edge_media_to_caption']['edges'][0]['node']['text']) # posts might name multiple artists
                    for artist in insta_handles:
                        if artist not in artist_list:
                            artist_list.append(artist)


# export artist_list to a csv to later scrape insta:

filename = '/Users/kylefrankovich/Desktop/insight_project/chicago_artist_list.csv'
with open(filename, 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_MINIMAL)
    wr.writerow(artist_list)
