# InfoCore Semantic Search API

## API Endpoint

**URL:** `http://127.0.0.1:8001/search`

## Description

This FastAPI endpoint computes semantic similarity between a query and a list of documents using OpenAI's text-embedding-3-small model.

## Request

**Method:** POST

**Endpoint:** `/search`

**Content-Type:** application/json

**Body:**
```json
{
  "docs": [
    "Contents of document 1",
    "Contents of document 2",
    "Contents of document 3"
  ],
  "query": "Your search query"
}
```

## Response

**Content-Type:** application/json

**Body:**
```json
{
  "matches": [
    "Most similar document",
    "Second most similar document",
    "Third most similar document"
  ]
}
```

The response returns the top 3 documents ranked by cosine similarity to the query.

## Features

- ✅ CORS enabled for all origins, methods, and headers
- ✅ Uses OpenAI text-embedding-3-small model
- ✅ Computes cosine similarity between query and documents
- ✅ Returns top 3 most relevant matches

## Example Usage

### Using curl:
```bash
curl -X POST http://127.0.0.1:8001/search \
  -H "Content-Type: application/json" \
  -d '{
    "docs": [
      "Python is a programming language",
      "FastAPI is a web framework",
      "Machine learning requires data"
    ],
    "query": "How to build APIs?"
  }'
```

### Using Python:
```python
import httpx

response = httpx.post(
    "http://127.0.0.1:8001/search",
    json={
        "docs": [
            "Python is a programming language",
            "FastAPI is a web framework",
            "Machine learning requires data"
        ],
        "query": "How to build APIs?"
    }
)

print(response.json())
```

## Server Status

Server is running on: **http://127.0.0.1:8001**

Endpoint: **http://127.0.0.1:8001/search**
