import cv2

class ColorSpace:
    def __init__(self):
        super().__init__()
    
    def BGR2GRAY(self,bgr_image):
        gray_image = cv2.cvtColor(bgr_image,cv2.COLOR_BGR2GRAY)
        return gray_image
    def BGR2RGB(self,bgr_image):
        rgb_image = cv2.cvtColor(bgr_image,cv2.COLOR_BGR2RGB)
        return rgb_image
    def BGR2HSV(self,bgr_image):
        hsv_image = cv2.cvtColor(bgr_image,cv2.COLOR_BGR2HSV)
        # hsv_image = cv2.cvtColor(bgr_image,cv2.COLOR_BGR2HSV_FULL)
        return hsv_image
    def BGR2YCrCb(self,bgr_image):
        YCrCb_image = cv2.cvtColor(bgr_image,cv2.COLOR_BGR2YCrCb)
        return YCrCb_image
    def SplitImage(self,bgr_image):
        blue_image,green_image,red_image = cv2.split(bgr_image)
        return blue_image,green_image,red_image
    def MergeImage(self,blue_image,green_image,red_image):
        merged_image = cv2.merge((blue_image,green_image,red_image))
        return merged_image