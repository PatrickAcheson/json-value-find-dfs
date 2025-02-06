# given value you want aka "c" input to find json path
# output: root.nested_object.array_of_objects[0].data.nested_array[2]
# final usable keys to find given value


class jseek_demo():
    # should have combined fuctions into one
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
        # i forgot
        full_str = "[" + path
        usable_path = ""
        skip = False
        for index, letter in enumerate(full_str):
            if skip:
                skip = False
                continue
            if letter == ".":
                if full_str[index - 2] == "]":
                    usable_path += "["
                    continue
                usable_path += "]["
            elif index < len(full_str) - 1:
                if full_str[index + 1] == "[":
                    usable_path += f"{full_str[index - 1]}{full_str[index]}]"
                    skip = True
                else:
                    usable_path += letter
            else:
                usable_path += letter

        if not usable_path.endswith("]"):
            usable_path += "]"
        
        import re
        def add_quotes(match):
            key = match.group(1)
            if key.isdigit():
                return f"[{key}]"
            else:
                return f"['{key}']"
        
        usable_path = re.sub(r"\[([^\[\]]+)\]", add_quotes, usable_path)
        return usable_path
    
    def traverse_path(self, usable_path):
        import re
        keys = re.findall(r"\[['\"]?([^'\"]+)['\"]?\]", usable_path)
        current = self.json_data
        for key in keys:
            if key.isdigit():
                current = current[int(key)]
            else:
                current = current[key]
        return current

    def test(self, target_value):
        path = self.find_path_to_value(target_value)
        if path is None:
            print("Value not found!")
            return
        usable_path = self.clean_path(path)
        print("Dot/bracket path:", path)
        print("Usable path:", usable_path)

        value = self.traverse_path(usable_path)
        print("Your value:", value)

jseek = jseek_demo()

target_value = "c"
jseek.test(target_value)