import praw
import datetime as dt
import os
import pymysql as sql
import openai as ai
import time 
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

#Access OpenAI API
AI_KEY = os.environ["AI_KEY"]
ai.api_key = AI_KEY


def get_topic(title): #version number 3.5-turbo

    #Prompt for Chat-Gpt
    prompt = f'''Please identify the publicly traded company discussed in the following information: 
    {title} Please respond with the company name and then its stock market abbreviation in that order. 
    Example: "Company Name", "Stock Abbreviation" You response should strictly follow this format and do not use
    any other words. Response Example: apple, inc, aapl 
    Response Example: microsoft, msft
    Response Example: Meta, inc., meta
    Follow this formatting strictly and do not include anything extra or anything less than this format.
    Do not repreat the information given to you or include anything other than the specific format given above. 
    Do not include any other information in your answer other than these two pieces of information 
    separated by a comma. No other end punctuation should be included in your answer including 
    periods. If no company is found to be the topic of the shown information, respond with an empty string.'''

    #messages = [{"content": prompt}]

    response = ai.Completion.create(
        model="text-curie-001",
        prompt=prompt,
        temperature=0, # this is the degree of randomness of the model's output
    )
    #return response.choices[0].message["content"]
    return response.choices[0].text.strip()
cursor = connection.cursor()
#access wallstreetbets subreddit
subreddit = reddit.subreddit("wallstreetbets")
posts = subreddit.new(limit = 5)

#Iterate over posts
for post in posts:
    post_id = post.id
    post_title =  post.title
    post_score = post.score
    post_time = dt.datetime.fromtimestamp(post.created_utc)
    post_body = post.selftext[:10000]
    topic = get_topic(post_title).lower()
    #Create SQL statement and post values
    print(topic)
    post_insert_query = 'INSERT INTO posts (id, title, score, created_utc, body, topic) VALUES (%s, %s, %s, %s, %s, %s)'
    post_values = (post_id, post_title, post_score, post_time, post_body, topic)

        #commit values into SQL database
    cursor.execute(post_insert_query, post_values)
    connection.commit()
    post.comments.replace_more(limit = 5)
    for comment in post.comments.list():
        comment_body = comment.body

        comment_insert_query = "INSERT INTO comments (id, body, topic) VALUES (%s, %s, %s)"
        comment_values = (post_id, comment_body, topic)

        cursor.execute(comment_insert_query, comment_values)
        connection.commit()
    
        


cursor.close()
connection.close()

