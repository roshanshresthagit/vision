import base64
import inspect
import json
import cv2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Any
import functions as function
from fastapi.middleware.cors import CORSMiddleware
from camera.data_structure.event_bus import EventBus
from camera.data_structure.DataStore import DataStore
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends

from camera.get_image import CAMERA



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define a class for input data
class NodeData(BaseModel):
    type: str
    func: str
    inputs: List[Any]  # Accept any type of input




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



# More complex functions can be added here

# Function to map the function name to the actual implementation
function_handlers = {
    "add": function.add,
    "sub": function.sub,
    "multiply": function.multiply,
    "load_image":function.load_image,
    "convert_to_grayscale":function.convert_to_grayscale,
    "find_contours":function.find_contours,
    "get_largest_contour":function.get_largest_contour,
    "threshold_image":function.threshold_image,
    "draw_contours":function.draw_contours,
    # Add more functions as needed
}

def get_function_code(func):
    return inspect.getsource(func)



@app.get("/get_functions")
async def get_functions():
    function_dict = {
        "add": get_function_code(function.add),
        "sub": get_function_code(function.sub),
        "convert_to_grayscale": get_function_code(function.convert_to_grayscale),
        "find_contours":get_function_code(function.find_contours),
        "get_largest_contour":get_function_code(function.get_largest_contour),
        "threshold_image": get_function_code(function.threshold_image),
    }
    return function_dict

# Endpoint for executing the function based on type and inputs
@app.post("/execute")
async def execute_function(data: NodeData):

    if data.func not in function_handlers:
        raise HTTPException(status_code=400, detail="Invalid function name")


    func = function_handlers[data.func]
    data111 = json.dumps(data.inputs, indent=2)

    # print("hhdhhdhdhdh",data)
    with open("image.json", "w") as file:
        file.write(str(data111))
    try:
        print("ttt")
        result = func(*data.inputs) 
        return {"result": result}
    except TypeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input arguments: {str(e)}")
    

##################################################
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
            # Encode the processed image as base64
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