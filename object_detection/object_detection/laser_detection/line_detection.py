
import cv2
import numpy as np
from util import get_limits  
import datetime

# green in BGR (Blue, Green, Red)
green = [0, 255, 0]  

cap = cv2.VideoCapture(0)

def timeStamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

line_thickness = 10  

while True:
    ret, frame = cap.read()
    if not ret:
        break  

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lowerLimit, upperLimit = get_limits(color=green)  
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit) 


    blurred = cv2.GaussianBlur(mask, (5, 5), 0)  
    edges = cv2.Canny(blurred, 50, 150)  

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=10, minLineLength=50, maxLineGap=10)

    detected_straight_line = False  
    if lines is not None:
        detected_straight_line = True
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), line_thickness)

    if detected_straight_line:
        print(f"Straight line detected at {timeStamp()}")

    scale_percent = 50 
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    resized_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

    resized_mask = cv2.resize(mask, (width, height), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', resized_mask)
    cv2.imshow('frame', resized_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()















# import cv2
# import numpy as np
# from PIL import Image
# from util import get_limits  
# import datetime

# # Exact green in BGR (Blue, Green, Red)
# green = [0, 255, 0]  

# cap = cv2.VideoCapture(0)

# def timeStamp():
#     return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

# # Line thickness variable
# line_thickness = 7 

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break  

#     hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#     lowerLimit, upperLimit = get_limits(color=green)  
#     mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)  

#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     detected_straight_line = False  

#     for contour in contours:
#         epsilon = 0.02 * cv2.arcLength(contour, True)
#         approx = cv2.approxPolyDP(contour, epsilon, True)

#         if len(approx) == 6: 
#             x1, y1 = approx[0][0]
#             x2, y2 = approx[1][0]
#             cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), line_thickness)
#             detected_straight_line = True  

#     if detected_straight_line:
#         print("Straight line is detected " + timeStamp())

#     scale_percent = 50 
#     width = int(frame.shape[1] * scale_percent / 100)
#     height = int(frame.shape[0] * scale_percent / 100)
#     resized_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

#     cv2.imshow('frame', resized_frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

