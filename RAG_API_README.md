# TechDocs RAG API

## API Endpoint

**Base URL:** `http://127.0.0.1:6000`

**Search Endpoint:** `http://127.0.0.1:6000/search?q=your_question`

## Description

This RAG (Retrieval Augmented Generation) API searches TypeScript documentation to answer questions about TypeScript.

## Usage

### GET Request

**Endpoint:** `/search`

**Query Parameter:** `q` (required) - The question to search for

**Example Requests:**

1. Question: "What does the author affectionately call the => syntax?"
   ```
   GET http://127.0.0.1:6000/search?q=What does the author affectionately call the => syntax?
   ```

2. Question: "Which operator converts any value into an explicit boolean?"
   ```
   GET http://127.0.0.1:6000/search?q=Which operator converts any value into an explicit boolean?
   ```

### Response Format

```json
{
  "answer": "The fat arrow syntax is affectionately called the fat arrow...",
  "sources": "TypeScript Book - Arrow Functions"
}
```

## Example Answers

- **Q:** "What does the author affectionately call the => syntax?"
  - **A:** Contains "fat arrow"

- **Q:** "Which operator converts any value into an explicit boolean?"
  - **A:** Contains "!!"

## Features

- ✅ CORS enabled for all origins
- ✅ GET requests with query parameters
- ✅ Semantic search using embeddings
- ✅ Returns relevant documentation excerpts
- ✅ Includes source references

## Server Status

The server is running on **port 6000**

API Endpoint: **http://127.0.0.1:6000/search?q=your_question**
