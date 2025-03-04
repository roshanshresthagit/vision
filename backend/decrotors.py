import base64
import io
import functools
from typing import Callable, Union, Tuple

import cv2
import numpy as np
from PIL import Image


def image_preprocessing_decorator(func: Callable) -> Callable:
    """
    A decorator that preprocesses an image input (Base64 string, dictionary, or numpy array) 
    before passing it to the wrapped function. It ensures that the function receives a numpy 
    array representation of the image and encodes the processed output back to Base64 if necessary.
    """
    @functools.wraps(func)
    def wrapper(image: Union[str, dict, np.ndarray], *args, **kwargs) -> Union[str, Tuple]:
        try:
            if isinstance(image, str):
                image = _decode_base64_to_array(image)
            elif isinstance(image, dict) and "data" in image:
                image = _decode_base64_to_array(image["data"].split(',')[1] if image["data"].startswith("data:image") else image["data"])
            elif not isinstance(image, np.ndarray):
                raise TypeError("Unsupported image format. Expected Base64 string, dictionary, or numpy.ndarray.")
            
            processed_image = func(image, *args, **kwargs)
            if isinstance(processed_image, list):
                print("here list")
                return processed_image
            return _encode_array_to_base64(processed_image)
        
        except Exception as e:
            raise RuntimeError(f"Error in image processing: {e}") from e
    
    return wrapper


def _decode_base64_to_array(image_base64: str) -> np.ndarray:
    """Decodes a Base64-encoded image string into a NumPy array."""
    image_bytes = base64.b64decode(image_base64)
    image = Image.open(io.BytesIO(image_bytes))
    return np.array(image)


def _encode_array_to_base64(image: np.ndarray) -> str:
    """Encodes a NumPy image array into a Base64 string."""
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode("utf-8")
