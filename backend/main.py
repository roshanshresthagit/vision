import json
import base64
import asyncio
import inspect
from types import FunctionType
from ultralytics import YOLO
from functions import  (imageFiltering, colorSpaceOperations, 
                        geometric, calculation, contourAnalysis, 
                        imageArithmetics, imageEnhancement, visualization, 
                        roi,ArithmeticOperations, template_matching,ModelOperations
                        )
import numpy as np
from io import BytesIO
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi import FastAPI, HTTPException, Request
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
from dic_gen import get_class_info


# List of modules containing functions to be exposed
MODULES = [
    ArithmeticOperations,
    imageFiltering,
    colorSpaceOperations,
    geometric,
    calculation,
    contourAnalysis,
    imageEnhancement,
    imageArithmetics,
    visualization,
    roi,
    template_matching,
    ModelOperations
]


NODE_TYPE_FUNCTION = "functionNode"
NODE_TYPE_INPUT = "inputNode"
NODE_TYPE_RESULT = "resultNode"
NODE_TYPE_IMAGE_INPUT = "imageInputNode"
NODE_TYPE_ROI_INPUT = "roiInputNode"
NODE_TYPE_DETECTION_RESULT = "detectionResultNode"

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
    targetHandle: Optional[str] = None

class DetectionRequest(BaseModel):
    model_name: str
    image: str


##########-----------Error Handling-----------###########
class ErrorResponse(BaseModel):
    error: str
    node_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class ProcessingError(Exception):
    def __init__(self, message: str, node_id: Optional[str] = None):
        self.node_id = node_id
        self.message = message
        super().__init__(message)


@app.exception_handler(ProcessingError)
async def processing_error_handler(request: Request, exc: ProcessingError):
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error=exc.message,
            node_id=exc.node_id
        ).dict()
    )

@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            details={"type": type(exc).__name__}
        ).dict()
    )

def decode_base64_image(base64_string: str) -> np.ndarray:
    """Decode base64 image string to numpy array"""
    try:
        if base64_string.startswith("data:image"):
            base64_string = base64_string.split(",")[1]
        img_bytes = base64.b64decode(base64_string)
        img = Image.open(BytesIO(img_bytes))
        return np.array(img)
    except Exception:
        raise ProcessingError("Invalid Image data")


def processing_to_send_result(value: Any) -> str:
    """Encode various types to base64 or JSON strings"""
    try:
        if isinstance(value, np.ndarray):
            image = Image.fromarray(value)
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            return "data:image/jpeg;base64," + base64.b64encode(buffered.getvalue()).decode()

        if isinstance(value, (int, float, str)):
            return str(value)

        if isinstance(value, (list, dict)):
            def convert(item):
                if isinstance(item, np.ndarray):
                    return item.tolist()
                return item

            if isinstance(value, list):
                converted = [convert(i) for i in value]
            else:
                converted = {k: convert(v) for k, v in value.items()}
                
            return json.dumps(converted)

        return str(value)
    except Exception:
        raise ProcessingError("Failed to convert result")

@app.post("/execute_flow")
async def execute_flow(request: Request):
    try:
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
                if not node or node["type"] != NODE_TYPE_FUNCTION:
                    return
                
                incoming_edges = [e for e in edges if e["target"] == node_id]
                

                #### processing input ######
                input_dict = {}
                for edge in incoming_edges:
                    src_id = edge["source"]
                    target_handle = edge.get("targetHandle")

                    if src_id not in node_values:
                        src_node = next((n for n in nodes if n["id"] == src_id), None)
                        if src_node and src_node.type == NODE_TYPE_FUNCTION:
                            await process_function_node(src_id)
                        elif src_node and src_node.type in [NODE_TYPE_INPUT,NODE_TYPE_IMAGE_INPUT,NODE_TYPE_DETECTION_RESULT]:
                            node_values[src_id] = inputValues.get(src_id)

                    val = node_values.get(src_id)
                    if isinstance(val, str) and val.startswith("data:image"):
                        val = decode_base64_image(val)

                    if target_handle:
                        input_dict[target_handle] = val
                    else:
                        input_dict[src_id] = val

                if not input_dict:
                    return

                func_name = node["data"].get("func")
                found = False
                instance_cache = {}
                for module in MODULES:
                    for name, obj in vars(module).items():
                        if inspect.isclass(obj) and func_name in vars(obj):
                            try:
                                method = getattr(obj, func_name)
                                if callable(method):
                                    sig = inspect.signature(method)
                                    params = list(sig.parameters.keys())
                                    args = [input_dict.get(p) for p in params if p != "self"]

                                    if obj not in instance_cache:
                                        instance_cache[obj] = obj() 
                                    instance = instance_cache[obj]

                                    result = method(instance, *args)
                                    node_values[node_id] = result
                                    
                                    found = True
                                    break
                            except Exception as e:
                                print(f"Error processing {func_name}: {e}")
                                node_values[node_id] = None
                                found = True
                                break
                        elif callable(obj) and name == func_name:
                            try:
                                sig = inspect.signature(obj)
                                params = list(sig.parameters.keys())
                                args = [input_dict.get(p) for p in params]
                                result = obj(*args)
                                node_values[node_id] = result
                                found = True
                                break
                            except Exception as e:
                                print(f"Error processing {func_name}: {e}")
                                node_values[node_id] = None
                                found = True
                                break
                    if found:
                        break

                processed_nodes.add(node_id)

            try:
                while pending_edges:
                    to_remove = []
                    for edge in pending_edges:
                        target_node = next(
                            (n for n in nodes if n["id"] == edge["target"]), None
                        )
                        if target_node and target_node["type"] in [NODE_TYPE_RESULT, NODE_TYPE_ROI_INPUT]:
                            source_id = edge["source"]
                            source_node = next(
                                (n for n in nodes if n["id"] == source_id), None
                            )
                            if source_node and source_node["type"] == NODE_TYPE_FUNCTION:
                                await process_function_node(source_id)
                            result_value = processing_to_send_result(
                                node_values.get(source_id, None)
                            )
                            if target_node["type"] == NODE_TYPE_ROI_INPUT:
                            
                                response_data = json.dumps(
                                {NODE_TYPE_ROI_INPUT: edge["target"], "value": result_value},
                                )
                            else:
                                response_data = json.dumps(
                                    {NODE_TYPE_RESULT: edge["target"], "value": result_value},
                                )
                            yield response_data + "\n"
                            to_remove.append(edge)

                    for edge in to_remove:
                        pending_edges.remove(edge)

                    await asyncio.sleep(0.1)

                yield json.dumps({"message": "All results processed"}) + "\n"

            except Exception as e:
                yield json.dumps({"error": str(e)}) + "\n"

        return StreamingResponse(flow_processor(), media_type="application/json")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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

#gets all used function code form function.py########
@app.get("/get_functions")
async def get_functions():
    function_sources = {}
    for module in MODULES:
        module_name = module.__name__
        for name, obj in inspect.getmembers(module):
            if isinstance(obj, FunctionType):
                function_sources[f"{module_name}.{name}"] = inspect.getsource(obj)
            elif inspect.isclass(obj):
                class_name = obj.__name__
                for meth_name, meth_obj in inspect.getmembers(obj, predicate=inspect.isfunction):
                    full_name = f"{module_name}.{class_name}.{meth_name}"
                    try:
                        function_sources[full_name] = inspect.getsource(meth_obj)
                    except TypeError:
                        function_sources[full_name] = f"# Could not retrieve source for {full_name}"
    
    return function_sources


@app.post("/update")
async def update(data: DetectionRequest):
    print("this function was called")
    try:
        # Convert base64 image to numpy array
        image_array = decode_base64_image(data.image)
        return await detect_objects(data.model_name, image_array)
    except Exception as e:
        return {"error": str(e)}



async def detect_objects(model_name, image):
    print("detecting objects")
    model = YOLO(model_name)
    print(model_name, image)
    detected_cakes = {}  # Dictionary to store cake detections
    total_detections = 0
    
    results = model(image, verbose=False)
    for result in results:
        boxes = result.boxes  # Get boxes on regular rectangle format
        for box in boxes:
            total_detections += 1
            # Get box coordinates
            coords = box.xyxy[0].cpu().numpy()  # Get box coordinates in (x1, y1, x2, y2) format
            coords = [int(c) for c in coords]
            
            # Get confidence score
            confidence = float(box.conf[0].cpu().numpy())
            
            # Store detection with simple numbering format
            detected_cakes[f'cake_{total_detections}'] = {
                'confidence': confidence,
                'coordinates': coords.tolist() if hasattr(coords, 'tolist') else coords
            }
    # If no detections were made, return empty dictionary
    if not detected_cakes:
        detected_cakes = {'one': 1, 'two': 2}  # Default response as requested
    print(detected_cakes)
        
    return detected_cakes
