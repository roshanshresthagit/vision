import cv2
import numpy as np
from ultralytics import YOLO


class ComputerVision:
    pass
    
class ImageProcessing(ComputerVision):
    def __init__(self):
        super().__init__()
    
    def load_image( self,image_path):
        """Load an image from the given path and return it."""
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Image not found at the specified path.")
            return image
        except Exception as e:
            return ("this error occure", e)




    def resize_image(self, image: np.ndarray, dimension_of_image=(640,640)) -> np.ndarray:
        try:
            if image is None:
                print("Error: Provided image is None.")
                return None
            resized_image = cv2.resize(image, dimension_of_image)
            return resized_image
        except Exception as e:
            return ("this error occure", e)

    def convert_to_color_image(self, image):
        try:
            color_image = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
            return color_image
        except Exception as e:
            return ("this error occure", e)


    def convert_to_grayscale_image(self, image):
        try:
            image=np.array(image)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return gray_image
        except Exception as e:
            return ("this error occure", e)
    
class Threshold(ImageProcessing):
    def __init__(self):
        super().__init__()
    
    def binary_threshold_image(self,image, lower_th=120, upper_th=255):
        """Apply thresholding to the given image using lower and upper threshold values."""
        try:
            _, thresholded_image = cv2.threshold(image, lower_th, upper_th, cv2.THRESH_BINARY)
            return thresholded_image
        except Exception as e:
            return ("this error occure", e)
    
    def inv_threshold_image(self,image, lower_th=120, upper_th=255):
        """Apply thresholding to the given image using lower and upper threshold values."""
        try:
            _, thresholded_image = cv2.threshold(image, lower_th, upper_th, cv2.THRESH_BINARY_INV)
            return thresholded_image
        except Exception as e:
            return ("this error occure", e)


class Arithmetic():
    def __init__(self):
        super().__init__()
    
    def add(self,number_1, number_2):
        try:
            sum = number_1+number_2
            return sum
        except Exception as e:
            return ("this error occure", e)

    def sub( self,number_1, number_2):
        try:
            subtract = number_1-number_2
            return subtract
        except Exception as e:
            return ("this error occure", e)

    def multiply(self, number_1, number_2):
        try:
            multiplication = number_1*number_2
            return multiplication
        except Exception as e:
            return ("this error occure", e)

class Calculas(Arithmetic):
    def __init__(self):
        super().__init__()
    
    def divide(self,number_1, number_2):
        try:
            if number_2 == 0:
                raise ValueError("Cannot divide by zero")
            division = number_1/number_2
            return division
        except:
            return("something went wrong")

    def modulus(self, number_1, number_2):
        try:
            modulus = number_1%number_2
            return modulus
        except Exception as e:
            return ("this error occure", e)

    def power(self, number_1, number_2):
        try:
            power = number_1**number_2
            return power
        except Exception as e:
            return ("this error occure", e)

    def floor_division(self, number_1, number_2):
        try:
            floor_division = number_1//number_2
            return floor_division
        except Exception as e:
            return ("this error occure", e)

class YoloDetection():
    def __init__(self):
        super().__init__()

    def detect_objects(self,model_name, image):
        try:
            model = YOLO(model_name)
            if isinstance(image, str):
                image = cv2.imread(image)
                if image is None:
                    raise ValueError(f"Could not load image from path: {image}")
                
            results = model(image)
            annotated_image = results[0].plot()
            return annotated_image
        except Exception as e:
            return ("this error occure", e)