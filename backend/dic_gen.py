import ast

#### function to extract the source code's name, args, inputs and outputs.
def parse_function(source_code):
    """Parse a function's source code and extract its name, arguments, inputs and outputs"""
    tree = ast.parse(source_code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args = {}
            num_args = len(node.args.args)
            num_defaults = len(node.args.defaults)

            for i, arg in enumerate(node.args.args):
                default_index = i - (num_args - num_defaults)

                if default_index >= 0:
                    args[arg.arg] = ast.unparse(node.args.defaults[default_index])  # Default value exists
                else:
                    args[arg.arg] = None
                continue
           
            num_inputs = len(args)
            
            return_vars = []
            for stmt in node.body:
                if isinstance(stmt, ast.Return):
                    if isinstance(stmt.value, ast.Name):
                        return_vars.append(stmt.value.id)
                    elif isinstance(stmt.value, ast.Tuple):
                        return_vars.extend(elt.id for elt in stmt.value.elts if isinstance(elt, ast.Name))
            
            return {
                'inputs': num_inputs,
                'outputs': len(return_vars),
                'inputNames': args,
                'outputNames': return_vars
            }
    
    return None