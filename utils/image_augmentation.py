import cv2
import base64
import numpy as np 

def read_image(image_path):
    """Read an image from a file."""
    return cv2.imread(image_path)

def image_to_base64(image):
    """Convert an image (numpy array) to a base64-encoded string."""
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')

def random_horizontal_flip(image):
    """Randomly flip the image horizontally."""
    image = read_image(image)
    if np.random.rand() > 0.5:
        return image_to_base64(cv2.flip(image, 1))
    return image_to_base64(image)

def random_vertical_flip(image):
    """Randomly flip the image vertically."""
    image = read_image(image)
    if np.random.rand() > 0.5:
        return image_to_base64(cv2.flip(image, 0))
    return image_to_base64(image)

def random_rotation(image, max_angle=90):
    """Randomly rotate the image by an angle."""
    image = read_image(image)
    angle = np.random.randint(-max_angle, max_angle)
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return image_to_base64(cv2.warpAffine(image, rotation_matrix, (w, h)))

def random_scaling(file_path):
    """
    Apply random scaling to the image while maintaining aspect ratio
    """
    try:
        # Read the image
        image = cv2.imread(file_path)
        if image is None:
            return "Error: Could not read image"

        # Get original dimensions
        height, width = image.shape[:2]
        
        # Generate random scale factor between 0.5 and 1.5
        scale_factor = np.random.uniform(0.5, 1.5)
        
        # Calculate new dimensions while maintaining aspect ratio
        new_height = int(height * scale_factor)
        new_width = int(width * scale_factor)
        
        # Resize image using the scale factor
        scaled_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
        
        # Create a new image with original size
        result_image = np.zeros_like(image)
        
        # Calculate starting positions to center the scaled image
        start_y = max(0, (height - new_height) // 2)
        start_x = max(0, (width - new_width) // 2)
        
        # If scaled image is larger, crop it to fit
        if new_height > height or new_width > width:
            crop_y = max(0, (new_height - height) // 2)
            crop_x = max(0, (new_width - width) // 2)
            scaled_image = scaled_image[
                crop_y:crop_y + min(height, new_height),
                crop_x:crop_x + min(width, new_width)
            ]
            # Update dimensions after cropping
            new_height, new_width = scaled_image.shape[:2]
            start_y = (height - new_height) // 2
            start_x = (width - new_width) // 2
        
        # Copy the scaled image into the result image
        result_image[
            start_y:start_y + new_height,
            start_x:start_x + new_width
        ] = scaled_image

        # Encode the result image
        _, buffer = cv2.imencode('.jpg', result_image)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return image_base64
    except Exception as e:
        return f"Error in scaling: {str(e)}"

def color_jitter(image_path, brightness_range=(0.8, 1.2), contrast_range=(0.8, 1.2)):
    """Randomly adjust the brightness and contrast of the image."""
    # Read the image
    image = read_image(image_path)
    
    # Generate random brightness and contrast values
    brightness_factor = np.random.uniform(*brightness_range)
    contrast_factor = np.random.uniform(*contrast_range)
    
    # Apply brightness and contrast adjustment
    # Adjust brightness by converting to float, scaling, and clipping to [0, 255]
    jittered_image = cv2.convertScaleAbs(image, alpha=contrast_factor, beta=0)
    jittered_image = np.clip(jittered_image * brightness_factor, 0, 255).astype(np.uint8)
    
    # Convert to base64 to display
    return image_to_base64(jittered_image)
