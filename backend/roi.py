import cv2
import numpy as np


class ROIS:
    def __init__(self):
        # No need for super().__init__() as there's no parent class
        pass

    def fixed_rectangle_roi(self, image, x=50, y=50, w=100, h=100):
        """
        Function: Fixed Rectangle ROI
        Description: Extract a fixed rectangular region of interest from the image.

        Inputs:
            image (ndarray): The input image.
            x (int, optional): X-coordinate of the top-left corner. Defaults to 50.
            y (int, optional): Y-coordinate of the top-left corner. Defaults to 50.
            w (int, optional): Width of the rectangle. Defaults to 100.
            h (int, optional): Height of the rectangle. Defaults to 100.

        Output:
            ndarray: The extracted ROI.
        """
        # Add boundary checks to prevent index errors
        h_img, w_img = image.shape[:2]
        x = max(0, min(x, w_img - 1))
        y = max(0, min(y, h_img - 1))
        w = min(w, w_img - x)
        h = min(h, h_img - y)

        return image[y : y + h, x : x + w]

    def polygon_roi(self, image, points):
        """
        Function: Polygon ROI
        Description: Extract a polygonal region of interest using a list of points.

        Inputs:
            image (ndarray): The input image.
            points (list): List of (x, y) tuples forming a polygon.

        Output:
            ndarray: The ROI image.
            ndarray: The binary mask used.
        """
        if not points or len(points) < 3:
            print("No points given that form polygon.")
            return None, None

        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [np.array(points, dtype=np.int32)], 255)
        roi = cv2.bitwise_and(image, image, mask=mask)
        return roi, mask

    def circular_roi(self, image, center=(100, 100), radius=50):
        """
        Function: Circular ROI
        Description: Extract a circular region of interest from the image.

        Inputs:
            image (ndarray): The input image.
            center (tuple, optional): Center of the circle. Defaults to (100, 100).
            radius (int, optional): Radius of the circle. Defaults to 50.

        Output:
            ndarray: The ROI image.
            ndarray: The binary mask used.
        """
        # Add boundary checks
        h_img, w_img = image.shape[:2]
        x, y = center
        x = max(0, min(x, w_img - 1))
        y = max(0, min(y, h_img - 1))
        radius = min(radius, min(x, y, w_img - x, h_img - y))

        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.circle(mask, (x, y), radius, 255, -1)
        roi = cv2.bitwise_and(image, image, mask=mask)
        return roi, mask

    def rectangle_drag_select_roi(self, image):
        """
        Function: Rectangle Drag-Select ROI
        Description: Allow user to manually drag and select a rectangle ROI.

        Inputs:
            image (ndarray): The input image.

        Output:
            ndarray: The selected ROI image.
        """
        r = cv2.selectROI("Select ROI", image, fromCenter=False, showCrosshair=True)
        cv2.destroyAllWindows()
        if (
            r[2] <= 0 or r[3] <= 0
        ):  # Changed from == 0 to <= 0 to handle negative values
            return None
        x, y, w, h = r
        return image[y : y + h, x : x + w]

    def fiducial_marker_roi(self, image, dictionary=cv2.aruco.DICT_4X4_50):
        """
        Function: Fiducial Marker-Based ROI
        Description: Detect ArUco markers and extract ROI based on their corners.

        Inputs:
            image (ndarray): The input image.
            dictionary (int, optional): ArUco dictionary type. Defaults to cv2.aruco.DICT_4X4_50.

        Output:
            ndarray: ROI image if markers found.
            ndarray: Binary mask used for ROI.
        """

        aruco_dict = cv2.aruco.getPredefinedDictionary(dictionary)
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
        corners, ids, _ = detector.detectMarkers(image)

        if ids is None or len(corners) == 0:
            return None, None

        pts = np.concatenate(corners, axis=1)[0].astype(int)
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [pts], 255)
        roi = cv2.bitwise_and(image, image, mask=mask)
        return roi, mask

    def mask_based_roi(self, image, mask):
        """
        Function: Mask-Based ROI
        Description: Apply a binary mask to extract the ROI from the image.

        Inputs:
            image (ndarray): The input image.
            mask (ndarray): The binary mask (255 for ROI, 0 for background).

        Output:
            ndarray: The ROI image.
        """
        # Check if mask dimensions match image dimensions
        if mask.shape[:2] != image.shape[:2]:
            print("Warning: Mask and image dimensions do not match")
            # Resize mask to match image dimensions
            mask = cv2.resize(mask, (image.shape[1], image.shape[0]))

        image = cv2.bitwise_and(image, image, mask=mask)
        return image
