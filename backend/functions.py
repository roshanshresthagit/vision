import base64
import io
import json
import cv2
import numpy as np
from PIL import Image

def add(a,b):
    sum = a+b
    return sum

def sub(a,b):
    subtract = a-b
    return subtract

def multiply(a,b):
    multiplication = a*b
    return multiplication


def load_image(image_path):
    """Load an image from the given path and return it."""
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found at the specified path.")
    return image


def resize_image(image: np.ndarray, dimension_of_image=(640,640)) -> np.ndarray:
    if image is None:
        print("Error: Provided image is None.")
        return None
    resized_image = cv2.resize(image, dimension_of_image)
    return resized_image


def convert_to_color_image(image):
    color_image = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
    return color_image


def convert_to_grayscale_image(image):
    print("hello i am under the water", type(image))
    image=np.array(image)
    # color_image = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print("converted")
    return gray_image

def get_contour_centroid(contour:np.ndarray):
    """Return the centroid (x, y) of a contour."""
    if not contour:
        return None
    contour = np.array(contour, dtype=np.int32)
    moments = cv2.moments(contour)
    if moments["m00"] == 0:
        return None
    cx = int(moments["m10"] / moments["m00"])
    cy = int(moments["m01"] / moments["m00"])
    center =(cx,cy)
    return center

def threshold_image(image, lower_th=120, upper_th=255):
    """Apply thresholding to the given image using lower and upper threshold values."""
    _, thresholded_image = cv2.threshold(image, lower_th, upper_th, cv2.THRESH_BINARY)
    # kernel_size=5
    # kernel = np.ones((kernel_size, kernel_size), np.uint8)
    
    # Apply Dilation
    # dilation = cv2.dilate(thresholded_image, kernel, iterations=1)
    # _, binary_image = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)
    # thresholded_image 
    return thresholded_image

def find_contours(image,retrival_mode=cv2.RETR_TREE, approximation_method=cv2.CHAIN_APPROX_SIMPLE):
    """Find contours in the given thresholded image and return contours as a list."""
    
    contours, _ = cv2.findContours(image, retrival_mode, approximation_method)
    contours_serializable = [c.tolist() for c in contours]


    if not contours:
        print("No contours found.")
        return []

    return contours_serializable


def get_contour_area(contour):
    """Return the area of a contour."""
    if not contour:
        return 0
    contour = np.array(contour, dtype=np.int32)
    area = cv2.contourArea(contour)
    return area


#for all contours
def get_max_area(contours):
    print("it hsere in max are")
    """Return the maximum area among given contours."""
    if not contours:
        return 0
    max_value = max(cv2.contourArea(np.array(c, dtype=np.int32)) for c in contours)
    print("max value",type(max_value))
    return int(max_value)



#average area of all contours
def get_average_area(contours):
    print("its here for average area")
    # contours = [np.array(c, dtype=np.int32) for c in contours]
    """Return the average area of given contours."""
    if not contours:
        return 0
    areas = [cv2.contourArea(np.array(c, dtype=np.int32)) for c in contours]
    print("here the areas",areas)
    average_area = sum(areas) / len(areas)
    return average_area




def get_largest_contour(contours):
    if not contours or len(contours) < 2:
        print("Not enough contours to find the second largest.")
        return None, None  # Return None if there aren't at least two contours

    # Convert list to np.ndarray
    contours = [np.array(c, dtype=np.int32) for c in contours]

    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    largest_contour = contours[0]
    second_largest_contour = contours[1]

    print(f"Largest contour area: {cv2.contourArea(largest_contour)}")
    print(f"Second largest contour area: {cv2.contourArea(second_largest_contour)}")

    # Convert contours back to a serializable format (lists)
    largest_contour = largest_contour.tolist()
    second_largest_contour = second_largest_contour.tolist()

    return  second_largest_contour



def process_contours(contours: np.ndarray):
    contours=[np.array(c, dtype=np.int32) for c in contours]
    result = []
    
    for contour in contours:
        moments = cv2.moments(contour)
        if moments["m00"] != 0:
            center_x = int(moments["m10"] / moments["m00"])
            center_y = int(moments["m01"] / moments["m00"])
        else:
            center_x, center_y = 0, 0
        
        distances = [np.linalg.norm(point - np.array([center_x, center_y])) for point in contour[:, 0]]
        min_radius = min(distances) if distances else 0
        max_radius = max(distances) if distances else 0
        
        result.append({
            "center": [center_x, center_y],
            "min_radius": min_radius,
            "max_radius": max_radius,
            "contour": contour.tolist()
        })
    
    with open("all_contour_data.json", "w") as f:
        json.dump(result, f, indent=4)


def draw_contours(image, contour_data, color_to_draw=(0,255,0)):

    """Draw all contours on the given image and return the plotted image."""
    if not contour_data or len(contour_data) == 0:
        print("No contour provided.")
        return image

    # Convert list of contours to NumPy arrays if necessary
    contours = [np.array(c, dtype=np.int32) for c in contour_data]

    # Copy image before drawing
    contour_image = image.copy()
    # if len(contour_image.shape) == 2:  # Grayscale image (1 channel)
    #     contour_image = cv2.cvtColor(contour_image, cv2.COLOR_GRAY2BGR)

    # Draw all contours on the image
    cv2.drawContours(contour_image, contours, -1, color_to_draw, 1)  
    cv2.imwrite("image.jpg",contour_image)

    return contour_image


