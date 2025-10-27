import httpx
import json

# Test the RAG API endpoint
base_url = "http://127.0.0.1:6000"

# Test questions from the requirements
test_questions = [
    "What does the author affectionately call the => syntax?",
    "Which operator converts any value into an explicit boolean?"
]

print("Testing RAG API Endpoint")
print("=" * 60)
print(f"Base URL: {base_url}\n")

for i, question in enumerate(test_questions, 1):
    print(f"Test {i}: {question}")
    
    try:
        # Make GET request with query parameter
        response = httpx.get(
            f"{base_url}/search",
            params={"q": question},
            timeout=30.0
        )
        response.raise_for_status()
        
        result = response.json()
        print(f"Status: {response.status_code}")
        print(f"Answer: {result['answer']}")
        print(f"Source: {result.get('sources', 'N/A')}")
        print("-" * 60)
        
    except Exception as e:
        print(f"Error: {e}")
        print("-" * 60)

print("\n✅ API Endpoint URL:")
print(f"{base_url}/search?q=your_question")
