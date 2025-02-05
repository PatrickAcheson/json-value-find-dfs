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
skip = False
for index, letter in enumerate("[" + result):
    if skip:
        skip = False
        continue
    print("debug:", index, letter)
    if letter == ".":
        if result[index - 2] == "]":
            usable_path += "["
            continue
        usable_path += "]["
    elif (index) < len(result) -1:
        if result[index + 1] == "[":
            usable_path += f"{result[index - 1]}{result[index]}]"
            skip = True
        else:
            usable_path += str(letter)
    else:
        usable_path += str(letter)

print("\n", usable_path)

# print(json_data)

print(f"Path to '{goal}': {result}")