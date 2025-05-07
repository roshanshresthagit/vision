import cv2
import numpy as np
from MTM import matchTemplates

class Matching:
    def __init__(self):
        pass

class Template(Matching):
    def __init__(self):
        super().__init__()
    
    def single_template_match(
            self,
            template: np.ndarray,
            scene: np.ndarray,
            label: str = "template",
            mask= None,
            method: str = "TM_CCOEFF_NORMED",
            score_threshold: float = 0.5,
            iou_threshold: float = 0.3,
            search_box= None
            ):
        """
            Function: match_single_template_with_nms
            Description: Performs single-template matching with optional mask, 
                        applies IoU-based non-maximum suppression, and returns final matches.

            Inputs:
                template (ndarray): Template image.
                scene (ndarray): Scene image to search in.
                label (str, optional): Label to associate with template. Defaults to "template".
                mask (ndarray, optional): Optional mask for the template. Defaults to None.
                method (str, optional): OpenCV template matching method as string. Defaults to "TM_CCOEFF_NORMED".
                score_threshold (float, optional): Score threshold to filter matches. Defaults to 0.5.
                iou_threshold (float, optional): IoU threshold for non-max suppression. Defaults to 0.3.
                search_box (tuple, optional): ROI within scene to restrict matching as (x, y, w, h). Defaults to None.

            Output:
                List[Tuple[str, Tuple[int, int, int, int], float]]: Filtered matches as (label, bbox, score).
        """

        tpl_entry = (label, template) if mask is None else (label, template, mask)
        method_enum = self._str_to_cv_method(method)

        raw_hits = matchTemplates(
            [tpl_entry],
            self.scene_img,
            method=self.method,
            N_object=float("inf"),
            score_threshold=self.score_threshold,
            maxOverlap=1.0,
            searchBox=self.search_box
        )
        final_hits = self._non_max_suppression(raw_hits, iou_threshold)
        return final_hits

    def _str_to_cv_method(self, s: str) -> int:
        return {
            "TM_SQDIFF":        cv2.TM_SQDIFF,
            "TM_SQDIFF_NORMED": cv2.TM_SQDIFF_NORMED,
            "TM_CCORR":         cv2.TM_CCORR,
            "TM_CCORR_NORMED":  cv2.TM_CCORR_NORMED,
            "TM_CCOEFF":        cv2.TM_CCOEFF,
            "TM_CCOEFF_NORMED": cv2.TM_CCOEFF_NORMED,
        }.get(s.upper(), cv2.TM_CCOEFF_NORMED)

    def _compute_iou(self, boxA, boxB) -> float:
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[0] + boxA[2], boxB[0] + boxB[2])
        yB = min(boxA[1] + boxA[3], boxB[1] + boxB[3])
        interW = max(0, xB - xA)
        interH = max(0, yB - yA)
        interArea = interW * interH
        union = boxA[2] * boxA[3] + boxB[2] * boxB[3] - interArea
        return interArea / union if union > 0 else 0

    def _non_max_suppression(
        self,
        hits,
        iou_thresh: float
    ):
        hits_sorted = sorted(hits, key=lambda h: h[2], reverse=True)
        keep = []
        for lbl, box, sc in hits_sorted:
            if any(self._compute_iou(box, k_box) >= iou_thresh for _, k_box, _ in keep):
                continue
            keep.append((lbl, box, sc))
        return keep

class FeatureDetectionClassical(Matching):
    def __init__(self):
        super().__init__()
    
    def detect_harris(image: np.ndarray,
                    block_size: int = 2,
                    ksize: int = 3,
                    k: float = 0.04,
                    thresh: float = 0.01) -> np.ndarray:
        """
        Function: detect_harris
        Description: Detects corners in an image using the Harris corner detection algorithm.
        Inputs:
            image (np.ndarray): Input BGR image.
            block_size (int, optional): Neighborhood size for corner detection. Defaults to 2.
            ksize (int, optional): Aperture parameter for the Sobel operator. Defaults to 3.
            k (float, optional): Harris detector free parameter. Defaults to 0.04.
            thresh (float, optional): Threshold for detecting strong corners. Defaults to 0.01.
        Output:
            np.ndarray: Output image with detected corners marked in red.
        """

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)
        dst = cv2.cornerHarris(gray, block_size, ksize, k)
        dst = cv2.dilate(dst, None)
        out = image.copy()
        out[dst > thresh * dst.max()] = [0, 0, 255]
        return out

    def detect_shi_tomasi(image: np.ndarray,
                        max_corners: int = 100,
                        quality_level: float = 0.01,
                        min_distance: float = 10) -> np.ndarray:
        """
        Function: detect_shi_tomasi
        Description: Detects corners in an image using the Shi-Tomasi corner detection algorithm.
        Inputs:
            image (np.ndarray): Input BGR image.
            max_corners (int, optional): Maximum number of corners to return. Defaults to 100.
            quality_level (float, optional): Minimum accepted quality of image corners. Defaults to 0.01.
            min_distance (float, optional): Minimum possible Euclidean distance between the returned corners. Defaults to 10.
        Output:
            np.ndarray: Output image with detected corners marked in green.
        """

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(gray, max_corners, quality_level, min_distance)
        out = image.copy()
        if corners is not None:
            for x, y in corners.reshape(-1, 2).astype(int):
                cv2.circle(out, (x, y), 4, (0, 255, 0), -1)
        return out

    def detect_fast(image: np.ndarray,
                    threshold: int = 10,
                    nonmax_suppression: bool = True) -> np.ndarray:
        
        """
        Function: detect_fast
        Description: Detects FAST features in an image.
        Inputs:
            image (np.ndarray): Input BGR image.
            threshold (int, optional): Detection threshold. Defaults to 10.
            nonmax_suppression (bool, optional): If true, non-maximum suppression is applied. Defaults to True.
        Output:
            np.ndarray: Output image with detected FAST features marked in red.
        """

        fast = cv2.FastFeatureDetector_create(threshold, nonmax_suppression)
        keypoints = fast.detect(image, None)
        image = cv2.drawKeypoints(image, keypoints, None, color=(255, 0, 0))
        return image

    def detect_orb(image: np.ndarray,
                n_features: int = 500) -> np.ndarray:
        
        """
        Function: detect_orb
        Description: Detects ORB features in an image.
        Inputs:
            image (np.ndarray): Input BGR image.
            n_features (int, optional): Maximum number of features to detect. Defaults to 500.
        Output:
            np.ndarray: Output image with detected ORB features marked in yellow.
        """
        orb = cv2.ORB_create(nfeatures=n_features)
        keypoints = orb.detect(image, None)
        image = cv2.drawKeypoints(image, keypoints, None, color=(0, 255, 255))
        return image

    def detect_mser(image: np.ndarray) -> np.ndarray:
        """
        Function: detect_mser
        Description: Detects Maximally Stable Extremal Regions (MSERs) in an image.
        Inputs:
            image (np.ndarray): Input BGR image.
        Output:
            np.ndarray: Output image with detected MSERs outlined in magenta.
        """
        mser = cv2.MSER_create()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        regions, _ = mser.detectRegions(gray)
        out = image.copy()
        for pts in regions:
            hull = cv2.convexHull(pts.reshape(-1, 1, 2))
            cv2.polylines(out, [hull], True, (255, 0, 255), 1)
        return out
class AccumulationAndBackgroundModels(Matching):
    def __init__(self):
        super().__init__()
    def running_average(bg: np.ndarray,
                        frame: np.ndarray,
                        alpha: float = 0.05) -> np.ndarray:
        """
        Function: running_average
        Description: Updates the background model using running average.
        Inputs:
            bg (np.ndarray): Background model.
            frame (np.ndarray): Current frame.
            alpha (float, optional): Learning rate. Defaults to 0.05.
        Output:
            np.ndarray: Updated background model.
        """
        result =  (1 - alpha) * bg + alpha * frame
        return result

    def accumulate_weighted(bg: np.ndarray,
                            frame: np.ndarray,
                            alpha: float = 0.05) -> np.ndarray:
        """
        Function: accumulate_weighted
        Description: Updates the background model using the running average method in OpenCV.
        Inputs:
            bg (np.ndarray): Background model.
            frame (np.ndarray): Current frame.
            alpha (float, optional): Learning rate. Defaults to 0.05.
        Output:
            np.ndarray: Updated background model.
        """

        cv2.accumulateWeighted(frame, bg, alpha)
        return bg

    def frame_difference(prev_frame: np.ndarray,
                        curr_frame: np.ndarray,
                        thresh: int = 25) -> np.ndarray:
        """
        Function: frame_difference
        Description: Computes the absolute difference between two consecutive frames and applies a threshold to extract the foreground mask.
        Inputs:
            prev_frame (np.ndarray): Previous frame in the sequence.
            curr_frame (np.ndarray): Current frame in the sequence.
            thresh (int, optional): Threshold value for binary thresholding. Defaults to 25.
        Output:
            np.ndarray: Binary foreground mask highlighting the differences between the two frames.
        """

        d = cv2.absdiff(prev_frame, curr_frame)
        _, fg_mask = cv2.threshold(d, thresh, 255, cv2.THRESH_BINARY)
        return fg_mask