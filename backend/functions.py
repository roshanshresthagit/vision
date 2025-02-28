import base64
import io
import json
import cv2
import numpy as np
from PIL import Image
from decrotors import image_preprocessing_decorator

def add(a,b):
    print("its here")
    sum = a+b
    print(sum)
    return sum

def sub(a,b):
    print("its here")
    subtract = a+b
    return subtract

def multiply(a,b):
    print("its here")
    subtract = a+b
    return subtract


def load_image(image_path):
    print("image received")
    """Load an image from the given path and return it."""
    # image = cv2.imread(image_path)
    # if image is None:
        # raise ValueError("Image not found at the specified path.")
    # return image

@image_preprocessing_decorator
def convert_to_grayscale(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  
    return gray_image

@image_preprocessing_decorator
def threshold_image(image, lower_th, upper_th):
    print("its here")
    """Apply thresholding to the given image using lower and upper threshold values."""
    _, thresholded_image = cv2.threshold(image, lower_th, upper_th, cv2.THRESH_BINARY)
    return thresholded_image
from json import JSONEncoder
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)
@image_preprocessing_decorator
def find_contours(image):
    
    """Find contours in the given thresholded image and return contours along with their count."""
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours_serializable = [c.tolist() for c in contours]
    # with open("contours.json", "w") as json_file:
    #     json.dump(contours, json_file, indent=4)
    encodedNumpyData = json.dumps(contours, cls=NumpyArrayEncoder)
    print(encodedNumpyData)
    return encodedNumpyData


def get_largest_contour(contours):
    # print(contours)
    print(type(contours),len(contours))
    contours = np.asarray(contours)

    """Find and return the contour with the maximum area."""
    if not contours:
        return None
    maximum = max(contours, key=cv2.contourArea)
    return maximum

def draw_contours(image, contours):
    """Draw contours on the given image and return the plotted image."""
    contour_image = image.copy()
    if contours[0].shape[0] == 1:
        contours=[contours]
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
    return contour_image
