from flask import render_template
from webapp import app
from flask import request
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
from webapp.a_Model import ModelIt
from pymongo import MongoClient
import pymongo
import datetime
from datetime import timedelta

# Python code to connect to Postgres
# You may need to modify this based on your OS,
# as detailed in the postgres dev setup materials.
# user = 'kylefrankovich' #add your Postgres username here
# host = 'localhost'
# dbname = 'birth_db'
# db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
# con = None
# con = psycopg2.connect(database = dbname, user = user)

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

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
       title = 'Home', user = { 'nickname': 'Miguel' },
       )

@app.route('/db')
def birth_page():
    sql_query = """
                SELECT * FROM birth_data_table WHERE delivery_method='Cesarean';
                """
    query_results = pd.read_sql_query(sql_query,con)
    births = ""
    for i in range(0,10):
        births += query_results.iloc[i]['birth_month']
        births += "<br>"
    return births

@app.route('/db_fancy')
def cesareans_page_fancy():
    sql_query = """
               SELECT index, attendant, birth_month FROM birth_data_table WHERE delivery_method='Cesarean';
                """
    query_results=pd.read_sql_query(sql_query,con)
    births = []
    for i in range(0,query_results.shape[0]):
        births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['attendant'], birth_month=query_results.iloc[i]['birth_month']))
    return render_template('cesareans.html',births=births)

@app.route('/ink_test')
def ink_test():
    sorted_posts = collection.find({"contains_tattoo": 1}).sort([("likes", pymongo.DESCENDING)]) # can add more complex query to only show recent data
    df =  pd.DataFrame(list(sorted_posts))
    df[df['date_added'] > search_date] # only include data w/in past week
    df_table = []
    for i in range(0,df.shape[0]):
        df_table.append(dict(account=df.iloc[i]['account'], likes=df.iloc[i]['likes'], link_to_post=df.iloc[i]['link_to_post']))
    return render_template('inkquery.html',df_table=df_table)

@app.route('/template_test')
def template_test():
    return render_template('index_gallery.html')


@app.route('/input')
def cesareans_input():
    return render_template("input.html")


@app.route('/output')
def cesareans_output():
  #pull 'birth_month' from input field and store it
  patient = request.args.get('birth_month')
    #just select the Cesareans  from the birth dtabase for the month that the user inputs
  query = "SELECT index, attendant, birth_month FROM birth_data_table WHERE delivery_method='Cesarean' AND birth_month='%s'" % patient
  print(query)
  query_results=pd.read_sql_query(query,con)
  print(query_results)
  births = []
  for i in range(0,query_results.shape[0]):
      births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['attendant'], birth_month=query_results.iloc[i]['birth_month']))
      the_result = ''
  the_result = ModelIt(patient,births)
  return render_template("output.html", births = births, the_result = the_result)
