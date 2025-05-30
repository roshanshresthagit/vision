import cv2
from ultralytics import YOLO


class YoloDetection:
    def __init__(self):
        pass

    def object_detection_yolo(self,model,image):
        model = YOLO(model)
        results = model(image, verbose=False)
        result = results[0]
        boxes = result.boxes

        # Extract detections
        detected_objects = []
        for box in boxes:
            detected_objects.append({
                "bbox": box.xyxy[0].tolist(),       
                "confidence": float(box.conf[0]),   
                "class_id": int(box.cls[0])         
            })

        return detected_objects
    
    def plot_detections(self, detected_objects, image):
        img = image.copy()
        
        for idx, obj in enumerate(detected_objects):
            bbox = obj["bbox"]
            x1, y1, x2, y2 = map(int, bbox)
            cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)
            cv2.putText(
                img,
                f"{idx}",                  
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 0, 0),               
                2,
                cv2.LINE_AA,
            )
            
        return img

    
    def crop_detected_object(self, detected_objects, image, index=0):
        if index < 0 or index >= len(detected_objects):
            raise IndexError("Index out of range for detected objects list.")
        
        bbox = detected_objects[index]["bbox"]
        x1, y1, x2, y2 = map(int, bbox)
        crop_img = image[y1:y2, x1:x2]

        return crop_img
    