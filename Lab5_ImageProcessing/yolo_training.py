import os
import random
from ultralytics import YOLO


IMAGES_FOLDER = "opencv_images"
TRAIN_DATASET_FILE = os.path.join(IMAGES_FOLDER, "train.txt")
VALIDATION_DATASET_FILE = os.path.join(IMAGES_FOLDER, "validation.txt")

images = [f for f in os.listdir(IMAGES_FOLDER) if f.endswith(('.jpg', '.png'))]
random.shuffle(images)

split_index = int(0.7 * len(images))
train_data = images[:split_index]
validation_data = images[split_index:]


def write_split(file_list, output_file):
    with open(output_file, "w") as f:
        for image_name in file_list:
            f.write(os.path.join(IMAGES_FOLDER, image_name) + "\n")


write_split(train_data, TRAIN_DATASET_FILE)
write_split(validation_data, VALIDATION_DATASET_FILE)

model = YOLO("yolov8s.pt")

model.train(
    data="data.yml",
    epochs=50,
    imgsz=256,
    batch=16,
    workers=4,
    name="passport_validation_model"
)
