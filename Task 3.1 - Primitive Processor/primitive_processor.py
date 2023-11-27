from os import system
import commands as cmd
import constants as const
import conditions as condition


class PrimitiveProcessor:
    __memory: list[float]
    __isRunning: bool

    def __init__(self):
        self.__initialize_memory()
        self.__run()

    def update(self) -> None:
        prompt = self.__get_prompt()
        self.__process_prompt(prompt)

    def is_running(self) -> bool:
        return self.__isRunning

    def __get_memory_index(self, memory_address: str) -> int:
        if len(memory_address) != 2 or memory_address[0] != "H":
            return const.NULL_INDEX
        try:
            raw_index = int(memory_address[1]) - 1
            if raw_index >= len(self.__memory):
                return const.NULL_INDEX
            return raw_index
        except ValueError:
            return const.NULL_INDEX

    def __get_memory_data(self, index: int) -> float:
        return self.__memory[index]

    def __set_memory_data(self, index: int, value: float) -> None:
        self.__memory[index] = value

    def __process_clear_command(self) -> None:
        system('cls')

    def __evaluate_math_operation(self, param_0: float, param_1: float, operation: str) -> float:
        if operation == cmd.ADD:
            return param_0 + param_1
        if operation == cmd.SUBTRACT:
            return param_0 - param_1
        if operation == cmd.MULTIPLY:
            return param_0 * param_1
        if operation == cmd.DIVIDE:
            return param_0 / param_1
        if operation == cmd.MOD:
            return param_0 % param_1

    def __evaluate_equality_operation(self, param_0: float, param_1: float, cond: str) -> bool:
        if cond == condition.EQUALS:
            return param_0 == param_1
        if cond == condition.NOT_EQUALS:
            return param_0 != param_1
        if cond == condition.GREATER:
            return param_0 > param_1
        if cond == condition.GREATER_OR_EQUALS:
            return param_0 >= param_1
        if cond == condition.SMALLER:
            return param_0 < param_1
        if cond == condition.SMALLER_OR_EQUALS:
            return param_0 <= param_1

    def __try_process_print_command(self, param_0: str) -> bool:
        memory_index = self.__get_memory_index(param_0)
        if memory_index == const.NULL_INDEX:
            return False
        data = self.__get_memory_data(memory_index)
        print(f"[{param_0}]: {data}")

    def __try_process_save_command(self, param_0: str, param_1: str) -> bool:
        write_memory_index = self.__get_memory_index(param_0)
        read_memory_index = self.__get_memory_index(param_1)
        if write_memory_index == const.NULL_INDEX:
            return False
        if read_memory_index != const.NULL_INDEX:
            data = self.__get_memory_data(read_memory_index)
            self.__set_memory_data(write_memory_index, data)
            return True
        try:
            data = float(param_1)
            self.__set_memory_data(write_memory_index, data)
            return True
        except ValueError:
            return False

    def __try_process_math_operation_command(self, param_0: str, param_1: str, operation: str) -> bool:
        write_memory_index = self.__get_memory_index(param_0)
        read_memory_index = self.__get_memory_index(param_1)
        if write_memory_index == const.NULL_INDEX:
            return False
        data = self.__get_memory_data(write_memory_index)
        if read_memory_index != const.NULL_INDEX:
            second_data = self.__get_memory_data(read_memory_index)
            data = self.__evaluate_math_operation(data, second_data, operation)
            self.__set_memory_data(write_memory_index, data)
            return True
        try:
            second_data = float(param_1)
            data = self.__evaluate_math_operation(data, second_data, operation)
            self.__set_memory_data(write_memory_index, data)
            return True
        except ValueError:
            return False

    def __try_proces_if_command(self, param_0: str, param_1: str, param_2: str) -> bool:
        cond = param_0
        if not condition.is_valid_condition(cond):
            return False
        memory_index_0 = self.__get_memory_index(param_1)
        memory_index_1 = self.__get_memory_index(param_2)
        try:
            if memory_index_0 != const.NULL_INDEX:
                data_0 = self.__get_memory_data(memory_index_0)
            else:
                data_0 = float(param_1)
            if memory_index_1 != const.NULL_INDEX:
                data_1 = self.__get_memory_data(memory_index_1)
            else:
                data_1 = float(param_2)
            result = self.__evaluate_equality_operation(data_0, data_1, cond)
            print(result)
            return True
        except ValueError:
            return False

    def __try_process_command_with_zero_params(self, command: str) -> bool:
        if command == cmd.CLEAR:
            self.__process_clear_command()
            return True
        return False

    def __try_process_command_with_one_params(self, command: str, param_0: str) -> bool:
        if command == cmd.PRINT:
            return self.__try_process_print_command(param_0)
        return False

    def __try_process_command_with_two_params(self, command: str, param_0: str, param_1: str) -> bool:
        if command == cmd.SAVE:
            return self.__try_process_save_command(param_0, param_1)
        if command == cmd.ADD:
            return self.__try_process_math_operation_command(param_0, param_1, cmd.ADD)
        if command == cmd.SUBTRACT:
            return self.__try_process_math_operation_command(param_0, param_1, cmd.SUBTRACT)
        if command == cmd.MULTIPLY:
            return self.__try_process_math_operation_command(param_0, param_1, cmd.MULTIPLY)
        if command == cmd.DIVIDE:
            return self.__try_process_math_operation_command(param_0, param_1, cmd.DIVIDE)
        if command == cmd.MOD:
            return self.__try_process_math_operation_command(param_0, param_1, cmd.MOD)
        return False

    def __try_process_command_with_three_params(self, command: str, param_0: str, param_1: str, param_2: str) -> bool:
        if command == cmd.IF:
            return self.__try_proces_if_command(param_0, param_1, param_2)
        return False

    def __process_invalid_prompt(self, prompt: str) -> None:
        print(f"Invalid prompt = [{prompt}]")

    def __process_prompt(self, prompt: str) -> None:
        split_with_space = prompt.split(' ')
        command = split_with_space[0]
        if len(split_with_space) == 1:
            if not self.__try_process_command_with_zero_params(command):
                self.__process_invalid_prompt(prompt)
            return None
        params = split_with_space[1].split(',')
        if len(params) == 1:
            if self.__try_process_command_with_one_params(command, params[0]):
                self.__process_invalid_prompt(prompt)
            return None
        if len(params) == 2:
            if not self.__try_process_command_with_two_params(command, params[0], params[1]):
                self.__process_invalid_prompt(prompt)
            return None
        if len(params) == 3:
            if not self.__try_process_command_with_three_params(command, params[0], params[1], params[2]):
                self.__process_invalid_prompt(prompt)
            return None
        self.__process_invalid_prompt(prompt)

    def __get_prompt(self) -> str:
        return input("Enter Prompt >")

    def __run(self) -> None:
        self.__isRunning = True

    def __initialize_memory(self) -> None:
        self.__memory = [0.0, 0.0, 0.0]

    def __quit(self) -> None:
        self.__isRunning = False
