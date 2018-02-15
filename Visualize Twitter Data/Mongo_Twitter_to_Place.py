'''
Created on Apr 25, 2017
@author: Xuebin Wei
www.lbsocial.net
'''
import pymongo
from pymongo import MongoClient

from time import mktime
from datetime import datetime
from time import strptime
import pyodbc 
from pprint import pprint

client = MongoClient()#type your own server configuration 
db = client.tweet_db # change to your tweet db

tweet_collection = db.tweet_collection # change to your tweet collection

tweet_collection.create_index([("id", pymongo.ASCENDING)],unique = True)
# tweet_cursor = tweet_collection.find({'coordinates' : {"$ne" : None}}) # get tweet with coordinates
tweet_cursor = tweet_collection.find({'id' : {"$ne" : None}})
num_of_tweet = float(tweet_cursor.count())

db_file = '' #change the location to your Access file
odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' %(db_file) # define the odbc connection parameter


conn = pyodbc.connect(odbc_conn_str)

cursor = conn.cursor()
i = 0
for document in tweet_cursor:
#     pprint(document)
#     try:
    tweet_created_at = document["created_at"].split()
    
    
    tweet_month = strptime(tweet_created_at[1],'%b').tm_mon
    if tweet_month<10:
        tweet_month_str = '0'+ str(tweet_month)
    else:
        tweet_month_str = str(tweet_month)
    
    tweet_date =tweet_created_at[5]+'-'+tweet_month_str+'-'+tweet_created_at[2]
    tweet_time = tweet_created_at[3]
    tweet_date_time = tweet_date +' '+tweet_time
    time_diff = datetime.now()-datetime.fromtimestamp(mktime(strptime(tweet_date_time, "%Y-%m-%d %H:%M:%S"))) 
    
    if document["coordinates"] is not None:
        x = document["coordinates"]['coordinates'][0]
        y = document["coordinates"]['coordinates'][1]
        z = (time_diff.total_seconds()+4.0*60*60)/50000.0 # height of tweet points, relative time difference to current time, recent tweets on top

    else:
        x =  'Null'
        y =  'Null'
        z =  'Null'
    
    if document["place"] is not None:
        place = document["place"]["full_name"]
        
    elif document["user"]["location"] is not None:
        place = document["user"]["location"]
    else:
        place = 'None'

    i = i+1 
    print(i/num_of_tweet)
#     print (i)
    sql_insert_statement = """insert into tweet(tweet_id, user_id,tweet_date, tweet_time, tweet_date_time, x, y,z, place) values('{}','{}','{}','{}','{}',{},{},{},'{}');""".format\
                             (document['id_str'],document["user"]["id_str"],tweet_date,tweet_time,tweet_date_time,x,y,z,place)
#     print (sql_insert_statement)
    try: 
        cursor.execute(sql_insert_statement)
        cursor.commit()
    except:
        pass

cursor.close()
conn.close()
