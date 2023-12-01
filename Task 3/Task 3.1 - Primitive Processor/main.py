from primitive_processor import PrimitiveProcessor
import path_utils as path


def main():
    processor = PrimitiveProcessor()
    instructions_path = path.get_path_relative("instructions/instructions_0")
    processor.run_instructions_from_path(instructions_path)
    instructions_path = path.get_path_relative("instructions/instructions_1")
    processor.run_instructions_from_path(instructions_path)


if __name__ == '__main__':
    main()
