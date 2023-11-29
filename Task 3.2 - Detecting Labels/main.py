import label_detector
from test_cases import test_cases


def main():
    for i in test_cases:
        print(label_detector.contains_label(i))


if __name__ == '__main__':
    main()
