EQUALS = "=="
NOT_EQUALS = "!="
GREATER = ">"
GREATER_OR_EQUALS = ">="
SMALLER = "<"
SMALLER_OR_EQUALS = "<="


def is_valid_condition(cond: str) -> bool:
    if cond == EQUALS:
        return True
    if cond == NOT_EQUALS:
        return True
    if cond == GREATER:
        return True
    if cond == GREATER_OR_EQUALS:
        return True
    if cond == SMALLER:
        return True
    if cond == SMALLER_OR_EQUALS:
        return True
    return False
