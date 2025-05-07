import cv2
import tensorflow as tf
import numpy as np

# Load saved model
model = tf.keras.models.load_model('laser_line_model.h5')

labels = {0: "Straight", 1: "Broken line detected"}

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess
    resized = cv2.resize(frame, (256, 256))
    normalized = resized.astype("float32") / 255.0
    input_img = np.expand_dims(normalized, axis=0)

    # Predict
    prediction = model.predict(input_img)
    class_id = np.argmax(prediction[0])
    text = labels[class_id]

    # Draw label
    color = (0, 255, 0) if class_id == 0 else (0, 0, 255)
    cv2.putText(frame, text, (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # Show
    cv2.imshow('Laser Line Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

