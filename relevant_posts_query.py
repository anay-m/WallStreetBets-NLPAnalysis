import json
from sentence_transformers import SentenceTransformer
import torch
import pinecone

pinecone.init(
    api_key= "e41d9382-7d0c-4537-8635-5235bc87759d",
    environment= "us-west4-gcp-free"
)

device = 'cuda' if torch.cuda.is_available() else 'cpu'

model = SentenceTransformer('all-MiniLM-L6-v2', device= device)
index_name = 'semantic-search-stock-symb'

# now connect to the index
symb_index = pinecone.GRPCIndex(index_name)


def lambda_handler(event, context):
    
    query = event["query"]
    xq = model.encode(query).tolist()
    xc = symb_index.query(xq, top_k=10, include_metadata=True)
    results = []
    for match in xc["matches"]:
        results.append(match["metadata"]["text"])
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }