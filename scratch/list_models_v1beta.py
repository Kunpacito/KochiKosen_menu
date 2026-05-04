import requests
GEMINI_API_KEY = 'AIzaSyBCcbxH0LYgj5yCd1fflp9hVX4rNTgNGT4'
url = f'https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}'
resp = requests.get(url)
print(resp.json())
