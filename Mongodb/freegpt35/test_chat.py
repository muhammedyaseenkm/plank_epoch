import requests

def retrieve_chat(content=None):
    # Define the API endpoint
    url = "http://localhost:3000/v1/chat/completions"
    
    # Define the request headers
    headers = {
        "Authorization": "Bearer anything_or_your_key",
        "Content-Type": "application/json"
    }
    
    # Define the request body with dynamic content if provided
    if content is not None:
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": content}]
        }
    else:
        # If no content provided, use an empty message
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": ""}]
        }
    
    # Make the POST request
    response = requests.post(url, headers=headers, json=data)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("Request successful!")
        print("Response content:")
        response_data = response.json()
        response_content = response_data['choices'][0]['message']['content']
        return response_data
    else:
        print("Request failed with status code:", response.status_code)
        return None

# Example usage with content
response_with_content = retrieve_chat("Hello")
print(response_with_content)  # This will print the response content if the request was successful

# Example usage without content
response_without_content = retrieve_chat()
print(response_without_content)  # This will print the response content if the request was successful
