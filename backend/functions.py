import base64
import io
import json
import cv2
import numpy as np
from PIL import Image
from decrotors import image_preprocessing_decorator

def add(a,b,c):
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
    subtract = a*b
    return subtract


def load_image(image_path):
    print("image received")
    """Load an image from the given path and return it."""
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found at the specified path.")
    return image


@image_preprocessing_decorator
def resize_image(image: np.ndarray, dimension_of_image=(640,640)) -> np.ndarray:
    if image is None:
        print("Error: Provided image is None.")
        return None
    resized_image = cv2.resize(image, dimension_of_image)
    return resized_image


@image_preprocessing_decorator
def convert_to_color_image(image):
    color_image = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
    return color_image


@image_preprocessing_decorator
def convert_to_grayscale_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image


@image_preprocessing_decorator
def threshold_image(image, lower_th, upper_th):
    """Apply thresholding to the given image using lower and upper threshold values."""
    _, thresholded_image = cv2.threshold(image, lower_th, upper_th, cv2.THRESH_BINARY)
    # kernel_size=5
    # kernel = np.ones((kernel_size, kernel_size), np.uint8)
    
    # Apply Dilation
    # dilation = cv2.dilate(thresholded_image, kernel, iterations=1)
    # _, binary_image = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)
    # thresholded_image 
    return thresholded_image

@image_preprocessing_decorator
def find_contours(image,retrival_mode=cv2.RETR_TREE, approximation_method=cv2.CHAIN_APPROX_SIMPLE):
    """Find contours in the given thresholded image and return contours as a list."""
    
    contours, _ = cv2.findContours(image, retrival_mode, approximation_method)
    contours_serializable = [c.tolist() for c in contours]


    if not contours:
        print("No contours found.")
        return []

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
def draw_contours(image, contour_data, color_to_draw=(0,255,0)):

    # image = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
    """Draw all contours on the given image and return the plotted image."""

    if not contour_data or len(contour_data) == 0:
        print("No contour provided.")
        return image
    cv2.imwrite("this.jpg",image)

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


