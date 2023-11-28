def invalid_memory(memory: str) -> str:
    return f"[Invalid memory][{memory}]"


def invalid_memory_or_value(memory: str) -> str:
    return f"[Invalid memory or value][{memory}]"


def save_value_to_memory(memory: str, other_memory: str, value: float) -> str:
    if other_memory is None:
        return f"[Save value to memory][{value} -> {memory}]"
    return f"[Save value to memory][{other_memory}={value}] -> {memory}"


def print_value_of_memory(memory: str, value: float) -> str:
    return f"[Print memory][{memory}]: {value}"


def math_operation(a: str, b: str, value: float, symbol: str) -> str:
    return f"[{a} {symbol} {b} = {value}]"


def invalid_condition(condition: str):
    return f"[Invalid Condition][{condition}]"


def if_condition(a: str, b: str, condition: str, value: bool):
    return f"[{a} {condition} {b} = {value}]"
