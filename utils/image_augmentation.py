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

def random_scaling(image_path, scale_range=(0.8, 1.2)):
    """Randomly scale the image within the specified scale range."""
    # Read the image
    image = read_image(image_path)
    
    # Determine the scaling factor
    scale = np.random.uniform(*scale_range)
    scaled_width = int(image.shape[1] * scale)
    scaled_height = int(image.shape[0] * scale)
    
    # Apply scaling
    scaled_image = cv2.resize(image, (scaled_width, scaled_height))
    
    # Ensure it fits in the original canvas size if needed
    # (For example, by centering or cropping the scaled image if too large)
    result_image = np.zeros_like(image)  # Blank canvas of original size
    start_x = max((result_image.shape[1] - scaled_image.shape[1]) // 2, 0)
    start_y = max((result_image.shape[0] - scaled_image.shape[0]) // 2, 0)
    
    # Place scaled image on the canvas
    result_image[start_y:start_y + scaled_image.shape[0], start_x:start_x + scaled_image.shape[1]] = scaled_image

    # Convert to base64 to display
    return image_to_base64(result_image)


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
