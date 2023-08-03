import json
import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase():
    cred = credentials.Certificate('./firebase-admin.json')
    firebase_admin.initialize_app(cred)
    
initialize_firebase()

def lambda_handler(event, context):
    collection_ref = firestore.client().collection('posts')
    query = event["query"]
    
    query_ref = collection_ref.where('topic', '==', query)
    snapshot = query_ref.get()
    
    results = {"positive":0, "negative": 0, "neutral": 0}
    for doc in snapshot:
        post_data = doc.to_dict()
        sentiment = post_data["sentiment"]
        if sentiment >= 0.65:
            results["positive"] += 1
        elif sentiment >= 0.35 and sentiment < 0.65:
            results["neutral"] += 1
        else:
            results["negative"] += 1
            
    snapshot_length = len(snapshot)
    results["positive"] = round(results["positive"]/snapshot_length * 100, 2)
    results["negative"] = round(results["negative"]/snapshot_length * 100, 2)
    results["neutral"] = round(results["neutral"]/snapshot_length * 100, 2)
    results["total"] = snapshot_length
    
    return {
        'statusCode': 200,
        'body': results
    }