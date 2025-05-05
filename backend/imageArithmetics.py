import cv2
import numpy as np


class ImageArithmetic:
    def __init__(self):
        """Initializes the ImageArithmetic class."""
        pass

    def imageAddition(self, image1, image2):
        """
        Function: Image Addition
        Description: Adds two images pixel-wise.
        Input: image1 (np.ndarray), image2 (np.ndarray)
        Output: Added image (np.ndarray)
        """
        added_image = cv2.add(image1, image2)
        return added_image

    def imageSubtraction(self, image1, image2):
        """
        Function: Image Subtraction
        Description: Subtracts the second image from the first image pixel-wise.
        Input: image1 (np.ndarray), image2 (np.ndarray)
        Output: Subtracted image (np.ndarray)
        """
        subtracted_image = cv2.subtract(image1, image2)
        return subtracted_image

    def imageBitwiseAnd(self, image1, image2):
        """
        Function: Bitwise AND
        Description: Performs bitwise AND operation between two images.
        Input: image1 (np.ndarray), image2 (np.ndarray)
        Output: Bitwise AND image (np.ndarray)
        """
        and_image = cv2.bitwise_and(image1, image2)
        return and_image

    def imageBitwiseOr(self, image1, image2):
        """
        Function: Bitwise OR
        Description: Performs bitwise OR operation between two images.
        Input: image1 (np.ndarray), image2 (np.ndarray)
        Output: Bitwise OR image (np.ndarray)
        """
        or_image = cv2.bitwise_or(image1, image2)
        return or_image

    def imageBitwiseXor(self, image1, image2):
        """
        Function: Bitwise XOR
        Description: Performs bitwise XOR operation between two images.
        Input: image1 (np.ndarray), image2 (np.ndarray)
        Output: Bitwise XOR image (np.ndarray)
        """
        xor_image = cv2.bitwise_xor(image1, image2)
        return xor_image

    def imageBitwiseNot(self, image1):
        """
        Function: Bitwise NOT
        Description: Inverts all the bits of the image.
        Input: image1 (np.ndarray)
        Output: Bitwise NOT image (np.ndarray)
        """
        inverted_image = cv2.bitwise_not(image1)
        return inverted_image

    def imageBlending(self, image1, image2, alpha=0.5):
        """
        Function: Image Blending
        Description: Blends two images using weighted addition.
        Input: image1 (np.ndarray), image2 (np.ndarray), alpha (float)
        Output: Blended image (np.ndarray)
        """
        blended_image = cv2.addWeighted(image1, alpha, image2, 1 - alpha, 0)
        return blended_image

    def imageBackgroundSubtraction(self, image1):
        """
        Function: Background Subtraction
        Description: Subtracts image from a black background using absolute difference.
        Input: image1 (np.ndarray)
        Output: Foreground image (np.ndarray)
        """
        bg = np.zeros_like(image1)
        foreground_image = cv2.absdiff(image1, bg)
        return foreground_image
