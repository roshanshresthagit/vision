import asyncio
import base64
import inspect
from io import BytesIO
import json
import cv2
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
import numpy as np
from pydantic import BaseModel
from typing import Dict, List, Any, Optional

import functions as function
from fastapi.middleware.cors import CORSMiddleware
from camera.data_structure.event_bus import EventBus
from camera.data_structure.DataStore import DataStore
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from camera.get_image import CAMERA
from PIL import Image



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*",],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

# Define a class for input data
class NodeData(BaseModel):
    type: str
    func: str
    inputs: List[Any]  

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


flow_data = {}

def decode_base64_image(base64_string):
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

@app.post("/start_flow")
async def start_flow(data: dict):
    global flow_data
    flow_data = {
        "nodes": data.get("nodes", []),
        "edges": data.get("edges", []),
        "inputValues": data.get("inputValues", {})
    }
    return {"status": "Flow data received"}

@app.get("/execute_flow")
async def execute_flow():
    nodes = flow_data.get("nodes", [])
    edges = flow_data.get("edges", [])
    inputValues = flow_data.get("inputValues", {})

    node_values = dict(inputValues)
    processed_nodes = set()

    edge_map = {}
    reverse_edge_map = {}
    for edge in edges:
        edge_map.setdefault(edge["target"], []).append(edge["source"])
        reverse_edge_map.setdefault(edge["source"], []).append(edge["target"])

    async def flow_processor():
        pending_edges = list(edges)  # We'll pop edges as we send results

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
                    elif src_node and src_node["type"] == "inputNode":
                        node_values[src_id] = inputValues.get(src_id)

                val = node_values.get(src_id)
                if isinstance(val, str) and val.startswith("data:image"):
                    val = decode_base64_image(val)
                input_values.append(val)

            if any(val is None for val in input_values):
                return

            func_name = node["data"].get("func")
            if func_name in function_handlers:
                try:
                    print(function_handlers[func_name])
                    result = function_handlers[func_name](*input_values)
                    print("result",result)
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

                # Remove processed result edges
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
        with open("function_dictonary.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except Exception as e: 
        return {"error": str(e)}
    


@app.get("/function_list")
async def get_function_list_json():
    try:
        with open("function_names.json","r",encoding="utf-8") as file:
            data=json.load(file)
        return data
    except Exception as e:
        return {"error": str(e)}


function_handlers = {
    "add": function.add,
    "sub": function.sub,
    "multiply": function.multiply,
    "load_image": function.load_image,
    "convert_to_grayscale_image": function.convert_to_grayscale_image,
    "find_contours": function.find_contours,
    "get_largest_contour": function.get_largest_contour,
    "threshold_image": function.threshold_image,
    "draw_contours": function.draw_contours,
    "convert_to_color_image": function.convert_to_color_image,
    "get_average_area": function.get_average_area,
    "get_max_area":function.get_max_area,
    "process_contours":function.process_contours,


}

#gets all used function code form function.py########
def get_function_code(func):
    return inspect.getsource(func)

@app.get("/get_functions")
async def get_functions():
    function_dict = {
        "add": get_function_code(function.add),
        "sub": get_function_code(function.sub),
        "convert_to_grayscale_image": get_function_code(function.convert_to_grayscale_image),
        "find_contours":get_function_code(function.find_contours),
        "get_largest_contour":get_function_code(function.get_largest_contour),
        "threshold_image": get_function_code(function.threshold_image),
    }
    return function_dict


# Endpoint for executing the function based on type and inputs
@app.post("/execute")
async def execute_function(data: NodeData):
    print("its here")
    if data.func not in function_handlers:
        raise HTTPException(status_code=400, detail="Invalid function name")

    func = function_handlers[data.func]
    data111 = json.dumps(data.inputs, indent=2)

    # print("hhdhhdhdhdh",data)
    with open("image.json", "w") as file:
        file.write(str(data111))
    try:
        result = func(*data.inputs) 
        return {"result": result}
    except TypeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input arguments: {str(e)}")
    

################################################## for live camera operations #####################################
obj = CAMERA()
event_bus = EventBus()
datastore = DataStore()


class Widget(BaseModel):
    key: str
    value: str | int


# Store widgets in a dictionary
widgets_dict = {}

# Initialize shared state
app.state.canvas_data = []


def get_canvas_data():
    """Dependency to access the canvas data."""
    return app.state.canvas_data


@app.post("/set_widget")
async def set_display_widget(widget: Widget):
    try:
        print(f"Setting widget: key={widget.key}, value={widget.value}")  # Log the data
        widgets_dict[widget.key] = widget.value
        return {"message": f"Widget {widget.key} set successfully", "data": widgets_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error setting widget: {str(e)}")

@app.get("/get_widget")
async def get_display_widget():
    try:
        winId = widgets_dict.get('widgetDisplay')
        if not winId:
            raise HTTPException(status_code=404, detail="widgetDisplay not found in widgets_dict")
        return {"widgetDisplay": winId}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching widget: {str(e)}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, canvas_data: list = Depends(get_canvas_data)):
    await websocket.accept()
    print("Client connected")
    try:
        while True:
            processed_image = obj.get_capture_image()
            # numArray = testing_function(processed_image, event_bus)
            print("Using canvas data:", canvas_data)

            if processed_image is None:
                continue
            for funct in canvas_data:
                event_bus.emit(funct['funcName'],)
            _, buffer = cv2.imencode('.jpg', processed_image)
            frame_base64 = base64.b64encode(buffer).decode("utf-8")
            
            # Send the encoded image through the WebSocket
            await websocket.send_text(frame_base64)
            if obj.g_bExit == True:
                break
            
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {str(e)}")


@app.get("/enum")
async def enum_device():
    try:
        obj.enum_devices()
        return {"message": "Device Found."}
        
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error enumerating devices: {str(e)}")

    
@app.get("/open")
async def open_camera(): 
    try:
        obj.open_device(nConnectionNum=0)    
        return {"message": "Camera opened successfully."}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error opening camera: {str(e)}")

@app.get("/grab")
async def start_capturing():
    try: 
        obj.start_grabbing()
        
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error capturing: {str(e)}")
    
@app.get("/close")
async def close_camera():
    try:
        obj.close_device()
        return {"message": "Camera closed successfully."}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error closing camera: {str(e)}")