from os import path


def get_path_relative(relative_path: str) -> str:
    absolute_path = path.dirname(__file__)
    return path.join(absolute_path, relative_path)
