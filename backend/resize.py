import cv2

def resize_image(image_path, target_width=640):
    # Load the image
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Error: Image not found or unable to open at {image_path}.")
        return None
    
    # Get the current dimensions of the image
    height, width = image.shape[:2]
    
    # Calculate the aspect ratio
    aspect_ratio = width / height
    
    # Calculate the new dimensions while preserving aspect ratio
    new_height = int(target_width / aspect_ratio)
    new_dimensions = (target_width, new_height)
    
    # Resize the image to the new dimensions
    resized_image = cv2.resize(image, new_dimensions)
    
    return resized_image

# Example usage
image_path = r"C:\Users\shres\Downloads\Image_20250304162546274.jpg"
resized_image = resize_image(image_path)

# Save the resized image if it exists
if resized_image is not None:
    save_path = r"C:\Users\shres\Downloads\resized_image_1.jpg"  # Provide full path to save
    cv2.imwrite(save_path, resized_image)
    print(f"Resized image saved to: {save_path}")
