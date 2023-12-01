# Command(s) with Zero parameter
CLEAR = "CLR"

# Command(s) with One parameter
PRINT = "YAZ"

# Command(s) with Two parameters
SAVE = "KAYDET"
ADD = "TOPLATUT"
SUBTRACT = "CIKARTUT"
MULTIPLY = "CARPTUT"
DIVIDE = "BOLTUT"
MOD = "MODTUT"

# Command(s) with Three parameters
IF = "EGER"


def get_symbol(command: str) -> str:
    if command == ADD:
        return "+"
    if command == SUBTRACT:
        return "-"
    if command == MULTIPLY:
        return "x"
    if command == DIVIDE:
        return "/"
    if command == MOD:
        return "%"
