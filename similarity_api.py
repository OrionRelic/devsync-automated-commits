from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
import logging

# It's recommended to set the API key as an environment variable for security
# For example: export OPENAI_API_KEY='your-api-key'
# If the environment variable is not set, you can pass it directly to the client:
# client = OpenAI(api_key="YOUR_API_KEY")

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def get_embedding(text: str, model="text-embedding-3-small"):
   api_key = os.environ.get("OPENAI_API_KEY")
   if not api_key:
       raise HTTPException(status_code=401, detail="OpenAI API key is missing or invalid. Please set the OPENAI_API_KEY environment variable.")
   
   client = OpenAI(api_key=api_key)
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

class SimilarityRequest(BaseModel):
    docs: List[str]
    query: str

class SimilarityResponse(BaseModel):
    matches: List[str]

@app.post("/similarity", response_model=SimilarityResponse)
async def get_similarity(request: SimilarityRequest):
    """
    Accepts a list of documents and a query, and returns the top 3 most similar documents.
    """
    if not request.docs or not request.query:
        raise HTTPException(status_code=400, detail="Docs and query cannot be empty.")

    try:
        # Generate embeddings for the documents and the query
        doc_embeddings = [get_embedding(doc) for doc in request.docs]
        query_embedding = get_embedding(request.query)

        # Compute cosine similarity
        similarities = cosine_similarity([query_embedding], doc_embeddings)[0]

        # Get the indices of the top 3 most similar documents
        top_3_indices = np.argsort(similarities)[-3:][::-1]

        # Get the content of the top 3 documents
        top_matches = [request.docs[i] for i in top_3_indices]

        return SimilarityResponse(matches=top_matches)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        # Check if the error is related to the API key
        if "OPENAI_API_KEY" in str(e):
            raise HTTPException(status_code=401, detail="OpenAI API key is missing or invalid. Please set the OPENAI_API_KEY environment variable.")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
