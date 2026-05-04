import requests
GEMINI_API_KEY = 'AIzaSyDkP8_sNN16vComUZoaqIjjmmybpcxlpdw'
url = f'https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}'
resp = requests.get(url)
print(resp.text)
