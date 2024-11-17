import os
import csv
from PIL import Image
import matplotlib.pyplot as plt


IMAGES_FOLDER = './tensorflow_images'
IMAGE_LABELS = './tensorflow_images/labels.csv'


def label_images():
    print("Enter y/n for each image whether it is suitable for passport or not.\n")

    with open(IMAGE_LABELS, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ImageName', 'Label'])

        for image_name in os.listdir(IMAGES_FOLDER):
            if image_name.endswith(('.jpg', '.png')) is False:
                continue

            image_path = os.path.join(IMAGES_FOLDER, image_name)

            image = Image.open(image_path)

            plt.imshow(image)
            plt.axis('off')
            plt.show(block=False)

            user_input = input(f"{image_name}: ")
            image_status = True if user_input.lower() == 'y' else False

            writer.writerow([image_name, image_status])

            plt.close()


if __name__ == "__main__":
    label_images()
