import requests
import json

GEMINI_API_KEY = 'AIzaSyDkP8_sNN16vComUZoaqIjjmmybpcxlpdw'
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}'

body = {
    'contents': [{'parts': [{'text': 'Hello'}]}]
}

resp = requests.post(url, json=body)
print(f"Status: {resp.status_code}")
print(f"Body: {resp.text}")
