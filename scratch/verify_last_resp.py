import json
import re

with open('debug_api.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the last "Response: {"
matches = list(re.finditer(r'Response: \{', content))
if matches:
    last_resp_start = matches[-1].start() + len('Response: ')
    last_resp_text = content[last_resp_start:]
    
    # Try to parse the JSON response from the log
    try:
        resp_json = json.loads(last_resp_text)
        text = resp_json['candidates'][0]['content']['parts'][0]['text']
        print("--- START TEXT ---")
        print(text)
        print("--- END TEXT ---")
        
        # Try to parse the extracted text
        try:
            parsed = json.loads(text.strip())
            print("Successfully parsed JSON from model!")
        except Exception as e:
            print(f"Failed to parse model text: {e}")
            # Save the text to a file for investigation
            with open('failed_json.txt', 'w', encoding='utf-8') as f2:
                f2.write(text)
    except Exception as e:
        print(f"Failed to parse API response from log: {e}")
else:
    print("No response found in log.")
