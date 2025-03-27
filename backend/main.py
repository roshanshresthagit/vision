import cv2
import json
import base64
import asyncio
import inspect
import functions
import numpy as np
from io import BytesIO
from pydantic import BaseModel
from typing import Dict, List, Any
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, Request
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
from dic_gen import parse_function


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*",],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

class Node(BaseModel):
    id: str
    type: str  # inputNode, functionNode, resultNode
    value: Any = None
    data: Dict[str, Any] = {}

class Edge(BaseModel):
    source: str
    target: str

class FlowRequest(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
    inputValues: Dict[str, Any] = {}


def decode_base64_image(base64_string):
    print("image converted into nparray")
    if base64_string.startswith("data:image"):
        base64_string = base64_string.split(",")[1]
    img_bytes = base64.b64decode(base64_string)
    img = Image.open(BytesIO(img_bytes))
    return np.array(img)

def encode_to_base64(value):
    if isinstance(value, np.ndarray):
        # Convert image to base64
        image = Image.fromarray(value)
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return "data:image/jpeg;base64," + base64.b64encode(buffered.getvalue()).decode()
    elif isinstance(value, (int, float, str)):
        return str(value)
    return json.dumps(value)

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

        async def process_function_node(node_id):
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
                    elif src_node and src_node["type"] == "inputNode" or "imageInputNode":
                        node_values[src_id] = inputValues.get(src_id)

                val = node_values.get(src_id)
                if isinstance(val, str) and val.startswith("data:image"):
                    val = decode_base64_image(val)
                input_values.append(val)

            if any(val is None for val in input_values):
                return

            func_name = node["data"].get("func")
            function_handlers = {name : obj 
                     for name, obj in vars(functions).items() 
                     if callable(obj)}
            if func_name in function_handlers:
                try:
                    result = function_handlers[func_name](*input_values)
                    node_values[node_id] = result
                except Exception:
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

                # Remove processed edges
                for edge in to_remove:
                    pending_edges.remove(edge)
                
                await asyncio.sleep(0.1)
                    
            yield json.dumps({"message": "All results processed"}) + "\n"

        except Exception as e:
            yield json.dumps({"error": str(e)}) + "\n"

    return StreamingResponse(flow_processor(), media_type="application/json")


@app.get("/function_dict")
async def get_function_json():
    try:
        function_dict = {
            name: inspect.getsource(obj)
            for name, obj in vars(functions).items()
            if callable(obj)
        }
        parsed_functions = {
            name: parse_function(source_code)
            for name, source_code in function_dict.items()
        }
        return parsed_functions
    
    except Exception as e: 
        return {"error": str(e)}
    
@app.get("/function_list")
async def get_function_list_json():
    try:
        function_dict = {
            name: inspect.getsource(obj)
            for name, obj in vars(functions).items()
            if callable(obj)
        }
        parsed_functions = {
            name: parse_function(source_code)
            for name, source_code in function_dict.items()
        }
        data = [{'id':func_name, 'label':func_name.capitalize(), 'func':func_name} 
                for func_name in parsed_functions.keys()]
        return data
    
    except Exception as e:
        return {"error": str(e)}



#gets all used function code form function.py########
def get_function_code(func):
    return inspect.getsource(func)

@app.get("/get_functions")
async def get_functions():
    function_dict = {name:inspect.getsource(obj)
                     for name, obj in vars(functions).items()
                     if callable(obj)}

    return function_dict
