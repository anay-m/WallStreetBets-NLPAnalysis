import praw
import datetime as dt
import os
import pymysql as sql
#Access Client Info
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
USER_AGENT = os.environ["USER_AGENT"]
reddit = praw.Reddit(client_id = CLIENT_ID, 
                     client_secret = CLIENT_SECRET, 
                     user_agent = USER_AGENT)

#Access SQL Database
"""HOST = os.environ["HOST"]
USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
DATABASE = os.environ["DATABASE"]

connection = sql.connect(host = HOST,
                         user= USER,
                         password= PASSWORD,
                         db= DATABASE)

cursor = connection.cursor()"""
#access wallstreetbets subreddit
subreddit = reddit.subreddit("wallstreetbets")
posts = subreddit.new(time_filter= 'day')

#Iterate over posts
for post in posts:
    if 'apple' in post.title.lower():
        post_id = post.id
        post_title =  post.title
        post_score = post.score
        post_time = dt.datetime.fromtimestamp(post.created_utc)
        post_body = post.selftext
        print(post_body)
        #Create SQL statement and post values
        post_insert_query = 'INSERT INTO posts (id, title, score, created_utc, body) VALUES (%s, %s, %s, %s, %s)'
        post_values = (post_id, post_title, post_score, post_time, post_body)

        #commit values into SQL database
        """cursor.execute(post.insert_query, post_values)
        connection.commit()"""
        post.comments.replace_more(limit = 10)
        for comment in post.comments.list():
            comment_body = comment.body
            print(comment_body)

        
            """comment_insert_query = "INSERT INTO comments (post_id, comment_body) VALUES (%s, %s)"
            comment_values = (post_id, comment_body)"""

            """cursor.execute(comment_insert_query, comment_values)
            connection.commit()

        


cursor.close()
connection.close()"""

