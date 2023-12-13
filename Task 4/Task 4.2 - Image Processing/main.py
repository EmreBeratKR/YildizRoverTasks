from os import path as os_path
import cv2
import matplotlib
import matplotlib.pyplot as plt


QUESTION_PADDING_TOP = -20
QUESTION_PADDING_BOTTOM = -20
QUESTION_WIDTH = 640
MIN_VERTICAL_GAP_BETWEEN_QUESTIONS = 50

NUMBER_COLORS = [(255, 5, 255), (211, 2, 121), (242, 1, 146), (231, 8, 134)]
BLANK_COLOR = (255, 255, 255)
COLOR_EQUALITY_THRESHOLD = 5

DETECTION_RECT_COLOR = (0, 255, 0)
DETECTION_RECT_THICKNESS = 2

ROW_WIDTH = 50
ROW_POS_Y = 150
LEFT_ROW_POS = (120, ROW_POS_Y)
RIGHT_ROW_POS = (790, ROW_POS_Y)
SHOW_CROPPED_ROWS = False


def get_path_relative(relative_path: str) -> str:
    absolute_path = os_path.dirname(__file__)
    return os_path.join(absolute_path, relative_path)


def is_similar_color(pixel_a: (int, int, int), pixel_b: (int, int, int)) -> bool:
    delta_r = pixel_a[0] - pixel_b[0]
    delta_g = pixel_a[1] - pixel_b[1]
    delta_b = pixel_a[2] - pixel_b[2]
    return ((delta_r ** 2 + delta_g ** 2 + delta_b ** 2) ** 0.5) <= COLOR_EQUALITY_THRESHOLD


def is_number_color(color: (int, int, int)) -> bool:
    for i in NUMBER_COLORS:
        if is_similar_color(color, i):
            return True
    return False


def show_image(img, name: str = "Image") -> None:
    matplotlib.use('TkAgg')
    plt.figure(name)
    plt.subplot(1, 1, 1)
    plt.imshow(img)
    plt.show()


def detect_questions_in_row(img, start_pos: (int, int), rect: (int, int)) -> None:
    x, y = start_pos
    width, height = rect
    end_x = x + width
    end_y = y + height
    question_positions = []
    if SHOW_CROPPED_ROWS:
        crop = img[y:end_y, x:end_x]
        show_image(crop)
    while y < end_y:
        while x < end_x:
            pixel = img[y, x]
            if is_number_color(pixel):
                question_positions.append((start_pos[0], y + QUESTION_PADDING_TOP))
                y += 100
                break
            x += 1
        x = start_pos[0]
        y += 1

    for question_pos in question_positions:
        height = calculate_question_height(img, question_pos)
        rect = (question_pos[0] + QUESTION_WIDTH, question_pos[1] + height)
        cv2.rectangle(img, question_pos, rect, DETECTION_RECT_COLOR, DETECTION_RECT_THICKNESS)


def calculate_question_height(img, pos: (int, int)) -> int:
    x, y = pos
    target_height = y + MIN_VERTICAL_GAP_BETWEEN_QUESTIONS
    target_width = x + QUESTION_WIDTH
    while True:
        is_valid = True
        while y < target_height:
            while x < target_width:
                pixel = img[y, x]
                if not is_similar_color(pixel, BLANK_COLOR):
                    is_valid = False
                    break
                x += 1
            if not is_valid:
                y += 1
                target_height = y + MIN_VERTICAL_GAP_BETWEEN_QUESTIONS
                break
            x = pos[0]
            y += 1
        if is_valid:
            height = target_height - pos[1] - MIN_VERTICAL_GAP_BETWEEN_QUESTIONS
            return height - QUESTION_PADDING_BOTTOM


def main():
    for i in range(6):
        img_path = get_path_relative(f"Pages/page_{i}.png")
        img = cv2.imread(img_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, _ = img_rgb.shape

        row_rect = (ROW_WIDTH, height - ROW_POS_Y)
        detect_questions_in_row(img_rgb, LEFT_ROW_POS, row_rect)
        detect_questions_in_row(img_rgb, RIGHT_ROW_POS, row_rect)

        show_image(img_rgb, f"Page {i}")


if __name__ == '__main__':
    main()
