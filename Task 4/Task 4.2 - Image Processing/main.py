from os import path as os_path
import cv2
import matplotlib
import matplotlib.pyplot as plt


NUMBER_COLORS = [(255, 5, 255), (211, 2, 121), (242, 1, 146), (231, 8, 134)]


def get_path_relative(relative_path: str) -> str:
    absolute_path = os_path.dirname(__file__)
    return os_path.join(absolute_path, relative_path)


def is_similar_color(pixel_a, pixel_b):
    delta_r = pixel_a[0] - pixel_b[0]
    delta_g = pixel_a[1] - pixel_b[1]
    delta_b = pixel_a[2] - pixel_b[2]
    return ((delta_r ** 2 + delta_g ** 2 + delta_b ** 2) ** 0.5) <= 5


def is_number_color(color):
    for i in NUMBER_COLORS:
        if is_similar_color(color, i):
            return True
    return False


def show_image(img, name="Image"):
    matplotlib.use('TkAgg')
    plt.figure(name)
    plt.subplot(1, 1, 1)
    plt.imshow(img)
    plt.show()


def detect_questions_in_row(img, start_pos, rect):
    x, y = start_pos
    width, height = rect
    end_x = x + width
    end_y = y + height
    questions = []
    #crop = img[y:end_y, x:end_x]
    #show_image(crop)
    while y < end_y:
        while x < end_x:
            pixel = img[y, x]
            if is_number_color(pixel):
                questions.append((start_pos[0], y))
                y += 100
                break
            x += 1
        x = start_pos[0]
        y += 1

    for question in questions:
        cv2.rectangle(img, question, (question[0] + 640, question[1] + 500), (0, 255, 0), 2)


def main():
    for i in range(6):
        img_path = get_path_relative(f"Pages/page_{i}.png")
        img = cv2.imread(img_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, _ = img_rgb.shape

        row_rect = (50, height - 300)
        detect_questions_in_row(img_rgb, (120, 150), row_rect)
        detect_questions_in_row(img_rgb, (790, 150), row_rect)

        show_image(img_rgb, f"Page {i}")


if __name__ == '__main__':
    main()
