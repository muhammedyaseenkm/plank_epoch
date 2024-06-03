mkdir freegpt35 && cd freegpt35

In windows Invoke-WebRequest -Uri 
curl -O https://raw.githubusercontent.com/hominsu/freegpt35/main/deploy/docker-compose.yml

docker compose up -d


In windows  use  Invoke-WebRequest -Method
curl -X POST "http://localhost:3000/v1/chat/completions" \
     -H "Authorization: Bearer anything_or_your_key" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "gpt-3.5-turbo",
           "messages": [{"role": "user", "content": "Hello"}],
         }'


>>>
{"id":"chatcmpl-*********","created":9999999999,"model":"gpt-3.5-turbo","object":"chat.completion","choices":[{"finish_reason":"stop","index":0,"message":{"content":"Hi there! How can I assist you today?","role":"assistant"}}],"usage":{"prompt_tokens":1,"completion_tokens":10,"total_tokens":11}}

>>>