import cv2

class ColorSpace:
    def __init__(self):
        pass
    
    def BGR2GRAY(self,bgr_image):
        """
        Function: BGR To Gray Images
        Description: Convert BGR color space to gray scale.        
        Input: 
            bgr_image The image in BGR color space.
        Output 
            gray_image: The gray scale image.
        """
        gray_image = cv2.cvtColor(bgr_image,cv2.COLOR_BGR2GRAY)
        return gray_image
    def BGR2RGB(self,bgr_image):
        """
        Function: BGR To RGB Images
        Description: Convert BGR color space to RGB color space.        
        Input: 
            bgr_image: The image in BGR color space.
        Output: 
            rgb_image: The RGB color space image.
        """
        rgb_image = cv2.cvtColor(bgr_image,cv2.COLOR_BGR2RGB)
        return rgb_image
    def BGR2HSV(self,bgr_image):
        """
        Function: BGR To HSV Images
        Description: Convert BGR color space to HSV color space.        
        Input :
            bgr_image: The image in BGR color space.
        Output :
            hsv_image: The HSV color space image.
        """
        hsv_image = cv2.cvtColor(bgr_image,cv2.COLOR_BGR2HSV)
        # hsv_image = cv2.cvtColor(bgr_image,cv2.COLOR_BGR2HSV_FULL)
        return hsv_image
    def BGR2HSL(self,bgr_image):
        """
        Function: BGR To HSL Images
        Description: Convert BGR color space to HSL color space.        
        Input :
            bgr_image: The image in BGR color space.
        Output :
            hsl_image: The HSL color space image.
        """
        hsl_image = cv2.cvtColor(bgr_image,cv2.COLOR_BGR2HLS)
        # hsl_image = cv2.cvtColor(bgr_image,cv2.COLOR_BGR2HLS_FULL)
        return hsl_image
    def BGR2YCrCb(self,bgr_image):
        """
        Function: BGR To YCrCb Images
        Description: Convert BGR color space to YCrCb color space.        
        Input :
            bgr_image: The image in BGR color space.
        Output :
            ycrcb_image: The YCrCb color space image.
        """
        ycrcb_image = cv2.cvtColor(bgr_image,cv2.COLOR_BGR2YCrCb)
        return ycrcb_image
    def BGR2Lab(self,bgr_image):
        """
        Function: BGR To Lab Images
        Description: Convert BGR color space to Lab color space.        
        Input :
            bgr_image: The image in BGR color space.
        Output :
            lab_image: The Lab color space image.
        """
        lab_image = cv2.cvtColor(bgr_image,cv2.COLOR_BGR2LAB)
        return lab_image
    def SplitImage(self,bgr_image):
        """
        Function: Split BGR Image
        Description: Split a BGR image into three color channels, blue, green and red.
        Input :
            bgr_image: The BGR image.
        Output :
            blue_image,green_image,red_image: The three color channels of the BGR image.
        """
        blue_image,green_image,red_image = cv2.split(bgr_image)
        return blue_image,green_image,red_image
    def MergeImage(self,blue_image,green_image,red_image):
        """
        Function: Merge Three Color Channels
        Description: Merge three color channels (blue,green and red) into a BGR image.
        Input :
            blue_image,green_image,red_image: The three color channels of the BGR image.
        Output :
            merged_image: The BGR image.
        """
        merged_image = cv2.merge((blue_image,green_image,red_image))
        return merged_image