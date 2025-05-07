import cv2
import numpy as np

class ImageEnhancement:
    def __init__(self):
        """Initializes the ImageEnhancement class."""
        pass

    def histogram_equalization(self, image: np.ndarray) -> np.ndarray:
        """
        Function: Histogram Equalization
        # Description: Enhances the contrast of a grayscale image using histogram equalization.
        # Input: Grayscale or color image (will be converted to grayscale)
        # Output: Contrast-enhanced image
        """
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        contrast_enhanced_image = cv2.equalizeHist(image) 
        return contrast_enhanced_image

    def clahe(
        self, image: np.ndarray, clip_limit=2.0, tile_grid_size=(8, 8)
    ) -> np.ndarray:
        """
        Function: CLAHE (Contrast Limited Adaptive Histogram Equalization)
        # Description: Enhances contrast using adaptive histogram equalization with clipping limit.
        # Input: Grayscale or color image (converted internally), clip limit, and tile grid size
        # Output: CLAHE enhanced image
        """
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        clahe_enhanced_image = clahe.apply(image)
        return clahe_enhanced_image

    def gamma_correction(self, image: np.ndarray, gamma: float) -> np.ndarray:
        """
        Function: Gamma Correction
        # Description: Applies gamma correction to adjust brightness levels in the image.
        # Input: Image and gamma value
        # Output: Gamma-corrected image
        """
        inv_gamma = 1.0 / gamma
        table = np.array([(i / 255.0) ** inv_gamma * 255 for i in range(256)]).astype(
            "uint8"
        )
        gamma_corrected_image = cv2.LUT(image, table)
        return gamma_corrected_image

    def logarithmic_transform(self, image: np.ndarray) -> np.ndarray:
        """
        Function: Logarithmic Transform
        # Description: Applies a logarithmic transformation to expand dark pixels and compress bright pixels.
        # Input: Image
        # Output: Log-transformed image
        """
        image = image.astype(np.float32) + 1  # avoid log(0)
        log_image = np.log(image)
        log_image = cv2.normalize(log_image, None, 0, 255, cv2.NORM_MINMAX)
        log_image = log_image.astype(np.uint8)
        return log_image
        

    def power_law_transform(self, image: np.ndarray, gamma: float) -> np.ndarray:
        """
        Function: Power-Law (Gamma) Transform
        # Description: Performs power-law transformation to control image brightness/contrast.
        # Input: Image and gamma value
        # Output: Power-law transformed image
        """
        image = image / 255.0
        power_image = np.power(image, gamma)
        power_image = np.uint8(255 * power_image)
        return power_image

    def sharpening(self, image: np.ndarray) -> np.ndarray:
        """
        Function: Sharpening
        # Description: Sharpens the input image using a kernel filter.
        # Input: Image
        # Output: Sharpened image
        """
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened_image = cv2.filter2D(image, -1, kernel)
        return sharpened_image

    def edge_enhancement(self, image: np.ndarray) -> np.ndarray:
        """
        Function: Edge Enhancement
        # Description: Enhances edges using the Laplacian operator.
        # Input: Image (color or grayscale)
        # Output: Edge-enhanced image
        """
        gray = (
            cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        )
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        laplacian = cv2.convertScaleAbs(laplacian)
        enhanced = cv2.add(gray, laplacian)
        return enhanced
