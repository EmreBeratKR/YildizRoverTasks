import label_detector
from test_cases import test_cases


def print_matrix(matrix: list[list[int]]) -> None:
    output = ""
    for i in range(0, len(matrix)):
        output += "|"
        for j in range(0, len(matrix[i])):
            output += "{:03d}".format(matrix[i][j]) + "|"
        if i < len(matrix) - 1:
            output += "\n"
    print(output)


def main():
    index = 0
    passed_count = 0
    for i in test_cases:
        index += 1
        matrix = i[0]
        expected_result = i[1]
        result = label_detector.contains_label(matrix)
        print(f"Case {index}: {result}")
        print(f"Expected result: {expected_result}")
        if expected_result == result:
            passed_count += 1
            print("Passed!")
        else:
            print("Failed!")
        print_matrix(matrix)
        print('-' * 100)
    print(f"{passed_count}/{index} cases are passed!")


if __name__ == '__main__':
    main()
