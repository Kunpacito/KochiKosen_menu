with open('debug_api.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    # Get the last 20 lines
    for line in lines[-20:]:
        print(line)
