class PrimitiveMemory:
    __value: float
    __initialized: bool

    def __init__(self):
        self.__value = 0.0
        self.__initialized = False

    def get_value(self) -> float:
        return self.__value

    def set_value(self, value: float) -> None:
        self.__value = value
        self.__initialized = True

    def is_initialized(self) -> bool:
        return self.__initialized
