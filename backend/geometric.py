import cv2
import numpy as np

class Geometric:
    def __init__(self):
        pass


class Transformations(Geometric):
    def __init__(self):
       
        super().__init__()
    def affine_transform(self, image, src_points=[[50,50],[200,50],[50,200]], dst_points=[[10,100],[200,50],[100,250]]):
        """
        Function: affine_transform
        Description: Apply an affine transformation to an image.
        Inputs:
            image (ndarray): The input image.
            src_points (list): List of source points.
            dst_points (list): List of destination points.

        Output:
            ndarray: The transformed image.
        """
        M = cv2.getAffineTransform(np.float32(src_points), np.float32(dst_points))
        return cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    def perspective_transform(self, image, src_points, dst_points):
        """
        Function: perspective_transform
        Description: Apply a perspective transformation to an image.
        Inputs:
            image (ndarray): The input image.
            src_points (list): List of source points for the perspective transform.
            dst_points (list): List of destination points for the perspective transform.
        Output:
            ndarray: The transformed image with applied perspective transformation.
        """

        M = cv2.getPerspectiveTransform(np.float32(src_points), np.float32(dst_points))
        return cv2.warpPerspective(image, M, (image.shape[1], image.shape[0]))
    def warp_affine(self, image, src_pts,dst_pts):
        """
        Function: warp_affine
        Description: Apply an affine transformation to an image with the given source and destination points.
        Inputs:
            image (ndarray): The input image.
            src_pts (list): List of source points.
            dst_pts (list): List of destination points.
        Output:
            ndarray: The transformed image with applied affine transformation.
        """
        M = cv2.getAffineTransform(np.float32(src_pts), np.float32(dst_pts))
        return cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    def warp_perspective(self, image, src_pts,dst_pts):
        """
        Function: warp_perspective
        Description: Apply a perspective transformation to an image with the given source and destination points.
        Inputs:
            image (ndarray): The input image.
            src_pts (list): List of source points.
            dst_pts (list): List of destination points.
        Output:
            ndarray: The transformed image with applied perspective transformation.
        """
        M = cv2.getPerspectiveTransform(np.float32(src_pts), np.float32(dst_pts))
        return cv2.warpPerspective(image, M, (image.shape[1], image.shape[0]))
    def rotate(self, image, angle, center=None, scale=1.0):
        """
        Function: Rotate
        Description: Rotate an image by a specified angle around a specified center point.
        Inputs:
            image (ndarray): The input image to be rotated.
            angle (float): The angle in degrees to rotate the image.
            center (tuple, optional): The center of rotation. If None, the image center is used. Defaults to None.
            scale (float, optional): The scale factor for the rotation. Defaults to 1.0.
        Output:
            ndarray: The rotated image.
        """

        (h, w) = image.shape[:2]
        if center is None:
            center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, scale)
        return cv2.warpAffine(image, M, (w, h))
    def translate(self, image, tx=10, ty=10):
        """
        Function: translate
        Description: Translate an image by a specified amount.
        Inputs:
            image (ndarray): The input image to be translated.
            tx (int, optional): The x-coordinate translation amount. Defaults to 10.
            ty (int, optional): The y-coordinate translation amount. Defaults to 10.
        Output:
            ndarray: The translated image.
        """
        M = np.float32([[1, 0, tx], [0, 1, ty]])
        return cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    def flip(self, image, flip_type):
        """
        Function: Flip
        Description: Flip an image either vertically or horizontally based on the specified flip type.
        Inputs:
            image (ndarray): The input image to be flipped.
            flip_type (str): The type of flip to apply. "vertical" for vertical flip, "horizontal" for horizontal flip.
        Output:
            ndarray: The flipped image.
        """

        if flip_type == "vertical":
            return cv2.flip(image, 0)
        elif flip_type == "horizontal":
            return cv2.flip(image, 1)

    def scale(self, image, fx, fy):
        """
        Function: Scale
        Description: Scale an image by specified factors along the x and y axes.
        Inputs:
            image (ndarray): The input image to be scaled.
            fx (float): The scaling factor for the x-axis.
            fy (float): The scaling factor for the y-axis.
        Output:
            ndarray: The scaled image.
        """
        return cv2.resize(image, None, fx=fx, fy=fy, interpolation=cv2.INTER_LINEAR)

class MomentsAndCentroids(Geometric):
    def __init__(self):
        
        super().__init__()

    def raw_moments(self, image):
        """
        Function: raw_moments
        Description: Compute the raw moments of an image.
        Inputs:
            image (ndarray): The input image for which to compute the raw moments.
        Output:
            dict: A dictionary containing the computed raw moments of the image.
        """

        return cv2.moments(image)

    def central_moments(self, image):
        """
        Function: central_moments
        Description: Compute the central moments of an image.
        Inputs:
            image (ndarray): The input image for which to compute the central moments.
        Output:
            dict: A dictionary containing the computed central moments of the image.
        """
        m = cv2.moments(image)
        return {
            'mu20': m['mu20'], 'mu11': m['mu11'], 'mu02': m['mu02'],
            'mu30': m['mu30'], 'mu21': m['mu21'], 'mu12': m['mu12'], 'mu03': m['mu03']
        }

    def hu_moments(self, image):
        """
        Function: hu_moments
        Description: Compute the Hu moments of an image.
        Inputs:
            image (ndarray): The input image for which to compute the Hu moments.
        Output:
            ndarray: A 1D array containing the computed Hu moments of the image.
        """
        m = cv2.moments(image)
        hu = cv2.HuMoments(m).flatten()
        return hu

    def centroid(self, image):
        """
        Function: centroid
        Description: Compute the centroid of an image.
        Inputs:
            image (ndarray): The input image for which to compute the centroid.
        Output:
            tuple: A tuple containing the x and y coordinates of the centroid of the image as integers.
        """
        m = cv2.moments(image)
        if m['m00'] != 0:
            cx = int(m['m10'] / m['m00'])
            cy = int(m['m01'] / m['m00'])
            return (cx, cy)
        else:
            return (0, 0)

    def orientation(self, image):
        """
        Function: orientation
        Description: Compute the orientation of an image.
        Inputs:
            image (ndarray): The input image for which to compute the orientation.
        Output:
            float: The computed orientation of the image in degrees.
        """
        m = cv2.moments(image)
        if m['mu20'] - m['mu02'] != 0:
            angle = 0.5 * np.arctan2(2 * m['mu11'], m['mu20'] - m['mu02'])
            return np.degrees(angle)
        return 0

    def fit_ellipse(self, contour):
        """
        Function: fit_ellipse
        Description: Fit an ellipse to a given contour using the least squares method.
        Inputs:
            contour (ndarray): The input contour to which to fit the ellipse.
        Output:
            tuple: A tuple containing the ellipse parameters (center, axes, angle) as a tuple of tuples.
            If the contour has less than 5 points, None is returned.
        """
        if len(contour) >= 5:
            ellipse = cv2.fitEllipse(contour)
            return ellipse
        else:
            return None

    def bounding_box_center(self, contour):
        """
        Function: bounding_box_center
        Description: Calculate the center of the bounding box for a given contour.
        Inputs:
            contour (ndarray): The input contour for which to compute the bounding box center.
        Output:
            tuple: A tuple representing the (x, y) coordinates of the center of the bounding box.
        """

        x, y, w, h = cv2.boundingRect(contour)
        return (x + w // 2, y + h // 2)