input7 = 255
input12 = 1000
input16 = 2
input22 = 2
input6 = 120
def main(imageinput1):

    def BGR2GRAY(bgr_image):
        """
        Function: BGR To Gray Images
        Description: Convert BGR color space to gray scale.
        Input:
            bgr_image The image in BGR color space.
        Output
            gray_image: The gray scale image.
        """
        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        return gray_image


    def draw_contour_diameters(image, contours, thickness=2):
        """
        Draws the maximum Feret diameter (longest distance between two points) for each contour.

        Parameters:
            image (np.ndarray): The image to draw on.
            contours (list): List of contours.
            color (tuple): Color of the diameter line in BGR.
            thickness (int): Thickness of the line.

        Returns:
            np.ndarray: Image with diameters drawn.
        """
        color =(0, 255, 0)  # Green color in BGR
        for contour in contours:
            if len(contour) < 2:
                continue

            # Flatten contour to a list of points
            points = contour[:, 0, :]  # shape (N, 2)

            # Compute the farthest pair of points (brute-force)
            max_dist = 0
            pt1, pt2 = None, None
            for p1, p2 in itertools.combinations(points, 2):
                dist = np.linalg.norm(p1 - p2)
                if dist > max_dist:
                    max_dist = dist
                    pt1, pt2 = tuple(p1), tuple(p2)

            if pt1 is not None and pt2 is not None:
                cv2.line(image, pt1, pt2, color, thickness)
                cv2.putText(
                    image,
                    f"{max_dist:.1f}px",
                    (pt1[0], pt1[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    1,
                    cv2.LINE_AA
                )

        return image


    def draw_distance_on_image(image, points, thickness=2):
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


    def filter_contours(contours, min_area=1000):
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


    def find_contours(image):
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


    def get_contour_centroids(contours):
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


    def inv_threshold_binary_image(image, lower_th=120, upper_th=255):
        """
        Function: Inverse Binary Threshold Image
        Description: Apply inverse binary thresholding to the given image using lower and upper threshold values.

        Inputs:
            image (ndarray): The image to apply the thresholding to.
            lower_th (int, optional): The lower threshold value. Defaults to 120.
            upper_th (int, optional): The upper threshold value. Defaults to 255.

        Output:
            ndarray: The inverse binary thresholded image.
        """
        _, thresholded_image = cv2.threshold(
            image, lower_th, upper_th, cv2.THRESH_BINARY_INV
        )
        return thresholded_image

    bgr2gray2 = BGR2GRAY(bgr_image=imageinput1)
    inv_threshold_binary_image4 = inv_threshold_binary_image(image=bgr2gray2, lower_th=input6, upper_th=input7)
    find_contours8 = find_contours(image=inv_threshold_binary_image4)
    filter_contours10 = filter_contours(contours=find_contours8, min_area=input12)
    draw_contour_diameters13 = draw_contour_diameters(image=imageinput1, contours=filter_contours10, thickness=input16)
    get_contour_centroids17 = get_contour_centroids(contours=filter_contours10)
    draw_distance_on_image19 = draw_distance_on_image(image=draw_contour_diameters13, points=get_contour_centroids17, thickness=input22)
    return draw_distance_on_image19