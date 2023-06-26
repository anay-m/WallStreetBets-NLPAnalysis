import praw
import datetime as dt
import os
import pymysql as sql
import openai as ai
import time 
import topic_finder as tf
import asyncio
from multiprocessing import Pool
import multiprocessing as mp
import datetime
#Access Client Info
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
USER_AGENT = os.environ["USER_AGENT"]
reddit = praw.Reddit(client_id = CLIENT_ID, 
                     client_secret = CLIENT_SECRET, 
                     user_agent = USER_AGENT)

#Access SQL Database
HOST = os.environ["HOST"]
USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
DATABASE = os.environ["DATABASE"]

connection = sql.connect(host = HOST,
                         user= USER,
                         password= PASSWORD,
                         db= DATABASE)

cursor = connection.cursor()

cursor.execute("DELETE FROM posts")
connection.commit()

cursor.execute("DELETE FROM comments")
connection.commit()
#access wallstreetbets subreddit
subreddit = reddit.subreddit("wallstreetbets")
posts = subreddit.new(limit = 12)

# Get the current UTC time
current_utc = datetime.datetime.utcnow()

# Define the time threshold (24 hours ago)
time_threshold = current_utc - datetime.timedelta(hours=24)

def process_post(post):
    if datetime.datetime.utcfromtimestamp(post.created_utc) < time_threshold:
        return
    post_id = post.id
    post_title =  post.title
    post_score = post.score
    post_time = dt.datetime.fromtimestamp(post.created_utc)
    post_body = post.selftext[:10000]
    input = f"{post_title}, {post_body}"
    topic = tf.main(post_title).lower()
    #Create SQL statement and post values
    print(topic)
    post_insert_query = 'INSERT INTO posts (id, title, score, created_utc, body, topic) VALUES (%s, %s, %s, %s, %s, %s)'
    post_values = (post_id, post_title, post_score, post_time, post_body, topic)

        #commit values into SQL database
    cursor.execute(post_insert_query, post_values)
    connection.commit()
    post.comments.replace_more(limit = 20)
    for comment in post.comments.list():
        comment_body = comment.body

        comment_insert_query = "INSERT INTO comments (id, body, topic) VALUES (%s, %s, %s)"
        comment_values = (post_id, comment_body, topic)

        cursor.execute(comment_insert_query, comment_values)
        connection.commit()
        x = True
#Iterate over posts
#for post in posts:

num_processes = 5
count = 0
with Pool(num_processes) as pool:
    pool.map(process_post, posts)

pool.close()

"""post_list = list(posts)
print(dt.datetime.fromtimestamp(post_list[-1].created_utc))"""
        


cursor.close()
connection.close()

