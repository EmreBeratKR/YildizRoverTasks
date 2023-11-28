from os import system, path as os_path
import commands as cmd
import constants as const
import conditions as condition
import output_messages as output_msg


class PrimitiveProcessor:
    __logs: list[str]
    __memory: list[float]

    def __init__(self):
        self.__initialize_memory()

    def run_instructions_from_path(self, path: str) -> None:
        self.__logs = []
        file = open(path, "r")
        instructions = []
        output = ""
        try:
            first_line = file.readline()
            base_path = os_path.split(path)
            output_path = ""
            for i in range(0, len(base_path) - 1):
                output_path = os_path.join(output_path, base_path[i])
            output_path = os_path.join(output_path, first_line.split('=')[1].split('"')[1])
        except:
            print(f"Syntax error at line 1:\n{first_line}")
        n = 0
        for line in file:
            instruction = line[0:-1]
            instructions.append(instruction)
            if not self.__try_process_instruction(instruction):
                print(f"Syntax error at line {n}:\n{line}")
            n += 1
        for i in range(0, len(instructions)):
            output += f"[{i}][IN]: {instructions[i]}\n"
            output += f"[{i}][OUT]: {self.__logs[i]}\n"
        file.close()
        log_file = open(output_path, "w")
        log_file.write(output)
        log_file.close()
        print(f"Log file has been written to path:\n[{output_path}]")

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
        self.__log("[Clear Console]")

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
            self.__log(output_msg.invalid_memory(param_0))
            return False
        data = self.__get_memory_data(memory_index)
        self.__log(output_msg.print_value_of_memory(param_0, data))
        return True

    def __try_process_save_command(self, param_0: str, param_1: str) -> bool:
        write_memory_index = self.__get_memory_index(param_0)
        read_memory_index = self.__get_memory_index(param_1)
        if write_memory_index == const.NULL_INDEX:
            self.__log(output_msg.invalid_memory(param_0))
            return False
        if read_memory_index != const.NULL_INDEX:
            data = self.__get_memory_data(read_memory_index)
            self.__set_memory_data(write_memory_index, data)
            self.__log(output_msg.save_value_to_memory(param_0, param_1, data))
            return True
        try:
            data = float(param_1)
            self.__set_memory_data(write_memory_index, data)
            self.__log(output_msg.save_value_to_memory(param_0, None, data))
            return True
        except ValueError:
            self.__log(output_msg.invalid_memory_or_value(param_1))
            return False

    def __try_process_math_operation_command(self, param_0: str, param_1: str, operation: str) -> bool:
        write_memory_index = self.__get_memory_index(param_0)
        read_memory_index = self.__get_memory_index(param_1)
        if write_memory_index == const.NULL_INDEX:
            self.__log(output_msg.invalid_memory(param_0))
            return False
        data = self.__get_memory_data(write_memory_index)
        if read_memory_index != const.NULL_INDEX:
            second_data = self.__get_memory_data(read_memory_index)
            data = self.__evaluate_math_operation(data, second_data, operation)
            self.__set_memory_data(write_memory_index, data)
            self.__log(output_msg.math_operation(param_0, param_1, data, cmd.get_symbol(operation)))
            return True
        try:
            second_data = float(param_1)
            data = self.__evaluate_math_operation(data, second_data, operation)
            self.__set_memory_data(write_memory_index, data)
            self.__log(output_msg.math_operation(param_0, param_1, data, cmd.get_symbol(operation)))
            return True
        except ValueError:
            self.__log(output_msg.invalid_memory_or_value(param_1))
            return False

    def __try_proces_if_command(self, param_0: str, param_1: str, param_2: str) -> bool:
        cond = param_0
        if not condition.is_valid_condition(cond):
            self.__log(output_msg.invalid_condition(cond))
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
            self.__log(output_msg.if_condition(param_1, param_2, cond, result))
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

    def __try_process_instruction(self, instruction: str) -> bool:
        split_with_space = instruction.split(' ')
        command = split_with_space[0]
        if len(split_with_space) == 1:
            return self.__try_process_command_with_zero_params(command)
        params = split_with_space[1].split(',')
        if len(params) == 1:
            return self.__try_process_command_with_one_params(command, params[0])
        if len(params) == 2:
            return self.__try_process_command_with_two_params(command, params[0], params[1])
        if len(params) == 3:
            return self.__try_process_command_with_three_params(command, params[0], params[1], params[2])

    def __initialize_memory(self) -> None:
        self.__memory = [0.0, 0.0, 0.0]

    def __log(self, msg) -> None:
        self.__logs.append(msg)
