import cv2
import numpy as np

class ComputerVision:
    pass
    
class ImageProcessing(ComputerVision):
    def __init__(self):
        super().__init__()
    
    def load_image( image_path):
        """Load an image from the given path and return it."""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found at the specified path.")
        return image


    def resize_image( image: np.ndarray, dimension_of_image=(640,640)) -> np.ndarray:
        if image is None:
            print("Error: Provided image is None.")
            return None
        resized_image = cv2.resize(image, dimension_of_image)
        return resized_image

 
    def convert_to_color_image( image):
        color_image = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
        return color_image


    def convert_to_grayscale_image( image):
        print("hello i am under the water", type(image))
        image=np.array(image)
        # color_image = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("converted")
        
        return gray_image
    
class Threshold(ImageProcessing):
    def __init__(self):
        super().__init__()
    
    def binary_threshold_image( image, lower_th=120, upper_th=255):
        """Apply thresholding to the given image using lower and upper threshold values."""
        _, thresholded_image = cv2.threshold(image, lower_th, upper_th, cv2.THRESH_BINARY)

        return thresholded_image
    
    def inv_threshold_image( image, lower_th=120, upper_th=255):
        """Apply thresholding to the given image using lower and upper threshold values."""
        _, thresholded_image = cv2.threshold(image, lower_th, upper_th, cv2.THRESH_BINARY_INV)

        return thresholded_image
    
class Arithmetic(ComputerVision):
    def __init__(self):
        super().__init__()
        
    def add(self,a,b):
        sum = a+b
        return sum

    def sub( a,b):
        subtract = a-b
        return subtract

    def multiply( a,b):
        multiplication = a*b
        return multiplication

