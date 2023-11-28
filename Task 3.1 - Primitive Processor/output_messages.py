def invalid_memory(memory: str) -> str:
    return f"Invalid memory: [{memory}]"


def uninitialized_memory(memory: str) -> str:
    return f"Uninitialized memory: [{memory}]"


def invalid_value(memory: str) -> str:
    return f"Invalid value: [{memory}]"


def invalid_parameter_count(command: str, count: int, valid_count: int) -> str:
    return f"Command [{command}] accepts {valid_count} parameter(s) but {count} is given"


def save_value_to_memory(memory: str, value: float) -> str:
    return f"{value} -> {memory}"


def print_value_of_memory(memory: str, value: float) -> str:
    return f"[{memory}]={value}"


def math_operation(a: str, b: str, value: float, symbol: str) -> str:
    return f"{a} {symbol} {b} = {value} | {save_value_to_memory(a, value)}"


def invalid_condition(condition: str):
    return f"Invalid Condition: [{condition}"


def if_condition(a: str, b: str, condition: str, value: bool):
    return f"{a} {condition} {b} = {value}"


def zero_division_error(a: str, b: str, symbol: str) -> str:
    return f"[{a} {symbol} {b}] yields zero division error"


def skip_instruction(instruction: str):
    return f"Skip [{instruction}]"
