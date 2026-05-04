import json
import re

with open('debug_api.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the last "Response: {"
matches = list(re.finditer(r'Response: \{', content))
if matches:
    last_resp_start = matches[-1].start() + len('Response: ')
    last_resp_text = content[last_resp_start:]
    
    # Try to extract the text part
    try:
        # We need to find the "text": "..." part and unescape it
        # Since it's in a log, it might be double escaped.
        # Let's try to parse the outer JSON first.
        # But the log entry itself might be partial or broken due to the way it was written.
        
        # Alternative: look for the first { and last } in the remaining text
        start = last_resp_text.find('{')
        end = last_resp_text.rfind('}')
        if start != -1 and end != -1:
            json_blob = last_resp_text[start:end+1]
            with open('last_json_raw.json', 'w', encoding='utf-8') as f2:
                f2.write(json_blob)
            print("Saved last_json_raw.json")
    except Exception as e:
        print(f"Error: {e}")
