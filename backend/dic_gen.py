import ast
import inspect

#### function to extract the source code's name, args, inputs and outputs.
def parse_function(source_code):
    """Parse a function's source code and extract its name, arguments, inputs and outputs"""
    tree = ast.parse(source_code.lstrip())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args = {}
            arguments = node.args.args
            num_defaults = len(node.args.defaults)

            non_self_args = [arg for arg in arguments if arg.arg != 'self']
            num_inputs = len(non_self_args)
            
            for i, arg in enumerate(non_self_args):
                default_index = i - (num_inputs - num_defaults)

                if default_index >= 0:
                    args[arg.arg] = ast.unparse(node.args.defaults[default_index])  # Default value exists
                else:
                    args[arg.arg] = None
                continue
           
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

def get_class_list(module):
    classes = {name:{
                    'parents':[parent.__name__
                        for parent in obj.__bases__ 
                        if parent.__name__ != 'object'] or None,
                    'methods':{func_name:parse_function(inspect.getsource(func_obj))
                        for func_name, func_obj in vars(obj).items()
                        if callable(func_obj) and func_name not in
                        ('__dict__', '__doc__', '__init__', '__module__', '__weakref__')} or None
                    }
        for name, obj in vars(module).items()
        if inspect.isclass(obj) and obj.__module__ == module.__name__ 
        }
    
    return classes

def get_class_dict(module):
    classes = {name:{
                    'parents':[parent.__name__
                        for parent in obj.__bases__ 
                        if parent.__name__ != 'object'] or None,
                    'methods':[{
                        'id': func_name,
                        'label': func_name.capitalize(),
                        'func': func_name
                        }
                            for func_name, func_obj in vars(obj).items()
                            if callable(func_obj) and func_name not in
                            ('__dict__', '__doc__', '__init__', '__module__', '__weakref__') or None]
                    }
            for name, obj in vars(module).items()
            if inspect.isclass(obj) and obj.__module__ == module.__name__ 
            }
    
    return classes

def get_class_info(module, islist = False):
    classes = get_class_dict(module) if islist else get_class_list(module)
    # Recursive function to build hierarchical structure
    def build_tree(node):
        children = {}
        for name, value in classes.items():
            # print(child, parents['parents'])
            if value['parents'] is not None and node in value['parents']:
                children[name] = {
                    'children':build_tree(name),
                    'methods':value['methods']
                }
        return children or None  # Return None for leaf nodes

    
    
    handler = {name:{
                    'children' : build_tree(name),
                    'methods' : classes[name]['methods']
                    }       
               for name, obj in vars(module).items()
               if inspect.isclass(obj) and obj.__module__ == module.__name__
               and not any(base.__module__ == module.__name__ for base in obj.__bases__)
               }

    return handler