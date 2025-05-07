import cv2
import numpy as np

NUM_SEGMENTS = 8
VALID_Y_MIN = 250
VALID_Y_MAX = 340
MAX_Y_DIFF_BETWEEN_SEGMENTS = 55

cap = cv2.VideoCapture("/dev/video2")

while True:
    ret, frame_bgr = cap.read()
    if not ret:
        break

    frame_bgr = cv2.resize(frame_bgr, (640, 480))
    frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

    # # Define yellow color range
    # lower_yellow_hsv = np.array([20, 100, 100])
    # upper_yellow_hsv = np.array([30, 255, 255])
    # yellow_mask = cv2.inRange(frame_hsv, lower_yellow_hsv, upper_yellow_hsv)


    # Define upper red range for your laser
    lower_red_hsv = np.array([170, 120, 140])   # slightly below your observed values
    upper_red_hsv = np.array([180, 160, 170])   # slightly above your observed values

    red_mask = cv2.inRange(frame_hsv, lower_red_hsv, upper_red_hsv)


    red_mask = cv2.GaussianBlur(red_mask, (3, 3), 0)

    image_height, image_width = red_mask.shape
    segment_pixel_width = image_width // NUM_SEGMENTS

    average_y_per_segment = []
    laser_broken = False

    cv2.rectangle(frame_bgr, (0, VALID_Y_MIN), (image_width, VALID_Y_MAX), (255, 255, 0), 1)

    for segment_index in range(NUM_SEGMENTS):
        x_start = segment_index * segment_pixel_width
        x_end = (segment_index + 1) * segment_pixel_width

        segment_mask = red_mask[:, x_start:x_end]
        yellow_pixels = cv2.findNonZero(segment_mask)

        if yellow_pixels is not None:
            avg_y = int(np.mean(yellow_pixels[:, 0, 1]))

            if VALID_Y_MIN <= avg_y <= VALID_Y_MAX:
                average_y_per_segment.append(avg_y)
                circle_color = (0, 255, 0)
            else:
                circle_color = (0, 0, 255)
                laser_broken = True
                cv2.putText(frame_bgr, "Out of range", (x_start + 2, VALID_Y_MIN - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, circle_color, 1)

            cv2.circle(frame_bgr, (x_start + segment_pixel_width // 2, avg_y), 3, circle_color, -1)
        else:
            laser_broken = True
            average_y_per_segment.append(None)
            cv2.putText(frame_bgr, "Missing", (x_start + 2, VALID_Y_MIN - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

    for i in range(1, len(average_y_per_segment)):
        if average_y_per_segment[i] is not None and average_y_per_segment[i - 1] is not None:
            y_diff = abs(average_y_per_segment[i] - average_y_per_segment[i - 1])
            if y_diff > MAX_Y_DIFF_BETWEEN_SEGMENTS:
                laser_broken = True
                cv2.line(frame_bgr,
                         (i * segment_pixel_width, average_y_per_segment[i]),
                         ((i - 1) * segment_pixel_width, average_y_per_segment[i - 1]),
                         (0, 0, 255), 2)

    if laser_broken:
        cv2.putText(frame_bgr, "Laser line broken!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    else:
        cv2.putText(frame_bgr, "Laser line OK", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Laser Monitor", frame_bgr)
    cv2.imshow("red Mask", red_mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()























# #  condition for execution:    the line laser marker have to be thought all the frame width.

# import cv2
# import numpy as np

# NUM_SEGMENTS = 8
# Y_MIN = 250
# Y_MAX = 340
# HEIGHT_DIFF_THRESHOLD = 55

# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     frame = cv2.resize(frame, (640, 480))
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#     # Yellow 
#     lower_yellow = np.array([20, 100, 100])
#     upper_yellow = np.array([30, 255, 255])
#     mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

#     mask = cv2.GaussianBlur(mask, (3, 3), 0)

#     height, width = mask.shape
#     segment_width = width // NUM_SEGMENTS

#     avg_ys = []
#     broken = False

#     cv2.rectangle(frame, (0, Y_MIN), (width, Y_MAX), (255, 255, 0), 1)

#     for i in range(NUM_SEGMENTS):
#         x_start = i * segment_width
#         x_end = (i + 1) * segment_width

#         segment = mask[:, x_start:x_end]
#         coords = cv2.findNonZero(segment)

#         if coords is not None:
#             avg_y = int(np.mean(coords[:, 0, 1]))

#             # Check if avg_y is in the valid laser range
#             if Y_MIN <= avg_y <= Y_MAX:
#                 avg_ys.append(avg_y)
#                 color = (0, 255, 0)
#             else:
#                 color = (0, 0, 255)
#                 broken = True
#                 cv2.putText(frame, "Out of range", (x_start + 2, Y_MIN - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

#             cv2.circle(frame, (x_start + segment_width // 2, avg_y), 3, color, -1)
#         else:
#             broken = True
#             avg_ys.append(None)
#             cv2.putText(frame, "Missing", (x_start + 2, Y_MIN - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

#     for i in range(1, len(avg_ys)):
#         if avg_ys[i] is not None and avg_ys[i - 1] is not None:
#             if abs(avg_ys[i] - avg_ys[i - 1]) > HEIGHT_DIFF_THRESHOLD:
#                 broken = True
#                 cv2.line(frame,
#                          (i * segment_width, avg_ys[i]),
#                          ((i - 1) * segment_width, avg_ys[i - 1]),
#                          (0, 0, 255), 2)

#     if broken:
#         cv2.putText(frame, "Laser line broken!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
#     else:
#         cv2.putText(frame, "Laser line OK", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

#     cv2.imshow("Laser Monitor", frame)
#     cv2.imshow("Mask", mask)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()







