import time
from os import path as os_path
import cv2
import matplotlib
import matplotlib.pyplot as plt
import numpy


PAGE_COUNT = 6
QUESTION_PADDING_TOP = -20
QUESTION_PADDING_BOTTOM = -20
QUESTION_WIDTH = 640
MIN_VERTICAL_GAP_BETWEEN_QUESTIONS = 50
MAX_QUESTION_COUNT_PER_COLUMN = 2
CALCULATE_QUESTION_HEIGHT_PRECISELY = False  # True: Precise / False: Fast

NUMBER_COLORS = [(255, 5, 255), (211, 2, 121), (242, 1, 146), (231, 8, 134)]
BLANK_COLOR = (255, 255, 255)
COLOR_EQUALITY_THRESHOLD = 5

DETECTION_RECT_COLOR = (0, 255, 0)
DETECTION_RECT_THICKNESS = 2

COLUMN_WIDTH = 50
COLUMN_POS_Y = 150
LEFT_COLUMN_POS = (120, COLUMN_POS_Y)
RIGHT_COLUMN_POS = (790, COLUMN_POS_Y)
SHOW_CROPPED_COLUMNS = False


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


def detect_questions_in_column(img, start_pos: (int, int), rect: (int, int)):
    x, y = start_pos
    width, height = rect
    end_x = x + width
    end_y = y + height
    question_positions = []
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    timer = time.time()
    if SHOW_CROPPED_COLUMNS:
        crop = img[y:end_y, x:end_x]
        show_image(crop)
    while y < end_y:
        while x < end_x:
            pixel = img_rgb[y, x]
            if is_number_color(pixel):
                question_positions.append((start_pos[0], y + QUESTION_PADDING_TOP))
                y += 100
                break
            x += 1
        if len(question_positions) >= MAX_QUESTION_COUNT_PER_COLUMN:
            break
        x = start_pos[0]
        y += 1
    print(f"Found all numbers in {time.time() - timer} seconds!")
    question_images = []
    for question_pos in question_positions:
        timer = time.time()
        height = calculate_question_height(img, question_pos)
        print(f"Calculate height in {time.time() - timer} seconds!")
        rect = (question_pos[0] + QUESTION_WIDTH, question_pos[1] + height)
        question_image = img_rgb[question_pos[1]:rect[1], question_pos[0]:rect[0]]
        question_images.append(question_image)
        cv2.rectangle(img, question_pos, rect, DETECTION_RECT_COLOR, DETECTION_RECT_THICKNESS)
    return question_images


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
                if CALCULATE_QUESTION_HEIGHT_PRECISELY:
                    y += 1
                    target_height = y + MIN_VERTICAL_GAP_BETWEEN_QUESTIONS
                else:
                    y = target_height
                    target_height += MIN_VERTICAL_GAP_BETWEEN_QUESTIONS
                break
            x = pos[0]
            y += 1
        if is_valid:
            height = target_height - pos[1] - MIN_VERTICAL_GAP_BETWEEN_QUESTIONS
            return height - QUESTION_PADDING_BOTTOM


def find_all_questions(img):
    height, width = img.shape[:2]
    row_rect = (COLUMN_WIDTH, height - COLUMN_POS_Y)
    left_side_questions = detect_questions_in_column(img, LEFT_COLUMN_POS, row_rect)
    right_side_questions = detect_questions_in_column(img, RIGHT_COLUMN_POS, row_rect)
    return left_side_questions + right_side_questions


def find_and_show_all_questions():
    for i in range(PAGE_COUNT):
        img_path = get_path_relative(f"Pages/page_{i}.png")
        img = cv2.imread(img_path)
        find_all_questions(img)
        show_image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def find_second_question(img):
    height, width = img.shape[:2]
    row_rect = (COLUMN_WIDTH, height - COLUMN_POS_Y)
    left_side_questions = detect_questions_in_column(img, LEFT_COLUMN_POS, row_rect)
    second_question = left_side_questions[1]
    return second_question


def get_number_image(number: int):
    img_path = get_path_relative(f"Numbers/{number}.png")
    img = cv2.imread(img_path, cv2.COLOR_BGR2RGB)
    return img


def create_test_from_second_questions():
    middle_gap = 50
    questions = []
    # detect questions
    for i in range(PAGE_COUNT):
        img_path = get_path_relative(f"Pages/page_{i}.png")
        img = cv2.imread(img_path)
        question = find_second_question(img)
        number = get_number_image(i + 1)
        number_height, number_width = number.shape[:2]
        question[:number_height, :number_width, :3] = number
        questions.append(question)
        print(f"[{i + 1}/{PAGE_COUNT}] Detected a Question!")
    # separate questions by 2 columns
    middle_index = int(len(questions) / 2)
    test_left = cv2.vconcat(questions[:middle_index])
    h1, w1 = test_left.shape[:2]
    test_right = cv2.vconcat(questions[middle_index:])
    h2, w2 = test_right.shape[:2]
    # load banner image
    banner_path = get_path_relative("test_banner.png")
    banner_img_rgb = cv2.imread(banner_path, cv2.COLOR_BGR2RGB)
    banner_height, banner_width = banner_img_rgb.shape[:2]
    banner_margin = int((w1 + w2 - banner_width + middle_gap) / 2)
    # create pixel matrix for output test
    test_height = max(h1, h2) + banner_height
    test_width = w1 + w2 + middle_gap
    test = numpy.full((test_height, test_width, 3), 255, numpy.uint8)
    # set pixels
    test[:banner_height, banner_margin:banner_margin + banner_width, :3] = banner_img_rgb
    test[banner_height:banner_height + h1, :w1, :3] = test_left
    test[banner_height:banner_height + h2, w1 + middle_gap:w1 + middle_gap + w2, :3] = test_right
    save_path = get_path_relative("output_test.png")
    cv2.imwrite(save_path, cv2.cvtColor(test, cv2.COLOR_RGB2BGR))
    show_image(test)


def main():
    create_test_from_second_questions()


if __name__ == '__main__':
    main()
