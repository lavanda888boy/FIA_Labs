import pandas as pd
import tensorflow as tf
import cv2
import os
import numpy as np
from yolo_passport_validation import is_valid_for_passport
from ultralytics import YOLO


IMAGES = './test_dataset/images'
IMAGE_LABELS = './test_dataset/labels.csv'

data = pd.read_csv(IMAGE_LABELS)
data['Label'] = data['Label'].astype(str)

test_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255).flow_from_dataframe(
        dataframe=data,
        directory=IMAGES,
        x_col="ImageName",
        y_col="Label",
        target_size=(128, 128),
        class_mode="binary",
        batch_size=32,
        shuffle=True,
        width_shift_range=0.3,
        height_shift_range=0.3,
        zoom_range=0.3,
)

cnn_model = tf.keras.models.load_model('./models/face_detection_cnn.keras')
cnn_predictions = cnn_model.predict(test_generator, verbose=1)
cnn_predictions = (cnn_predictions > 0.5).astype(int)

yolo_model = YOLO('./models/face_detection_yolo.pt')
yolo_predictions = []

for i in range(len(data)):
    image_path = os.path.join(IMAGES, data['ImageName'][i])
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    results = yolo_model.predict(image_path)
    annotations = []

    for box in results[0].boxes:
        class_id = int(box.cls.item())
        class_name = results[0].names[class_id]

        x_center, y_center, bbox_width, bbox_height = box.xywh.numpy().flatten()

        x_center_normalized = x_center / width
        y_center_normalized = y_center / height
        bbox_width_normalized = bbox_width / width
        bbox_height_normalized = bbox_height / height

        annotations.append((class_id, x_center_normalized, y_center_normalized,
                           bbox_width_normalized, bbox_height_normalized))

        x1 = int(x_center - bbox_width / 2)
        y1 = int(y_center - bbox_height / 2)
        x2 = int(x_center + bbox_width / 2)
        y2 = int(y_center + bbox_height / 2)

        color = (0, 255, 0) if class_name == "face" else (255, 0, 0)
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, class_name, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    is_valid = is_valid_for_passport(image_path, annotations)
    yolo_predictions.append(int(is_valid))

    validity_label = "Valid" if is_valid else "Invalid"
    label_color = (0, 255, 0) if is_valid else (0, 0, 255)
    cv2.putText(image, validity_label, (10, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, label_color, 3)

    cv2.imshow("YOLO Passport Validation", image)

    key = cv2.waitKey(0)
    if key == 27:
        break

cv2.destroyAllWindows()

true_labels = test_generator.labels
cnn_correct_predictions = np.sum(cnn_predictions.flatten() == true_labels)
yolo_correct_predictions = np.sum(np.array(yolo_predictions) == true_labels)

cnn_accuracy = cnn_correct_predictions / len(true_labels)
yolo_accuracy = yolo_correct_predictions / len(true_labels)

print(f"Tensorflow CNN Test Accuracy: {cnn_accuracy:.3f}")
print(f"YOLO Test Accuracy: {yolo_accuracy:.3f}")
