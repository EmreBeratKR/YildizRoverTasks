from primitive_processor import PrimitiveProcessor


def main():
    processor = PrimitiveProcessor()
    while processor.is_running():
        processor.update()


if __name__ == '__main__':
    main()
