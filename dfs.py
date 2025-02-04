import json

with open('test.json', 'r') as f:
    json_data = json.load(f)

def find_path_to_value(json_data, target_value):
    queue = [("", json_data)]
    
    while queue:
        current_path, current_value = queue.pop(0)
        
        if isinstance(current_value, dict):
            for k, v in current_value.items():
                new_path = f"{current_path}.{k}" if current_path else k
                queue.append((new_path, v))
        elif isinstance(current_value, list):
            for index, item in enumerate(current_value):
                new_path = f"{current_path}[{index}]" if current_path else f"[{index}]"
                queue.append((new_path, item))
        else:
            if current_value == target_value:
                return current_path
    return None

goal = "c"
result = find_path_to_value(json_data, goal)

usable_path = ""
start = True
for index, letter in enumerate(result):
    if letter == ".":
        if start:
            usable_path += "["
            start = False
            continue
        usable_path += "]["
    elif index == len(result) - 1:
        usable_path += "]"
    else:
        usable_path += str(letter)

print(usable_path)

print(json_data[usable_path])

print(f"Path to '{goal}': {result}")