import numpy as np
import cv2

def get_limits(color):
    """ Returns tight HSV limits for detecting an exact color. """
    c = np.uint8([[color]])  
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
    h = hsvC[0][0][0]  # Extract hue value

    # Narrow threshold for precise detection
    lower_limit = np.array([h - 10, 100, 100], dtype=np.uint8)
    upper_limit = np.array([h + 10, 255, 255], dtype=np.uint8)

    return lower_limit, upper_limit





