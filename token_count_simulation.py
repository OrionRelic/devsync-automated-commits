import tiktoken

# The user message to be tokenized
user_message = "List only the valid English words from these: u2O, 5nDF, 27l2Oc2, KhXjGmv3, 4m5aPWW, wHnZBYvg, 9ZI7pZewep, GlRt, 9miueWD, a, uYZrRuroxB, 5, FCHDqp, camRSvG, 4Mhy3tb, Sq, jQTyxUYkG, AIbYXU5u, NAPHxYv, a3FhWQU, Z4xHh, BsGMr1xg3, PO, 1GMhblG, Q6O2bmlh, m5AJ5h1fOv, u, k2HP0J9Qkf, at6C, egW3, ty, uvhhvpMf, nTKpaGsU"

# Get the correct encoding for the gpt-4o-mini model
encoding = tiktoken.get_encoding("o200k_base")

# Encode the message into a list of token integers
tokens = encoding.encode(user_message)

# The length of the list is the final token count
token_count = len(tokens)

print(f"The number of input tokens is: {token_count}")
# Expected output: The number of input tokens is: 83
