from path_utils import get_path_relative
from PIL import Image
import cv2
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def is_similar(pixel_a, pixel_b):
    delta_r = pixel_a[0] - pixel_b[0]
    delta_g = pixel_a[1] - pixel_b[1]
    delta_b = pixel_a[2] - pixel_b[2]
    return ((delta_r ** 2 + delta_g ** 2 + delta_b ** 2) ** 0.5) <= 3.5


def test():
    path = get_path_relative("Pages/page_0.jpeg")
    image = Image.open(path)
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            pixel = pixels[x, y]
            is_similarr = is_similar(pixel, (210, 21, 129))
            if is_similarr:
                print(pixel)


def main():
    img_path = get_path_relative("image.png")
    img = cv2.imread(img_path)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    path = get_path_relative("stop_data.xml")
    stop_data = cv2.CascadeClassifier(path)
    found = stop_data.detectMultiScale(img_gray, minSize=(20, 20))
    amount_found = len(found)

    if amount_found != 0:
        for (x, y, width, height) in found:
            cv2.rectangle(img_rgb, (x, y),
                          (x + height, y + width),
                          (0, 255, 0), 5)

    plt.subplot(1, 1, 1)
    plt.imshow(img_rgb)
    plt.show()


if __name__ == '__main__':
    main()
