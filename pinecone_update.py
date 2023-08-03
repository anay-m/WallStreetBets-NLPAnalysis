from sentence_transformers import SentenceTransformer
import torch
import pinecone
import praw
from better_profanity import profanity
import os
from tqdm.auto import tqdm

PINECONEKEY = os.environ["PINECONEKEY"]
pinecone.init(
    api_key= PINECONEKEY,
    environment= "us-west4-gcp-free"
)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
index_name = 'semantic-search-stock-symb'

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
USER_AGENT = os.environ["USER_AGENT"]
reddit = praw.Reddit(client_id = CLIENT_ID, 
                     client_secret = CLIENT_SECRET, 
                     user_agent = USER_AGENT)
subreddit = reddit.subreddit("wallstreetbets")

batch_size = 128

def lambda_handler(event, context):
    
    post_list = list(subreddit.new(limit = 500))
    for i in range(len(post_list)-1, -1, -1):
        if profanity.contains_profanity(post_list[i]):
            post_list.pop(i)
    pinecone.delete_index(index_name)
    pinecone.create_index(
        name=index_name,
        dimension=model.get_sentence_embedding_dimension(),
        metric='cosine'
    )
    symb_index = pinecone.GRPCIndex(index_name)
    for i in tqdm(range(0, len(post_list), batch_size)):
        # find end of batch
        i_end = min(i+batch_size, len(post_list))
        # create IDs batch
        ids = [str(x) for x in range(i, i_end)]
        # create metadata batch
        metadatas = [{'text': text} for text in post_list[i:i_end]]
        # create embeddings
        xc = model.encode(post_list[i:i_end])
        # create records list for upsert
        records = zip(ids, xc, metadatas)
        # upsert to Pinecone
        symb_index.upsert(vectors=records)
    
    return {
        'statusCode': 200,
        'body': "success"
    }