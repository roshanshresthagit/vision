import cv2
import numpy as np


class GeometricOperations:
    def __init__(self):
        pass


class Transformations(GeometricOperations):
    def __init__(self):
        super().__init__()

    def affine_transform(
        self,
        image,
        src_points=[[50, 50], [200, 50], [50, 200]],
        dst_points=[[10, 100], [200, 50], [100, 250]],
    ):
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
        transformed_image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
        return transformed_image

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
        transformed_image = cv2.warpPerspective(
            image, M, (image.shape[1], image.shape[0])
        )
        return transformed_image

    def warp_affine(self, image, src_pts, dst_pts):
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

        transformed_image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
        return transformed_image

    def warp_perspective(self, image, src_pts, dst_pts):
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
        transformed_image = cv2.warpPerspective(
            image, M, (image.shape[1], image.shape[0])
        )
        return transformed_image

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
        transformed_image = cv2.warpAffine(image, M, (w, h))
        return transformed_image

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
        transformed_image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
        return transformed_image

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
            flipped_image = cv2.flip(image, 0)
        elif flip_type == "horizontal":
            flipped_image = cv2.flip(image, 1)
        return flipped_image

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
        scaled_image = cv2.resize(
            image, None, fx=fx, fy=fy, interpolation=cv2.INTER_LINEAR
        )
        return scaled_image


class MomentsAndCentroids(GeometricOperations):
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

        moments = cv2.moments(image)
        return moments

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
        moments = {
            "mu20": m["mu20"],
            "mu11": m["mu11"],
            "mu02": m["mu02"],
            "mu30": m["mu30"],
            "mu21": m["mu21"],
            "mu12": m["mu12"],
            "mu03": m["mu03"],
        }
        return moments

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
        moments = cv2.HuMoments(m).flatten()
        return moments

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
        (cx, cy) = (0, 0)
        if m["m00"] != 0:
            cx = int(m["m10"] / m["m00"])
            cy = int(m["m01"] / m["m00"])
        return (cx, cy)

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
        orient = 0
        if m["mu20"] - m["mu02"] != 0:
            angle = 0.5 * np.arctan2(2 * m["mu11"], m["mu20"] - m["mu02"])
            orient = np.degrees(angle)
        return orient

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
        ellipse = "None"
        if len(contour) >= 5:
            ellipse = cv2.fitEllipse(contour)
        return ellipse

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
        center = (x + w // 2, y + h // 2)
        return center


class Resize(GeometricOperations):
    def __init__(self):
        super().__init__()

    def resize_image(self, image, width, height, interpolation=cv2.INTER_LINEAR):
        """
        Function: resize
        Description: Resize an image to a specified width and height.
        Inputs:
            image (ndarray): The input image to be resized.
            width (int): The desired width of the resized image.
            height (int): The desired height of the resized image.
        Output:
            ndarray: The resized image.
        """
        resized_image = cv2.resize(image, (width, height), interpolation=interpolation)
        return resized_image

    def gaussian_pyramid(self, image, levels):
        """
        Function: gaussian_pyramid
        Description: Generate a Gaussian pyramid of the input image up to a specified number of levels.
        Inputs:
            image (ndarray): The input image for pyramid generation.
            levels (int): The number of levels in the pyramid.
        Output:
            list: A list of images representing the Gaussian pyramid.
        """
        pyramid = [image]
        for _ in range(levels - 1):
            image = cv2.pyrDown(image)
            pyramid.append(image)
        return pyramid

    def laplacian_pyramid(self, image, levels):
        """
        Function: laplacian_pyramid
        Description: Generate a Laplacian pyramid from the input image using Gaussian pyramid decomposition.
        Inputs:
            image (ndarray): The input image for pyramid generation.
            levels (int): The number of levels in the pyramid.
        Output:
            list: A list of images representing the Laplacian pyramid.
        """
        gaussian = self.gaussian_pyramid(image, levels)
        laplacian = []
        for i in range(levels - 1):
            size = (gaussian[i].shape[1], gaussian[i].shape[0])
            upsampled = cv2.pyrUp(gaussian[i + 1], dstsize=size)
            lap = cv2.subtract(gaussian[i], upsampled)
            laplacian.append(lap)
        laplacian.append(gaussian[-1])
        return laplacian


class BlobsAndConnected(GeometricOperations):
    def __init__(self):
        super().__init__()

    def simple_blob_detector(image, params=None):
        """
        Function: simple_blob_detector
        Description: Detects blobs in a binary or grayscale image using OpenCV's SimpleBlobDetector.
        Inputs:
            image (ndarray): The input image in which to detect blobs.
            params (cv2.SimpleBlobDetector_Params, optional): Custom parameters for blob detection. If None, default parameters are used.
        Output:
            list: A list of detected keypoints representing blobs.
        """
        if params is None:
            params = cv2.SimpleBlobDetector_Params()
            params.filterByArea = True
            params.minArea = 100
            params.maxArea = 5000

        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(image)
        return keypoints

    def connected_components_labeling(binary_image):
        """
        Function: connected_components_labeling
        Description: Performs connected component labeling on a binary image.
        Inputs:
            binary_image (ndarray): A binary image where the foreground is non-zero and background is zero.
        Output:
            tuple: A tuple (num_labels, labels) where 'num_labels' is the number of connected components,
                and 'labels' is an image with each pixel labeled by its component index.
        """
        num_labels, labels = cv2.connectedComponents(binary_image)
        return num_labels, labels

    def blob_statistics(binary_image):
        """
        Function: blob_statistics
        Description: Computes statistics for each connected component in a binary image.
        Inputs:
            binary_image (ndarray): A binary image for analysis.
        Output:
            tuple: A tuple (num_labels, labels, stats, centroids) where:
                - num_labels: number of labels (including background)
                - labels: labeled image
                - stats: statistics (x, y, width, height, area) for each label
                - centroids: centroids (x, y) of each label
        """
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
            binary_image
        )
        return num_labels, labels, stats, centroids

    def draw_bounding_boxes(image, stats, min_area=50):
        """
        Function: draw_bounding_boxes
        Description: Draws bounding boxes around blobs using their statistical data.
        Inputs:
            image (ndarray): The original image on which bounding boxes will be drawn.
            stats (ndarray): An array of statistics for each connected component (from connectedComponentsWithStats).
            min_area (int): Minimum area of blobs to consider for bounding box drawing.
        Output:
            ndarray: The image with bounding boxes drawn around qualifying blobs.
        """
        output = image.copy()
        for i in range(1, stats.shape[0]):  # Skip background (index 0)
            x, y, w, h, area = stats[i]
            if area >= min_area:
                cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return output

    def highlight_blobs_connected_components(image):
        """
        Function: highlight_blobs_connected_components
        Description: Detects blobs using connected components and assigns random colors to each.
        Inputs:
            image (ndarray): Binary input image where blobs are white and background is black.
        Output:
            ndarray: Color image with each blob highlighted in a different color.
        """
        num_labels, labels = cv2.connectedComponents(image)
        output = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
        colors = [
            tuple(np.random.randint(0, 255, 3).tolist()) for _ in range(num_labels)
        ]

        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                label = labels[y, x]
                if label > 0:
                    output[y, x] = colors[label]
        return output


class HoughTransform(GeometricOperations):
    def __init__(self):
        super().__init__()

    def hough_line_transform(image, rho=1, theta=np.pi / 180, threshold=150):
        """
        Function: hough_line_transform
        Description: Detects lines in a binary edge image using the standard Hough Line Transform.
        Inputs:
            image (ndarray): Edge-detected binary image (e.g., output of Canny).
            rho (float): Distance resolution of the accumulator in pixels.
            theta (float): Angle resolution of the accumulator in radians.
            threshold (int): Accumulator threshold parameter. Only lines with votes > threshold are returned.
        Output:
            list: A list of lines in (rho, theta) format. Returns None if no lines are found.
        """
        lines = cv2.HoughLines(image, rho, theta, threshold)
        return lines

    def probabilistic_hough_line_transform(
        image,
        rho=1,
        theta=np.pi / 180,
        threshold=100,
        min_line_length=50,
        max_line_gap=10,
    ):
        """
        Function: probabilistic_hough_line_transform
        Description: Detects lines in a binary edge image using the Probabilistic Hough Line Transform.
        Inputs:
            image (ndarray): Edge-detected binary image (e.g., output of Canny).
            rho (float): Distance resolution of the accumulator in pixels.
            theta (float): Angle resolution of the accumulator in radians.
            threshold (int): Accumulator threshold parameter. Only lines with votes > threshold are returned.
            min_line_length (int): Minimum line length. Line segments shorter than this are rejected.
            max_line_gap (int): Maximum allowed gap between points on the same line to link them.
        Output:
            list: A list of lines, where each line is represented as [x1, y1, x2, y2].
                Returns None if no lines are found.
        """
        lines = cv2.HoughLinesP(
            image,
            rho,
            theta,
            threshold,
            minLineLength=min_line_length,
            maxLineGap=max_line_gap,
        )
        return lines

    def hough_circle_detection(
        image, dp=1.2, min_dist=20, param1=100, param2=30, min_radius=0, max_radius=0
    ):
        """
        Function: hough_circle_detection
        Description: Detects circles in a grayscale image using the Hough Circle Transform.
        Inputs:
            image (ndarray): Input grayscale image.
            dp (float): Inverse ratio of the accumulator resolution to the image resolution.
            min_dist (int): Minimum distance between the centers of the detected circles.
            param1 (float): Higher threshold for the Canny edge detector (lower is half).
            param2 (float): Accumulator threshold for center detection. Smaller means more false circles.
            min_radius (int): Minimum radius of the circles to detect.
            max_radius (int): Maximum radius of the circles to detect.
        Output:
            ndarray: An array of detected circles, each defined by (x_center, y_center, radius).
                    Returns None if no circles are detected.
        """
        circles = cv2.HoughCircles(
            image,
            cv2.HOUGH_GRADIENT,
            dp,
            min_dist,
            param1=param1,
            param2=param2,
            minRadius=min_radius,
            maxRadius=max_radius,
        )
        if circles is not None:
            circles = np.uint16(np.around(circles))
        return circles
