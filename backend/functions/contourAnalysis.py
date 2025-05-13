import math
import random
import cv2
import numpy as np
from skimage.segmentation import slic, mark_boundaries, random_walker


class ContourAnalysis:
    def __init__(self):
        pass


class ShapeAnalysis(ContourAnalysis):
    def __init__(self):
        super().__init__()

    def find_contours(self, image):
        """
        Function: Find Contours
        Description: Detect external contours in a binary image.
        Input:
            binary_image: The input image in binary format (single-channel).
        Output
            contours: A list of detected contours.
        """
        contours, _ = cv2.findContours(
            image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        return contours
    
    def draw_distance_on_image(self,image, points, thickness=2):
        color = (0, 255, 0)  # Green color in BGR
        """
        Draws two points, a line between them, and the Euclidean distance label.

        Args:
            image (np.ndarray): The image to draw on.
            points (list of tuple): List of two points [(x1, y1), (x2, y2)].
            color (tuple): BGR color for drawing. Default is green.
            thickness (int): Thickness of the line and circles.

        Returns:
            np.ndarray: Image with drawings.
        """
        if len(points) != 2:
            raise ValueError("points must be a list of exactly two (x, y) tuples.")
        
        point1, point2 = points

        # Calculate Euclidean distance
        distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

        # Draw circles at points
        cv2.circle(image, point1, 5, color, -1)
        cv2.circle(image, point2, 5, color, -1)

        # Draw line between points
        cv2.line(image, point1, point2, color, thickness)

        # Calculate midpoint for label
        mid_x = (point1[0] + point2[0]) // 2
        mid_y = (point1[1] + point2[1]) // 2

        # Put distance text
        text = f"{distance:.2f}"
        cv2.putText(image, text, (mid_x + 10, mid_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)

        return image
    
    def get_contour_centroids(self,contours):
        centroids = []
        for cnt in contours:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                centroids.append((cx, cy))
            else:
                centroids.append(None)
        return centroids
        
    def draw_contours(self, original_bgr_image, contours):

        """
        Function: Draw Contours
        Description: Draw detected contours on the image.
        Input:
            image: The input image (BGR format).
            contours: A list of detected contours.
        Output
            image_with_contours: The input image with contours drawn.
        """
        image_with_contours = cv2.drawContours(
            original_bgr_image, contours, -1, (0, 255, 0), 2
        )
        return image_with_contours

    def filter_contours(self, contours, min_area=1000):
        """
        Function: Filter Contours
        Description: Filter contours based on area.
        Input:
            contours: A list of detected contours.
            min_area: Minimum area threshold for filtering.
        Output
            filtered_contours: A list of filtered contours.
        """
        filtered_contours = [
            contour for contour in contours if cv2.contourArea(contour) > min_area
        ]
        return filtered_contours

    def convex_hull(self, contour):
        """
        Function: Convex Hull
        Description: Compute the convex hull of a contour.
        Input:
            contour: The contour points as a NumPy array.
        Output
            hull: The convex hull as a NumPy array.
        """
        hull = cv2.convexHull(contour)
        return hull

    def contour_approximation(self, contour, epsilon_ratio=0.01):
        """
        Function: Contour Approximation
        Description: Approximate a contour to a simpler shape using the Douglas-Peucker algorithm.
        Input:
            contour: The contour points as a NumPy array.
            epsilon_ratio The approximation accuracy as a percentage of the arc length.
        Output
            approx: The approximated contour.
        """
        epsilon = epsilon_ratio * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        return approx

    def contour_area_and_perimeter(self, contour):
        """
        Function: Contour Area & Perimeter
        Description: Calculate the area and perimeter of a contour.
        Input:
            contour: The contour points as a NumPy array.
        Output
            area: The area of the contour.
            perimeter: The perimeter (arc length) of the contour.
        """
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        return area, perimeter

    def minimum_enclosing_circle_and_rectangle(self, contour):
        """
        Function: Minimum Enclosing Circle / Rectangle
        Description: Find the minimum enclosing circle and upright bounding rectangle for a contour.
        Input:
            contour: The contour points as a NumPy array.
        Output
            circle: A tuple (x, y, radius) representing the enclosing circle.
            rect: A tuple (x, y, w, h) representing the bounding rectangle.
        """
        (x, y), radius = cv2.minEnclosingCircle(contour)
        x, y, radius = int(x), int(y), int(radius)
        rect = cv2.boundingRect(contour)
        return (x, y, radius), rect

    def bounded_rotated_rectangle(self, contour):
        """
        Function: Bounding Rotated Rectangle
        Description: Compute the minimum area rotated bounding rectangle for a contour.
        Input:
            contour: The contour points as a NumPy array.
        Output
            box: The 4 corner points of the rotated rectangle.
            rect: The rotated rectangle parameters ((cx, cy), (w, h), angle).
        """
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = box.astype(int)
        return box, rect


class SegmentationClassical(ContourAnalysis):
    def __init__(self):
        super().__init__()

    def apply_grab_cut(self, image, rect, iter_count=5):
        """
        Function: GrabCut
        Description: Segment the foreground from background using the GrabCut algorithm.
        Input:
            image: The input BGR image.
            rect: A tuple (x, y, w, h) defining the bounding box for initialization (ROI).
            iter_count: Number of iterations for the GrabCut algorithm.
        Output
            mask_output: A binary mask where foreground is 1 and background is 0.
        """
        mask = np.zeros(image.shape[:2], np.uint8)

        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        cv2.grabCut(
            image, mask, rect, bgdModel, fgdModel, iter_count, cv2.GC_INIT_WITH_RECT
        )

        mask_output = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")

        segmented_image = image * mask_output[:, :, np.newaxis]

        return segmented_image

    def watershed(
        self, image: np.ndarray, filter_size=(3, 3), iterations=2
    ) -> np.ndarray:
        """
        Function: watershed
        Description: Segment distinct objects in the image using the Watershed algorithm.
        Input:
            image: The input BGR image to segment.
            filter_size: A tuple defining the kernel size for morphological operations.
        Output:
            image: The input image with object contours drawn in color.
        """
        print("Filter Size: ", filter_size)
        print("Iterations: ", iterations)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(
            gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        # Morphological Opening to remove small noise
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, filter_size)
        binary_image = cv2.morphologyEx(
            binary_image, cv2.MORPH_OPEN, kernel, iterations=iterations
        )

        # Dilate to get sure background
        sure_bg = cv2.dilate(binary_image, kernel, iterations=iterations)

        # Compute distance transform to find sure foreground (centers of objects)
        dist = cv2.distanceTransform(binary_image, cv2.DIST_L2, 5)
        _, sure_fg = cv2.threshold(dist, 0.5 * dist.max(), 255, cv2.THRESH_BINARY)
        sure_fg = sure_fg.astype(np.uint8)

        # unknown region refers to the boundary area
        unknown = cv2.subtract(sure_bg, sure_fg)

        _, markers = cv2.connectedComponents(sure_fg)

        # increment marker length so background is not 0 (required by watershed)
        markers += 1

        markers[unknown == 255] = 0

        # Apply watershed (modifies markers in place)
        markers = cv2.watershed(image, markers)

        labels = np.unique(markers)

        targets = []

        # Skip background (label 1) and boundary (-1), process each object
        for label in labels[2:]:
            target = np.where(markers == label, 255, 0).astype(np.uint8)

            contours, hierarchy = cv2.findContours(
                target, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            targets.append(contours[0])

        image = cv2.drawContours(image, targets, -1, color=(0, 23, 233), thickness=2)
        return image

    def k_means_clustering(self, image, k=3, criteria=None, attempts=10):
        """
        Function: kmeans_segmentation
        Description: Segment the image into clusters using the K-Means clustering algorithm.
        Input:
            image: The input BGR image to segment.
            k: Number of clusters for K-Means.
            criteria: Termination criteria for K-Means (default: 10 iterations or epsilon = 1.0).
            attempts: Number of times the algorithm is executed using different initial labellings.
        Output:
            segmented_image: The image with each pixel labeled by its cluster center color.
        """
        if criteria is None:
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

        pixel_values = image.reshape((-1, 3))
        pixel_values = np.float32(pixel_values)

        compactness, labels, centers = cv2.kmeans(
            pixel_values, k, None, criteria, attempts, cv2.KMEANS_PP_CENTERS
        )

        # Convert centers back to uint8 (valid image colors)
        centers = np.uint8(centers)

        # Replace each pixel value with its corresponding cluster center
        segmented_data = centers[labels.flatten()]
        segmented_image = segmented_data.reshape(image.shape)

        return segmented_image

    def mean_shift_segmentation(self, image, spatial_radius=10, color_radius=30):
        """
        Function: mean_shift_segmentation
        Description: Segment the image using the Mean Shift algorithm for clustering based on color and spatial proximity.
        Input:
            image: The input BGR image to segment.
            spatial_radius: Radius for the spatial window (affects smoothing).
            color_radius: Radius for the color window (affects color clustering).
        Output:
            segmented_image: The segmented image after applying mean shift filtering.
        """
        # Apply pyrMeanShiftFiltering to segment the image
        # This smooths the image while preserving edges based on spatial and color proximity
        segmented_image = cv2.pyrMeanShiftFiltering(
            image, sp=spatial_radius, sr=color_radius
        )
        return segmented_image

    def region_growing(self, image, seed=None, threshold=5):
        """
        Function: region_growing
        Description: Segment connected regions in an image based on pixel intensity similarity starting from a seed point.
        Input:
            image: The input BGR image.
            seed: A tuple (x, y) representing the starting point for region growing.
            threshold: Maximum absolute difference allowed between pixel intensities.
        Output:
            region_mask: A binary mask where grown region pixels are 255 and others are 0.
        """
        height, width, _ = image.shape

        # If seed is not provided, choose a random one
        if seed is None:
            seed = (random.randint(0, width - 1), random.randint(0, height - 1))

        region_mask = np.zeros((height, width), dtype=np.uint8)

        # Stack for DFS
        stack = [seed]

        # Color at the seed point
        seed_color = image[seed[1], seed[0]].astype(np.int32)

        # 8-connectivity directions
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        while stack:
            x, y = stack.pop()

            if region_mask[y, x] == 0:
                current_color = image[y, x].astype(np.int32)
                color_distance = np.linalg.norm(current_color - seed_color)

                if color_distance <= threshold:
                    region_mask[y, x] = 255

                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if (
                            0 <= nx < width
                            and 0 <= ny < height
                            and region_mask[ny, nx] == 0
                        ):
                            stack.append((nx, ny))

        return region_mask

    def slic_segmentation(
        self, image: np.ndarray, num_segments: int = 100, compactness: int = 10
    ):
        """
        Function: slic_segmentation
        Description: Segment the image into superpixels using the SLIC algorithm and assign each pixel to a region (seed).
        Input:
            image: The input BGR image.
            num_segments: Approximate number of superpixels to generate.
            compactness: Balances color proximity and spatial distance (higher = more spatially compact).
        Output:
            segmented_image: The input image with superpixel boundaries drawn.
            labels: A 2D array where each pixel is labeled with its superpixel index.
        """
        lab_image = cv2.cvtColor(image, cv2.color_bgr2lab)
        lab_image_float = lab_image.astype(np.float32) / 255.0

        labels = slic(lab_image_float, n_segments=num_segments, compactness=compactness)

        segmented_image = mark_boundaries(image, labels, color=(1, 0, 0))
        segmented_image = (segmented_image * 255).astype(np.uint8)

        return segmented_image, labels

    def seeded_segmentation(self, image, seeds=None, beta=90):
        """
        Function: seeded_segmentation
        Description: Segment the image using manually or programmatically defined seed markers with the Random Walker algorithm.
        Input:
            image: The input grayscale image.
            seeds: A 2D array (same size as image) where each pixel is:
                - 0 for unknown
                - 1, 2, 3, ... for different seed labels
            beta: Controls the smoothness; higher beta gives sharper boundaries.
        Output:
            segmentation: A 2D array where each pixel is labeled with its region index.
        """
        if not seeds:
            seeds = np.zeros_like(image, dtype=np.uint8)
            seeds[30:50, 30:50] = 1
            seeds[0:10, 0:10] = 2

        image = image.astype(np.float64)
        segmentation = random_walker(image, seeds, beta=beta, mode="bf")
        return segmentation

    def flood_fill(self, image, seed=None, threshold=30, fill_color=(0, 255, 0)):
        """
        Function: flood_fill_color
        Description: Perform flood fill on a BGR image starting from a seed point, replacing similar-colored connected pixels with a new color.
        Input:
            image: The input BGR image.
            seed: A tuple (x, y) indicating the seed point (column, row).
            threshold: Maximum allowed color difference (Euclidean) from the seed pixel.
            fill_color: A tuple (B, G, R) indicating the new fill color.
        Output:
            filled_image: A copy of the original image with the region flood-filled.
        """
        if not seed:
            height, width, _ = image.shape
            seed = (random.choice(range(width)), random.choice(range(height)))
        filled_image = image.copy()

        h, w, _ = image.shape
        visited = np.zeros((h, w), dtype=np.uint8)

        # Get the seed color
        seed_color = image[seed[1], seed[0]].astype(np.int32)

        # Queue for BFS
        queue = [seed]

        # 4-connected neighbors
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            x, y = queue.pop()

            if 0 <= x < w and 0 <= y < h and visited[y, x] == 0:
                current_color = image[y, x].astype(np.int32)

                # Compute Euclidean color distance
                color_diff = np.linalg.norm(current_color - seed_color)

                if color_diff <= threshold:
                    filled_image[y, x] = fill_color
                    visited[y, x] = 1

                    for dx, dy in directions:
                        queue.append((x + dx, y + dy))

        return filled_image


class EdgeDetection(ContourAnalysis):
    def __init__(self):
        super().__init__()

    def sobel_x(self, image):
        """
        Function: sobel_x
        Description: Applies Sobel filter in the X direction to detect vertical edges.
        Input:
            image: Input BGR image.
        Output:
            sobel_x: Edge-detected image highlighting vertical edges.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        image = cv2.convertScaleAbs(sobel_x)
        return image

    def sobel_y(self, image):
        """
        Function: sobel_y
        Description: Applies Sobel filter in the Y direction to detect horizontal edges.
        Input:
            image: Input BGR image.
        Output:
            sobel_y: Edge-detected image highlighting horizontal edges.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        image = cv2.convertScaleAbs(sobel_y)
        return image

    def laplacian(self, image):
        """
        Function: laplacian
        Description: Applies the Laplacian operator to detect edges based on second derivatives.
        Input:
            image: Input BGR image.
        Output:
            laplacian: Edge-detected image showing regions of rapid intensity change.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        image = cv2.convertScaleAbs(laplacian)
        return image

    def canny_edge_detector(self, image, threshold1=100, threshold2=100):
        """
        Function: canny
        Description: Applies the Canny edge detector to find edges using gradient and non-maximum suppression.
        Input:
            image: Input BGR image.
        Output:
            edges: Binary image with detected edges.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1=threshold1, threshold2=threshold2)
        return edges

    def scharr_filter(self, image):
        """
        Function: scharr
        Description: Applies Scharr filter for better gradient approximation compared to Sobel.
        Input:
            image: Input BGR image.
        Output:
            scharr_combined: Edge-detected image combining X and Y directions.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        grad_x = cv2.Scharr(gray, cv2.CV_64F, 1, 0)
        grad_y = cv2.Scharr(gray, cv2.CV_64F, 0, 1)
        scharr = cv2.magnitude(grad_x, grad_y)
        image = cv2.convertScaleAbs(scharr)
        return image

    def prewitt(self, image):
        """
        Function: prewitt
        Description: Applies Prewitt operator to detect edges using simple horizontal and vertical kernels.
        Input:
            image: Input BGR image.
        Output:
            prewitt_combined: Edge-detected image combining horizontal and vertical responses.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        kernelx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
        kernely = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        img_prewittx = cv2.filter2D(gray, -1, kernelx)
        img_prewitty = cv2.filter2D(gray, -1, kernely)
        image = cv2.convertScaleAbs(img_prewittx + img_prewitty)
        return image

    def roberts_cross(self, image):
        """
        Function: roberts_cross
        Description: Applies the Roberts Cross operator for edge detection using diagonal gradients.
        Input:
            image: Input BGR image.
        Output:
            roberts: Edge-detected image highlighting diagonal intensity changes.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        kernelx = np.array([[1, 0], [0, -1]], dtype=np.float32)
        kernely = np.array([[0, 1], [-1, 0]], dtype=np.float32)
        x = cv2.filter2D(gray, cv2.CV_64F, kernelx)
        y = cv2.filter2D(gray, cv2.CV_64F, kernely)
        roberts = cv2.magnitude(x, y)
        image = cv2.convertScaleAbs(roberts)
        return image
