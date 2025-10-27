import httpx

# OpenAI API endpoint
url = "https://api.openai.com/v1/chat/completions"

# Dummy API key for testing
api_key = "dummy-api-key"

# The meaningless test text
test_text = """yd 3rMiiCmW 
 ZA fel Fbc5JF2l z  2lIqANioh AvsesI"""

# Prepare the request payload
payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
            "role": "system",
            "content": "Analyze the sentiment of the text and classify it as GOOD, BAD, or NEUTRAL."
        },
        {
            "role": "user",
            "content": test_text
        }
    ]
}

# Send POST request with Authorization header
response = httpx.post(
    url,
    json=payload,
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
)

# Raise an exception if the request failed
response.raise_for_status()

# Parse and display the response
result = response.json()
print("API Response:")
print(result)
