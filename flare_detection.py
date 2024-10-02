import cv2
import numpy as np


color_range = {
    'red': [
        {'lower': np.array([0, 100, 100]), 'upper': np.array([10, 255, 255])},
        {'lower': np.array([160, 100, 100]), 'upper': np.array([180, 255, 255])}
    ],
    'yellow': {
        'lower': np.array([20, 150, 150]),
        'upper': np.array([30, 255, 255])
    },
    'blue': {
        'lower': np.array([94, 46, 189]),
        'upper': np.array([170, 255, 255])
    }
}


def detect_flare_color(image, color):
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = None
    if color == 'red':
        for i in color_range[color]:
            lower = i['lower']
            upper = i['upper']
            mask_part = cv2.inRange(hsv_img, lower, upper)
            mask = mask_part if mask is None else mask | mask_part
    else:
        lower = color_range[color]['lower']
        upper = color_range[color]['upper']
        mask = cv2.inRange(hsv_img, lower, upper)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) > 3000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return image


def detect_flares_in_order(image, flare_order):
    for flare_color in flare_order:
        print(f"Detecting {flare_color} flare")
        image_copy = image.copy()
        detected_image = detect_flare_color(image_copy, flare_color)
        cv2.imshow(f'{flare_color} Flare Detection', detected_image)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()
        
        
image = cv2.imread("flare_image.jpg")
color_1=input("Enter the first color: ")
color_2=input("Enter the second color: ")
color_3=input("Enter the third color: ")

color_order = [color_1, color_2, color_3]

detected_positions = detect_flares_in_order(image, color_order)
