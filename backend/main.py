import json
import base64
import asyncio
import inspect
import functions, imageFiltering, colorSpaceOperations
import numpy as np
from io import BytesIO
from pydantic import BaseModel
from typing import Dict, List, Any, Union
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, Request
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
from dic_gen import get_class_info

# List of modules containing functions to be exposed
MODULES = [functions, imageFiltering, colorSpaceOperations]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Node(BaseModel):
    id: str
    type: str  
    value: Any = None
    data: Dict[str, Any] = {}

class Edge(BaseModel):
    source: str
    target: str

class FlowRequest(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
    inputValues: Dict[str, Any] = {}


def decode_base64_image(base64_string: str) -> np.ndarray:
    """Decode base64 image string to numpy array"""
    if base64_string.startswith("data:image"):
        base64_string = base64_string.split(",")[1]
    img_bytes = base64.b64decode(base64_string)
    img = Image.open(BytesIO(img_bytes))
    return np.array(img)

def encode_to_base64(value: Any) -> str:
    """Encode various types to base64 strings"""
    if isinstance(value, np.ndarray):
        image = Image.fromarray(value)
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return "data:image/jpeg;base64," + base64.b64encode(buffered.getvalue()).decode()
    elif isinstance(value, (int, float, str)):
        return str(value)
    return json.dumps(value)

def find_function_handler(func_name: str) -> tuple[callable, bool]:
    """Search for a function across all modules and return its handler and whether it's a class method"""
    for module in MODULES:
        for name, obj in vars(module).items():
            if inspect.isclass(obj):
                # Search for the method in the class
                if func_name in vars(obj):
                    method = getattr(obj, func_name)
                    if callable(method):
                        return method, True  # It's a class method
            elif callable(obj) and name == func_name:
                return obj, False  # It's a standalone function
    return None, False

@app.post("/execute_flow")
async def execute_flow(request: Request):
    data = await request.json()
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    inputValues = data.get("inputValues", {})

    node_values = dict(inputValues)
    processed_nodes = set()

    edge_map = {}
    for edge in edges:
        edge_map.setdefault(edge["target"], []).append(edge["source"])

    async def flow_processor():
        pending_edges = list(edges)

        async def process_function_node(node_id: str):
            if node_id in processed_nodes:
                return

            node = next((n for n in nodes if n["id"] == node_id), None)
            if not node or node["type"] != "functionNode":
                return

            input_sources = edge_map.get(node_id, [])
            input_values = []
            for src_id in input_sources:
                if src_id not in node_values:
                    src_node = next((n for n in nodes if n["id"] == src_id), None)
                    if src_node and src_node["type"] == "functionNode":
                        await process_function_node(src_id)
                    elif src_node and src_node["type"] in ["inputNode","imageInputNode"]:
                        node_values[src_id] = inputValues.get(src_id)

                val = node_values.get(src_id)
                if isinstance(val, str) and val.startswith("data:image"):
                    val = decode_base64_image(val)
                input_values.append(val)

            if any(val is None for val in input_values):
                return

            func_name = node["data"].get("func")
            func_handler, is_class_method = find_function_handler(func_name)

            if func_handler:
                try:
                    if is_class_method:
                        # Get the class that contains this method
                        cls = next(
                            obj for module in MODULES
                            for name, obj in vars(module).items()
                            if inspect.isclass(obj) and func_name in vars(obj)
                        )
                        instance = cls()
                        result = func_handler(instance, *input_values)
                    else:
                        # It's a standalone function
                        result = func_handler(*input_values)
                    
                    node_values[node_id] = result
                except Exception as e:
                    print(f"Error executing {func_name}: {str(e)}")
                    node_values[node_id] = None
            else:
                node_values[node_id] = None

            processed_nodes.add(node_id)

        try:
            while pending_edges:
                to_remove = []
                for edge in pending_edges:
                    target_node = next((n for n in nodes if n["id"] == edge["target"]), None)
                    if target_node and target_node["type"] == "resultNode":
                        source_id = edge["source"]
                        source_node = next((n for n in nodes if n["id"] == source_id), None)
                        if source_node and source_node["type"] == "functionNode":
                            await process_function_node(source_id)

                        result_value = encode_to_base64(node_values.get(source_id, None))

                        response_data = json.dumps({
                            "resultNode": edge["target"],
                            "value": result_value
                        })
                        yield response_data + "\n"
                        to_remove.append(edge)

                for edge in to_remove:
                    pending_edges.remove(edge)
                
                await asyncio.sleep(0.1)
                    
            yield json.dumps({"message": "All results processed"}) + "\n"

        except Exception as e:
            yield json.dumps({"error": str(e)}) + "\n"

    return StreamingResponse(flow_processor(), media_type="application/json")

@app.get("/function_dict")
async def get_function_json():
    """Get detailed function dictionary from all modules"""
    try:
        function_dict = get_class_info(MODULES, islist=False)
        return function_dict
    except Exception as e: 
        return {"error": str(e)}
    
@app.get("/function_list")
async def get_function_list_json():
    """Get simplified function list from all modules"""
    try:
        function_list = get_class_info(MODULES, islist=True)
        return function_list
    except Exception as e:
        return {"error": str(e)}

@app.get("/get_functions")
async def get_functions():
    """Get source code of all functions from all modules"""
    function_dict = {}
    for module in MODULES:
        module_name = module.__name__
        function_dict[module_name] = {
            name: inspect.getsource(obj)
            for name, obj in vars(module).items()
            if callable(obj) and not name.startswith('_')
        }
    return function_dict