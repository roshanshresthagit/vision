import base64
import io
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
    print("its here",image)
    """Apply thresholding to the given image using lower and upper threshold values."""
    _, thresholded_image = cv2.threshold(image, lower_th, upper_th, cv2.THRESH_BINARY)
    return thresholded_image

def find_contours(image):
    image_data = image["data"]  
    if image_data.startswith("data:image"):
        image_data = image_data.split(',')[1]
    image_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_bytes))
    image_np = np.array(image)

    gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)  
    """Find contours in the given thresholded image and return contours along with their count."""
    contours, _ = cv2.findContours(gray_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour= get_largest_contour(contours)
    second = sorted(contours,  key=cv2.contourArea, reverse= True)
    image=draw_contours(image_np,second[1])
    _, buffer = cv2.imencode('.jpg', image)
    frame_base64 = base64.b64encode(buffer).decode("utf-8")
    return frame_base64

def get_largest_contour(contours):
    """Find and return the contour with the maximum area."""
    if not contours:
        return None

    return max(contours, key=cv2.contourArea)

def draw_contours(image, contours):
    """Draw contours on the given image and return the plotted image."""
    contour_image = image.copy()
    if contours[0].shape[0] == 1:
        contours=[contours]
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
    return contour_image

# Example usage
# if __name__ == "__main__":
#     img_path = "new.jpg"
#     img = load_image(img_path)
#     gray = convert_to_grayscale(img)
#     thresh = threshold_image(img, 100, 255)
#     contours, num_contours = find_contours(thresh)
#     largest_contour = get_largest_contour(contours)
#     print(f"--{largest_contour[0].shape[0]} and {contours[0].shape[0]}--")
#     contour_image = draw_contours(img, largest_contour)
#     print(f"Number of contours found: {num_contours}")
    
#     # Display images (for testing purposes)
#     cv2.imshow("Grayscale Image", gray)
#     cv2.imshow("Thresholded Image", thresh)
#     cv2.imshow("Contour Image", contour_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
