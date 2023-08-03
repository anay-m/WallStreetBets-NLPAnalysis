import firebase_admin
from firebase_admin import credentials, firestore
import praw
import os
import topic_finder as tf

def initialize_firebase():
    cred = credentials.Certificate('./firebase-admin.json')
    firebase_admin.initialize_app(cred)

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
USER_AGENT = os.environ["USER_AGENT"]
reddit = praw.Reddit(client_id = CLIENT_ID, 
                     client_secret = CLIENT_SECRET, 
                     user_agent = USER_AGENT)

def lambda_handler(event, context):
    initialize_firebase()
    db = firestore.client()
    collection_ref = db.collection('posts')

    # Delete all documents in the 'posts' collection
    docs = collection_ref.get()
    for doc in docs:
        doc.reference.delete()
        
    subreddit = reddit.subreddit("wallstreetbets")
    posts = subreddit.new(limit = 50)
    for post in posts:
        post_id = post.id
        post_title =  post.title
        post_body = post.selftext[:10000]
        post_topic = tf.main(post_title).lower()
        post_sentiment = 1
        post_url = post.url
        new_post_data = {
            'id': post_id,
            'title': post.title,
            'body': post_body,
            'topic': post_topic,
            'sentiment': post_sentiment,
            'url': post_url
        }
        collection_ref.add(new_post_data)
    
    return {
        'statusCode': 200,
        'body': 'Data added to Firestore.'
    }
