import base64
import io
from PIL import Image
import cv2
import numpy as np
import functools

def image_preprocessing_decorator(func):
    @functools.wraps(func)
    def wrapper(image, *args, **kwargs):

        if type(image)==dict or type(image)== str:
            image_data = image["data"]
            if image_data.startswith("data:image"):
                image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            image = np.array(image)
            print("this ",type(image))
            processed_image = func(image, *args, **kwargs)
            print("that ")
            _, buffer = cv2.imencode('.jpg', processed_image)
            frame_base64 = base64.b64encode(buffer).decode("utf-8")
            return frame_base64  
        return func(image,*args,**kwargs)

    return wrapper