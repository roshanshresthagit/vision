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

@image_preprocessing_decorator
def find_contours(image):
    """Find contours in the given thresholded image and return contours as a list."""
    #contours is a np.ndarray
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        print("No contours found.")
        return []

    contours_serializable = [c.tolist() for c in contours]

    

    return contours_serializable


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

@image_preprocessing_decorator
def draw_contours(image, contour_data):
    """Draw the largest contour on the given image and return the plotted image."""

    if not contour_data or len(contour_data) == 0:
        print("No contour provided.")
        return image

    # Convert list back to NumPy array
    contour = np.array(contour_data, dtype=np.int32)

    # Ensure contour has the correct shape (N, 1, 2)
    if len(contour.shape) == 2:
        contour = contour.reshape(-1, 1, 2)

    # Wrap the single contour in a list
    contours = [contour]

    # Copy image before drawing
    contour_image = image.copy()

    # Draw contour on image
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)

    return contour_image