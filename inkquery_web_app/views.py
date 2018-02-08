from inkquery_web_app import app
from flask import render_template
import pandas as pd
from pymongo import MongoClient
import pymongo
import datetime
from datetime import timedelta
import urllib
import json

# client = MongoClient() # connects to default host and port, can also manually specify:
client = MongoClient('localhost', 27017)

# creating/opening database:
db = client.insight_database

# opening collection (instagram posts):
collection = db.gram_posts

# only include posts w/in past week
today = datetime.date.today()
margin = datetime.timedelta(days = 7)
search_date = today - margin


sorted_posts = collection.find({"contains_tattoo": 1}).sort([("likes", pymongo.DESCENDING)]) # can add more complex query to only show recent data
df =  pd.DataFrame(list(sorted_posts))
df = df[df['date_added'] > search_date] # only include data w/in past week
df = df[0:150]

link_htmls = []
for i in range(len(df[0:150])):
    try:
        post_url = 'https://api.instagram.com/oembed?url=' + df.iloc[i]['link_to_post'] + '/'
        response = urllib.request.urlopen(post_url)
        html = json.load(response)
        link_htmls.append(html['html'])
    except:
        continue

page_1_links = link_htmls[0:30]
page_2_links = link_htmls[30:60]
page_3_links = link_htmls[60:90]
page_4_links = link_htmls[90:120]
page_5_links = link_htmls[120:150]

# @app.route('/')
# @app.route('/index')
# def index():
#    return "Hello, World!"

# @app.route('/')
# @app.route('/index')
# def index():
#     return render_template("inkquery_template.html", posts = page_1_links)

@app.route('/')
@app.route('/index')
def index():
    return render_template("inkquery_template_formatting_test.html")

@app.route('/page_2')
def page_2():
    return render_template("inkquery_template_page_2.html", posts = page_2_links)

@app.route('/page_3')
def page_3():
    return render_template("inkquery_template_page_3.html", posts = page_3_links)


@app.route('/page_4')
def page_4():
    return render_template("inkquery_template_page_4.html", posts = page_4_links)

@app.route('/page_5')
def page_5():
    return render_template("inkquery_template_page_5.html", posts = page_5_links)

@app.route('/about_me')
def about_me():
    return render_template("about_me.html")

@app.route('/about_inkquery')
def about_inkquery():
    return render_template("about_inkquery.html")

@app.route('/contact')
def contact():
    return render_template("inkquery_template_page_5.html")
