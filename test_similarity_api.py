import httpx
import json

# Test the similarity endpoint
url = "http://127.0.0.1:8000/similarity"

# Sample test data
test_payload = {
    "docs": [
        "Python is a high-level programming language.",
        "FastAPI is a modern web framework for building APIs.",
        "Machine learning models require large datasets.",
        "Semantic search uses embeddings to find relevant documents."
    ],
    "query": "How to build REST APIs with Python?"
}

print("Testing the /similarity endpoint...")
print(f"URL: {url}")
print(f"\nRequest payload:")
print(json.dumps(test_payload, indent=2))

try:
    response = httpx.post(url, json=test_payload, timeout=30.0)
    response.raise_for_status()
    
    result = response.json()
    print(f"\nResponse (Status {response.status_code}):")
    print(json.dumps(result, indent=2))
    
    print("\n✅ Success! The API is working correctly.")
    print(f"\nAPI endpoint: {url}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
