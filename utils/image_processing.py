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

def resize(image, size=(256, 256)):
    image = read_image(image)
    return image_to_base64(cv2.resize(image, size))

def normalize(image):
    # Normalization logic (e.g., scaling pixel values)
    image = read_image(image)
    normalized_image = image / 255.0  # Scale to [0, 1]
    # Rescale back to [0, 255] for display and convert to uint8
    display_image = (normalized_image * 255).astype(np.uint8)
    return image_to_base64(display_image)

def grayscaling(image):
    image = read_image(image)
    return image_to_base64(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))

def crop_image(image, crop_fraction=0.5):
    """Crop the image to a central square."""
    image = read_image(image)
    h, w = image.shape[:2]
    start_x = int(w * (1 - crop_fraction) / 2)
    start_y = int(h * (1 - crop_fraction) / 2)
    return image_to_base64(image[start_y:start_y + int(h * crop_fraction), start_x:start_x + int(w * crop_fraction)])

def denoise_image(image):
    """Reduce noise in the image using Gaussian Blur."""
    image = read_image(image)
    return image_to_base64(cv2.GaussianBlur(image, (5, 5), 0))

