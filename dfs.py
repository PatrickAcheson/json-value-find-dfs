class jseek_demo():
    def __init__(self):
        import json
        with open('test.json', 'r') as f:
            self.json_data = json.load(f)

    def find_path_to_value(self, target_value):
        queue = [("", self.json_data)]
        
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

    def clean_path(self, path):
        usable_path = ""
        start = True
        skip = False
        for index, letter in enumerate("[" + path):
            if skip:
                skip = False
                continue
            if letter == ".":
                if path[index - 2] == "]":
                    usable_path += "["
                    continue
                usable_path += "]["
            elif (index) < len(path) - 1:
                if path[index + 1] == "[":
                    usable_path += f"{path[index - 1]}{path[index]}]"
                    skip = True
                else:
                    usable_path += str(letter)
            else:
                usable_path += str(letter)
        
        import re
        def add_quotes(match):
            key = match.group(1)
            if key.isdigit():
                return f"[{key}]"
            else:
                return f"['{key}']"
        
        usable_path = re.sub(r"\[([^\[\]]+)\]", add_quotes, usable_path)
        return usable_path
    

jseek = jseek_demo()
path = jseek.find_path_to_value("c")
usable_path = jseek.clean_path(path)

print("\n", usable_path)

