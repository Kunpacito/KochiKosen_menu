import requests
import json

GEMINI_API_KEY = 'AIzaSyBCcbxH0LYgj5yCd1fflp9hVX4rNTgNGT4'

def test_v1beta_2_0():
    prompt = "Return a JSON with a list of 3 fruits."
    body = {
        'contents': [{'parts': [
            {'text': prompt}
        ]}],
        'generationConfig': {
            'temperature': 0.2, 
            'maxOutputTokens': 2048,
            'responseMimeType': 'application/json'
        }
    }

    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}'
    
    print(f"Testing URL: {url}")
    resp = requests.post(url, json=body)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text[:500]}")

if __name__ == "__main__":
    test_v1beta_2_0()
