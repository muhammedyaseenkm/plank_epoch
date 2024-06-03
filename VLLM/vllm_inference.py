import requests

# Define the vLLM server URL
VLLM_API_URL = "http://localhost:8000/v1/completions"

# Define the payload for the request
payload = {
    "model": "facebook/opt-125m",
    "prompt": "San Francisco is a",
    "max_tokens": 10,
    "temperature": 0.7,
    "top_p": 0.9,
}

# Send a POST request to the vLLM API
response = requests.post(VLLM_API_URL, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Print the generated text
    completion = response.json()
    print("Generated text:", completion["choices"][0]["text"])
else:
    print("Request failed with status code:", response.status_code)
    print("Response:", response.text)
