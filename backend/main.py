import inspect
import json
import cv2
from fastapi import FastAPI, HTTPException
import numpy as np
from pydantic import BaseModel
from typing import List, Any
import functions as function
from fastapi.middleware.cors import CORSMiddleware


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
