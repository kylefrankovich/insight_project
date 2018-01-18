# script to pull artist instagram handles from shops within a given city,
# provided by *city*_shops.txt

import os
import datetime

# instagram-scraper deluxetattoochicago --maximum 20 --media-types none --include-location --destination /Users/kylefrankovich/Desktop/insight/project_ideas/test_data
now = datetime.datetime.now()
download_folder = os.getcwd() + '/' + now.strftime("%Y-%m-%d") + '_scrape'

# download recent metadata for each shop within the city shop list file:
instagram-scraper --filename shop_list_test.txt --maximum 50 --media-types none --include-location --destination '/Users/kylefrankovich/Desktop/insight_project/2018-01-17_scrape' --retain-username
