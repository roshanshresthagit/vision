import cv2
import os
class Visualization:
    def __init__(self):
        pass

    def putText(self, image, text="Sample Text", starting_point=(10, 30), font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, color=(255, 0, 0), thickness=2, line_type=cv2.LINE_AA):
        """
            Function: putText
            Description: Draw text on the image with customizable font and style.
            Input: 
                image, text="Sample Text", starting_point=(10, 30), font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, color=(255, 0, 0), thickness=2, line_type=cv2.LINE_AA
            Output: 
                image: The image with the text drawn on it.
        """
        image = cv2.putText(image, text, starting_point, font, font_scale, color, thickness, line_type)
        return image

    def putRectangle(self, image, starting_point=(0, 0), ending_point=(100, 100), color=(255, 0, 0), thickness=2, line_type=cv2.LINE_AA):
        """
            Function: putRectangle
            Description: Draw a rectangle on the image.
            Input: 
                image, starting_point=(0, 0), ending_point=(100, 100), color=(255, 0, 0), thickness=2, line_type=cv2.LINE_AA
            Output: 
                image: The image with the rectangle drawn.
        """
        image = cv2.rectangle(image, starting_point, ending_point, color, thickness, lineType=line_type)
        return image

    def putCircle(self, image, center=(50, 50), radius=20, color=(255, 0, 0), thickness=2, line_type=cv2.LINE_AA):
        """
            Function: putCircle
            Description: Draw a circle on the image.
            Input: 
                image, center=(50, 50), radius=20, color=(255, 0, 0), thickness=2, line_type=cv2.LINE_AA
            Output: 
                image: The image with the circle drawn.
        """
        image = cv2.circle(image, center, radius, color, thickness, lineType=line_type)
        return image

    def putLine(self, image, starting_point=(0, 0), ending_point=(100, 100), color=(255, 0, 0), thickness=2, line_type=cv2.LINE_AA):
        """
            Function: putLine
            Description: Draw a straight line between two points on the image.
            Input: 
                image, starting_point=(0, 0), ending_point=(100, 100), color=(255, 0, 0), thickness=2, line_type=cv2.LINE_AA
            Output: 
                image: The image with the line drawn.
        """
        image = cv2.line(image, starting_point, ending_point, color, thickness, lineType=line_type)
        return image

    def writeImage(self, image, path="output.jpg"):
        """
            Function: writeImage
            Description: Save the image to the specified path. Creates the directory if it doesn't exist.
            Input: 
                image, path="output.jpg"
            Output: 
                None (Image is written to disk).
        """
        dir_name = os.path.dirname(path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        cv2.imwrite(path, image)