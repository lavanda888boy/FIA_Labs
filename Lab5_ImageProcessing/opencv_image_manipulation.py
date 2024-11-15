import cv2 as cv
import matplotlib.pyplot as plt


def blur_image(image_path, blur_kernel_size=(7, 7)):
    image = cv.imread(image_path)
    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    blur = cv.blur(image, blur_kernel_size)
    blur_rgb = cv.cvtColor(blur, cv.COLOR_BGR2RGB)

    plt.subplot(1, 2, 1)
    plt.imshow(image_rgb)
    plt.title('Original')

    plt.subplot(1, 2, 2)
    plt.imshow(blur_rgb)
    plt.title('Blurred')
    plt.show()


def sharpen_image(image_path, blur_kernel_size=(7, 7), alpha=2,
                  beta=-1):
    image = cv.imread(image_path)
    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    blur = cv.blur(image, blur_kernel_size)
    sharp = cv.addWeighted(image, alpha,
                           blur, beta, 0)
    sharp_rgb = cv.cvtColor(sharp, cv.COLOR_BGR2RGB)

    plt.subplot(1, 2, 1)
    plt.imshow(image_rgb)
    plt.title('Original')

    plt.subplot(1, 2, 2)
    plt.imshow(sharp_rgb)
    plt.title('Sharpened')
    plt.show()


if __name__ == "__main__":
    blur_image('example.jpg')
    sharpen_image('example.jpg')
