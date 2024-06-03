import google.generativeai as genai
import os

# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
genai.configure(api_key='AIzaSyAwUnam6bwzIvEMna3-sknk5ZUVT8OS7wo')
model = genai.GenerativeModel('gemini-1.0-pro-latest')
response = model.generate_content("Explain to build the complete pipe line to use gemini from production to deployment")
print(response.text)