import cv2
import numpy as np

def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        hsv_frame = param
        if y < hsv_frame.shape[0] and x < hsv_frame.shape[1]:
            hsv_pixel = hsv_frame[y, x]
            h, s, v = hsv_pixel
            print(f"HSV at ({x},{y}): H={h}, S={s}, V={v}")

cap = cv2.VideoCapture("/dev/video2")  # or 0 for default webcam

if not cap.isOpened():
    print("Failed to open camera.")
    exit()

cv2.namedWindow("HSV")

while True:
    ret, frame_bgr = cap.read()
    if not ret:
        break

    frame_bgr = cv2.resize(frame_bgr, (640, 480))
    frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

    # Set the mouse callback to access HSV values
    cv2.setMouseCallback("HSV", on_mouse, frame_hsv)

    # Show the HSV image
    hsv_visual = cv2.cvtColor(frame_hsv, cv2.COLOR_HSV2BGR)  # To show nicely
    cv2.imshow("HSV", hsv_visual)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
