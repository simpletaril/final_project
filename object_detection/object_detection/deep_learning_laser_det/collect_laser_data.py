import cv2
import os
import random

# Define where to save the dataset
BASE_DIR = "dataset"
CLASSES = ["straight", "interrupted"]
SPLITS = ["train", "val"]
VAL_RATIO = 0.2  # 20% of the data will go to validation

# Create folder structure if it doesn't exist
for split in SPLITS:
    for cls in CLASSES:
        os.makedirs(os.path.join(BASE_DIR, split, cls), exist_ok=True)

# Function to get the next image number
def get_next_index(path, prefix):
    files = [f for f in os.listdir(path) if f.startswith(prefix) and f.endswith('.jpg')]
    indices = [int(f.split('_')[1].split('.')[0]) for f in files if '_' in f]
    return max(indices) + 1 if indices else 1

# Open the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Press 's' to save a STRAIGHT laser image")
print("Press 'i' to save an INTERRUPTED laser image")
print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize to 256x256 (match your model input)
    resized_frame = cv2.resize(frame, (256, 256))

    # Show live video
    cv2.imshow("Laser Line Dataset Collector", resized_frame)

    # Handle key press
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    elif key == ord('s') or key == ord('i'):
        label = "straight" if key == ord('s') else "interrupted"
        split = "val" if random.random() < VAL_RATIO else "train"

        folder_path = os.path.join(BASE_DIR, split, label)
        index = get_next_index(folder_path, label)
        filename = f"{label}_{index}.jpg"
        save_path = os.path.join(folder_path, filename)

        cv2.imwrite(save_path, resized_frame)
        print(f"[SAVED] {save_path}")

cap.release()
cv2.destroyAllWindows()
