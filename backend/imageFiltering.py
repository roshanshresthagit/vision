import cv2
import numpy as np


class ImageFiltering:
    pass


class Threshold(ImageFiltering):
    def __init__(self):
        super().__init__()

    def threshold_binary_image(self, image, lower_th=120, upper_th=255):
        """
        Function: Binary Threshold Image
        Description: Apply thresholding to the given image using lower and upper threshold values.

        Inputs:
            image (ndarray): The image to apply the thresholding to.
            lower_th (int, optional): The lower threshold value. Defaults to 120.
            upper_th (int, optional): The upper threshold value. Defaults to 255.

        Output:
            ndarray: The thresholded image.
        """
        _, thresholded_image = cv2.threshold(
            image, lower_th, upper_th, cv2.THRESH_BINARY
        )
        return thresholded_image

    def inv_threshold_binary_image(self, image, lower_th=120, upper_th=255):
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

    def threshold_truncate_image(self, image, lower_th=120, upper_th=255):
        """
        Function: Truncate Threshold Image
        Description: Apply truncate thresholding to the given image using lower and upper threshold values.

        Inputs:
            image (ndarray): The image to apply the thresholding to.
            lower_th (int, optional): The lower threshold value. Defaults to 120.
            upper_th (int, optional): The upper threshold value. Defaults to 255.

        Output:
            ndarray: The truncate thresholded image.
        """
        _, thresholded_image = cv2.threshold(
            image, lower_th, upper_th, cv2.THRESH_TRUNC
        )
        return thresholded_image

    def threshold_to_zero_image(self, image, lower_th=120, upper_th=255):
        """
        Function: Threshold to Zero Image
        Description: Apply threshold to zero to the given image using lower and upper threshold values.

        Inputs:
            image (ndarray): The image to apply the thresholding to.
            lower_th (int, optional): The lower threshold value. Defaults to 120.
            upper_th (int, optional): The upper threshold value. Defaults to 255.

        Output:
            ndarray: The thresholded image.
        """

        _, thresholded_image = cv2.threshold(
            image, lower_th, upper_th, cv2.THRESH_TOZERO
        )
        return thresholded_image

    def threshold_to_zero_inv_image(self, image, lower_th=120, upper_th=255):
        """
        Function: Threshold to Zero Inverse Image
        Description: Apply threshold to zero inverse to the given image using lower and upper threshold values.

        Inputs:
            image (ndarray): The image to apply the thresholding to.
            lower_th (int, optional): The lower threshold value. Defaults to 120.
            upper_th (int, optional): The upper threshold value. Defaults to 255.

        Output:
            ndarray: The thresholded image.
        """

        _, thresholded_image = cv2.threshold(
            image, lower_th, upper_th, cv2.THRESH_TOZERO_INV
        )
        return thresholded_image

    def threshold_binary_image_OTSU(self, image):
        """
        Function: Binary Threshold Image with OTSU
        Description: Apply thresholding to the given image with OTSU, where the threshold value is automatically determined.

        Inputs:
            image (ndarray): The image to apply the thresholding to.
        Output:
            ndarray: The thresholded image.
        """
        _, thresholded_image = cv2.threshold(
            image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        return thresholded_image

    def inv_threshold_binary_image_OTSU(self, image):
        """
        Function: Inverse Binary Threshold Image with OTSU
        Description: Apply inverse thresholding to the given image with OTSU, where the threshold value is automatically determined.

        Inputs:
            image (ndarray): The image to apply the inverse thresholding to.
        Output:
            ndarray: The thresholded image.
        """
        _, thresholded_image = cv2.threshold(
            image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )
        return thresholded_image

    def threshold_truncate_image_OTSU(self, image):
        """
        Function: Truncate Threshold Image with OTSU
        Description: Apply truncate thresholding to the given image with OTSU, where the threshold value is automatically determined.

        Inputs:
            image (ndarray): The image to apply the thresholding to.
        Output:
            ndarray: The thresholded image.
        """
        _, thresholded_image = cv2.threshold(
            image, 0, 255, cv2.THRESH_TRUNC + cv2.THRESH_OTSU
        )
        return thresholded_image

    def threshold_to_zero_image_OTSU(self, image):
        """
        Function: Threshold to Zero Image with OTSU
        Description: Apply threshold to zero to the given image with OTSU, where the threshold value is automatically determined.

        Inputs:
            image (ndarray): The image to apply the thresholding to.
        Output:
            ndarray: The thresholded image.
        """
        _, thresholded_image = cv2.threshold(
            image, 0, 255, cv2.THRESH_TOZERO + cv2.THRESH_OTSU
        )
        return thresholded_image

    def threshold_to_zero_inv_image_OTSU(self, image):
        """
        Function: Threshold to Zero Inverse Image with OTSU
        Description: Apply threshold to zero inverse to the given image with OTSU, where the threshold value is automatically determined.

        Inputs:
            image (ndarray): The image to apply the thresholding to.
        Output:
            ndarray: The thresholded image.
        """
        _, thresholded_image = cv2.threshold(
            image, 0, 255, cv2.THRESH_TOZERO_INV + cv2.THRESH_OTSU
        )
        return thresholded_image

    def threshold_triangle_image(self, image):
        """
        Function: Triangle Threshold Image
        Description: Apply triangle thresholding to the given image.

        Inputs:
            image (ndarray): The image to apply the thresholding to.
        Output:
            ndarray: The thresholded image.
        """
        _, thresholded_image = cv2.threshold(
            image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_TRIANGLE
        )
        return thresholded_image


class AdaptiveThreshold(ImageFiltering):
    def __init__(self):
        super().__init__()

    def adaptive_threshold_mean_C(self, image, block_size=21, C=10):
        """
        Function: Adaptive Threshold with Mean
        Description: Apply adaptive thresholding to the given image with mean calculation.

        Inputs:
            image (ndarray): The image to apply the thresholding to.
            block_size (int, optional): The size of the window used for calculating the threshold value. Defaults to 21.
            C (int, optional): A constant value subtracted from the calculated threshold value. Defaults to 10.

        Output:
            ndarray: The thresholded image.
        """
        threshold_image = cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, block_size, C
        )
        return threshold_image

    def adaptive_threshold_gaussian_C(self, image, block_size=21, C=10):
        """
        Function: Adaptive Threshold with Gaussian
        Description: Apply adaptive thresholding to the given image with Gaussian calculation.

        Inputs:
            image (ndarray): The image to apply the thresholding to.
            block_size (int, optional): The size of the window used for calculating the threshold value. Defaults to 21.
            C (int, optional): A constant value subtracted from the calculated threshold value. Defaults to 10.

        Output:
            ndarray: The thresholded image.
        """
        threshold_image = cv2.adaptiveThreshold(
            image,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            block_size,
            C,
        )
        return threshold_image


class BlurringAndNoiseReduction(ImageFiltering):
    def __init__(self):
        super().__init__()

    def median_blur(self, image, ksize=3):
        """
        Function: Median Blur
        Description: Apply median blurring to the given image.

        Inputs:
            image (ndarray): The image to apply the blurring to.
            ksize (int, optional): The size of the kernel used for blurring. Defaults to 3.

        Output:
            ndarray: The blurred image.
        """
        blurred_image = cv2.medianBlur(image, ksize)
        return blurred_image

    def gaussian_blur(self, image, ksize=3, sigmaX=0, sigmaY=0):
        """
        Function: Gaussian Blur
        Description: Apply Gaussian blurring to the given image.

        Inputs:
            image (ndarray): The image to apply the blurring to.
            ksize (int, optional): The size of the kernel used for blurring. Defaults to 3.
            sigmaX (int, optional): The standard deviation in the X direction. Defaults to 0.
            sigmaY (int, optional): The standard deviation in the Y direction. Defaults to 0.
        Output:
            ndarray: The blurred image.
        """
        blurred_image = cv2.GaussianBlur(image, (ksize, ksize), sigmaX, sigmaY)
        return blurred_image

    def bilateral_filter(self, image, d=9, sigmaColor=75, sigmaSpace=75):
        """
        Function: Bilateral Filter
        Description: Apply bilateral filtering to the given image.

        Inputs:
            image (ndarray): The image to apply the filtering to.
            d (int, optional): The diameter of the pixel neighborhood. Defaults to 9.
            sigmaColor (int, optional): The filter sigma in the color space. Defaults to 75.
            sigmaSpace (int, optional): The filter sigma in the coordinate space. Defaults to 75.

        Output:
            ndarray: The filtered image.
        """
        filtered_image = cv2.bilateralFilter(image, d, sigmaColor, sigmaSpace)
        return filtered_image

    def box_filter(self, image, ddepth=-1, ksize=3):
        """
        Function: Box Filter
        Description: Apply box filtering to the given image.

        Inputs:
            image (ndarray): The image to apply the filtering to.
            ddepth (int,optional): The depth of the output image. Defaults to -1.
            ksize (int, optional): The size of the kernel used for filtering. Defaults to 3.

        Output:
            ndarray: The filtered image.
        """
        filtered_image = cv2.boxFilter(image, ddepth, (ksize, ksize))
        return filtered_image

    def non_local_means_denoising(
        self, image, h=10, hColor=10, templateWindowSize=7, searchWindowSize=15
    ):
        """
        Function: Non-Local Means Denoising
        Description: Apply Non-Local Means Denoising to a color image using OpenCV's fastNlMeansDenoisingColored.
        Inputs:
            image (numpy.ndarray): Input BGR image to denoise.
            h (int, optional): Filter strength for luminance component. Higher value removes more noise but can lose details. Defaults to 10.
            hColor (int, optional): Filter strength for color components (chrominance). Defaults to 10.
            templateWindowSize (int, optional): Size of the patch used for denoising (should be odd, e.g., 7). Defaults to 7.
            searchWindowSize (int, optional): Size of the window to search for similar patches (should be odd, e.g., 15). Defaults to 15.
        Output:
            numpy.ndarray: Denoised image.
        """
        image = cv2.fastNlMeansDenoisingColored(
            image, None, h, hColor, templateWindowSize, searchWindowSize
        )
        return image


class MorphologicalOperations(ImageFiltering):
    def __init__(self):
        super().__init__()

    def _is_binarized(self, image):
        unique_values = np.unique(image)
        return len(unique_values) == 2 and set(unique_values) == {0, 255}

    def _binarize_image(self, image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    def erode(self, image, iterations=1, kernel=None, filter_size=(3, 3)):
        """
        Function: Erode
        Description: Apply erosion morphological operation to the given image.

        Inputs:
            image (ndarray): The image to apply the erosion to.
            iterations (int, optional): Number of times erosion is applied. Defaults to 1.
            kernel (ndarray, optional): Structuring element used for erosion. If None, a default kernel is created. Defaults to None.
            filter_size (tuple, optional): Size of the structuring element if kernel is None. Defaults to (3, 3).

        Output:
            ndarray: The eroded image.
        """
        if not self._is_binarized(image):
            image = self._binarize_image(image)
        if kernel is None:
            kernel = np.ones(filter_size, np.uint8)
        eroded_image = cv2.erode(image, kernel=kernel, iterations=iterations)
        return eroded_image

    def dilate(self, image, iterations=1, kernel=None, filter_size=(3, 3)):
        """
        Function: Dilate
        Description: Apply dilation morphological operation to the given image.

        Inputs:
            image (ndarray): The image to apply the dilation to.
            iterations (int, optional): Number of times dilation is applied. Defaults to 1.
            kernel (ndarray, optional): Structuring element used for dilation. If None, a default kernel is created. Defaults to None.
            filter_size (tuple, optional): Size of the structuring element if kernel is None. Defaults to (3, 3).

        Output:
            ndarray: The dilated image.
        """

        if not self._is_binarized(image):
            image = self._binarize_image(image)
        if kernel is None:
            kernel = np.ones(filter_size, np.uint8)
        dilated_image = cv2.dilate(image, kernel=kernel, iterations=iterations)
        return dilated_image

    def opening(self, image, kernel=None, filter_size=(3, 3)):
        """
        Function: Opening
        Description: Apply opening morphological operation to the given image.

        Inputs:
            image (ndarray): The image to apply the opening to.
            kernel (ndarray, optional): Structuring element used for opening. If None, a default kernel is created. Defaults to None.
            filter_size (tuple, optional): Size of the structuring element if kernel is None. Defaults to (3, 3).

        Output:
            ndarray: The opened image.
        """
        if not self._is_binarized(image):
            image = self._binarize_image(image)
        if kernel is None:
            kernel = np.ones(filter_size, np.uint8)
        opened_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        return opened_image

    def closing(self, image, kernel=None, filter_size=(3, 3)):
        """
        Function: Closing
        Description: Apply closing morphological operation to the given image.

        Inputs:
            image (ndarray): The image to apply the closing to.
            kernel (ndarray, optional): Structuring element used for closing. If None, a default kernel is created. Defaults to None.
            filter_size (tuple, optional): Size of the structuring element if kernel is None. Defaults to (3, 3).

        Output:
            ndarray: The closed image.
        """
        if not self._is_binarized(image):
            image = self._binarize_image(image)
        if kernel is None:
            kernel = np.ones(filter_size, np.uint8)
        closed_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        return closed_image

    def morphological_gradient(self, image, kernel=None, filter_size=(3, 3)):
        """
        Function: Morphological Gradient
        Description: Apply morphological gradient operation to the given image.

        Inputs:
            image (ndarray): The image to apply the gradient to.
            kernel (ndarray, optional): Structuring element used for gradient. If None, a default kernel is created. Defaults to None.
            filter_size (tuple, optional): Size of the structuring element if kernel is None. Defaults to (3, 3).

        Output:
            ndarray: The gradient image.
        """
        if not self._is_binarized(image):
            image = self._binarize_image(image)
        if kernel is None:
            kernel = np.ones(filter_size, np.uint8)
        gradient_image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)
        return gradient_image

    def white_hat(self, image, filter_size=(3, 3)):
        """
        Function: White Hat
        Description: Apply white hat (top hat) morphological operation to the given image.
        Inputs:
            image (ndarray): The image to apply the white hat operation to.
            filter_size (tuple, optional): The size of the structuring element. Defaults to (3, 3).
        Output:
            ndarray: The image after applying the white hat operation.
        """

        if not self._is_binarized(image):
            image = self._binarize_image()
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, filter_size)
        white_hat_image = cv2.morphologyEx(gray_image, cv2.MORPH_TOPHAT, kernel)
        return white_hat_image

    def black_hat(self, image, filter_size=(3, 3)):
        """
        Function: Black Hat
        Description: Apply black hat morphological operation to the given image.

        Inputs:
            image (ndarray): The image to apply the black hat operation to.
            filter_size (tuple, optional): The size of the structuring element. Defaults to (3, 3).

        Output:
            ndarray: The image after applying the black hat operation.
        """

        if not self._is_binarized(image):
            image = self._binarize_image(image)
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, filter_size)
        black_hat_image = cv2.morphologyEx(gray_image, cv2.MORPH_BLACKHAT, kernel)
        return black_hat_image


class ExposureOperations(ImageFiltering):
    def __init__(self):
        super().__init__()

    def brighten_image(self, image, alpha=1, beta=10):
        """
        Function: Brighten Image
        Description: Increase the brightness of the given image using the specified alpha and beta values.

        Inputs:
            image (ndarray): The image to be brightened.
            alpha (float, optional): The gain (contrast) factor. Defaults to 1.
            beta (int, optional): The bias (brightness) factor added to each pixel. Defaults to 10. Higher beta gives brighter image.

        Output:
            ndarray: The brightened image.
        """

        brightened_image = cv2.convertScaleAbs(image, alpha, beta)
        return brightened_image

    def darken_image(self, image, alpha=1, beta=-10):
        """
        Function: Darken Image
        Description: Decrease the brightness of the given image using the specified alpha and beta values.

        Inputs:
            image (ndarray): The image to be darkened.
            alpha (float, optional): The gain (contrast) factor. Defaults to 1.
            beta (int, optional): The bias (brightness) factor added to each pixel. Defaults to -10. Lower beta gives darker image.

        Output:
            ndarray: The darkened image.
        """

        darkened_image = cv2.convertScaleAbs(image, alpha, beta)
        return darkened_image

    def contrast_image(self, image, alpha=1.2, beta=0):
        """
        Function: Contrast Image
        Description: Adjust the contrast of the given image using the specified alpha and beta values.

        Inputs:
            image (ndarray): The image to be contrasted.
            alpha (float, optional): The gain (contrast) factor. Defaults to 1.2. Higher alpha gives higher contrast.
            beta (int, optional): The bias (brightness) factor added to each pixel. Defaults to 0.

        Output:
            ndarray: The contrasted image.
        """
        contrasted_image = cv2.convertScaleAbs(image, alpha, beta)
        return contrasted_image
