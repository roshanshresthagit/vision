import ast
import json

with open("functions.py", "r") as f:
    tree = ast.parse(f.read())

data = {}
function_callable={}

for node in tree.body:
    if isinstance(node, ast.FunctionDef):
        func_name = node.name
        input_names = [arg.arg for arg in node.args.args]
        num_inputs = len(input_names)
        return_vars = []
    

        for stmt in node.body:
            if isinstance(stmt, ast.Return):
                if isinstance(stmt.value, ast.Name):
                    return_vars.append(stmt.value.id)
                elif isinstance(stmt.value, ast.Tuple):
                    return_vars.extend([elt.id for elt in stmt.value.elts if isinstance(elt, ast.Name)])
        
        data[func_name] = {
            "inputs": num_inputs,
            "outputs": len(return_vars),
            "inputNames": input_names,
            "outputNames": return_vars
        }

  

def format_data(data):
    json_str = json.dumps(data, indent=2)
    return json_str

formatted_output = format_data(data)

with open("function_dictonary.json", "w") as file:
    file.write(formatted_output)

function_names = [
    {"id": func_name, "label": func_name.capitalize(), "func": func_name}
    for func_name in data.keys()
]
function_names_json = json.dumps(function_names, indent=2)


with open("function_names.json", "w") as file:
    file.write(str(function_names_json))



# function_handler = {func_name: f"function.{func_name}" for func_name in data.keys()}

# # Write valid JSON (strings as values)
# with open("function_handler.json", "w") as file:
#     json.dump(function_handler, file, indent=2)
