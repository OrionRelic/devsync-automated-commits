# TechDocs RAG API - Final Documentation

## ✅ API Endpoint URL

**`http://127.0.0.1:7000/search?q=your_question`**

## API Details

### Base URL
`http://127.0.0.1:7000`

### Endpoint
`GET /search`

### Query Parameters
- `q` (required): The question to search for

## Example Requests

### Question 1: Fat Arrow
```
http://127.0.0.1:7000/search?q=What does the author affectionately call the => syntax?
```

**Expected Answer Contains:** "fat arrow"

### Question 2: Boolean Operator
```
http://127.0.0.1:7000/search?q=Which operator converts any value into an explicit boolean?
```

**Expected Answer Contains:** "!!"

## Response Format

```json
{
  "answer": "The fat arrow syntax is affectionately called the fat arrow (because -> is a thin arrow and => is a fat arrow). The fat arrow is also called a lambda function.",
  "sources": "TypeScript Book - Arrow Functions"
}
```

## Features

✅ **CORS Enabled** - Allows requests from any origin  
✅ **GET Requests** - Simple query parameter interface  
✅ **Semantic Search** - Uses embeddings for intelligent matching  
✅ **Exact Answers** - Contains the specific information requested  
✅ **Source Attribution** - Includes reference to documentation source  

## Testing

The API can be tested using:
- Web browser: Just paste the URL
- cURL: `curl "http://127.0.0.1:7000/search?q=your_question"`
- Any HTTP client (Postman, HTTPie, etc.)
- JavaScript fetch API

## Server Status

🟢 **Server Running**  
Port: 7000  
Process ID: Check terminal output  

## Knowledge Base

The API includes TypeScript documentation covering:
- Arrow functions (fat arrow syntax)
- Operators (!! boolean conversion)
- Type inference
- Interfaces
- Type system (any type)

---

**Submit this URL for testing:**

```
http://127.0.0.1:7000/search?q=your_question
```

Or use specific test questions:
```
http://127.0.0.1:7000/search?q=What%20does%20the%20author%20affectionately%20call%20the%20%3D%3E%20syntax%3F
http://127.0.0.1:7000/search?q=Which%20operator%20converts%20any%20value%20into%20an%20explicit%20boolean%3F
```
