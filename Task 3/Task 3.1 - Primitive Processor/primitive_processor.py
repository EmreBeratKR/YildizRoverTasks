from os import system, path as os_path
from primitive_memory import PrimitiveMemory
import commands as cmd
import constants as const
import conditions as condition
import output_messages as output_msg


class PrimitiveProcessor:
    __logs: list[str]
    __memories: list[PrimitiveMemory]
    __should_skip_next_instruction: bool
    __is_runtime_error_occur: bool

    def __init__(self):
        self.__initialize_memory()
        self.__should_skip_next_instruction = False
        self.__is_runtime_error_occur = False

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
            output_path = os_path.join(output_path, first_line.split('=')[1][1:-2])
        except:
            print(f"File {file.name} has invalid output path!")
        n = 0
        for line in file:
            instruction = line[0:-1]
            instructions.append(instruction)
            if not self.__try_process_instruction(instruction):
                error_type = "Runtime" if self.__is_runtime_error_occur else "Syntax"
                print(f"File {file.name}\n{error_type} error at line {n + 2}: {self.__logs[-1]}\n{line}{100 * '-'}")
            n += 1
        for i in range(0, len(instructions)):
            output += f"[{i}][IN] : {instructions[i]}\n"
            output += f"[{i}][OUT]: {self.__logs[i]}\n"
            output += "-" * 100 + "\n"
        file.close()
        log_file = open(output_path, "w")
        log_file.write(output)
        log_file.close()
        print(f"Log file has been written to path:\n[{output_path}]")
        print("-" * 100 + "\n" + output)

    def __get_memory_index(self, memory_address: str) -> int:
        if len(memory_address) != 2 or memory_address[0] != "H":
            return const.NULL_INDEX
        try:
            raw_index = int(memory_address[1]) - 1
            if raw_index >= len(self.__memories):
                return const.NULL_INDEX
            return raw_index
        except ValueError:
            return const.NULL_INDEX

    def __is_memory_initialized(self, index: int) -> float:
        return self.__memories[index].is_initialized()

    def __get_memory_data(self, index: int) -> float:
        return self.__memories[index].get_value()

    def __set_memory_data(self, index: int, value: float) -> None:
        self.__memories[index].set_value(value)

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

    def __try_process_print_command(self, params: list[str]) -> bool:
        if len(params) != 1:
            self.__log(output_msg.invalid_parameter_count(cmd.PRINT, len(params), 1))
            return False
        param_0 = params[0]
        memory_index = self.__get_memory_index(param_0)
        if memory_index == const.NULL_INDEX:
            self.__log(output_msg.invalid_memory(param_0))
            return False
        if not self.__is_memory_initialized(memory_index):
            self.__log(output_msg.uninitialized_memory(param_0))
            self.__raise_runtime_error()
            return False
        data = self.__get_memory_data(memory_index)
        self.__log(output_msg.print_value_of_memory(param_0, data))
        return True

    def __try_process_save_command(self, params: list[str]) -> bool:
        if len(params) != 2:
            self.__log(output_msg.invalid_parameter_count(cmd.SAVE, len(params), 2))
            return False
        param_0 = params[0]
        param_1 = params[1]
        write_memory_index = self.__get_memory_index(param_0)
        if write_memory_index == const.NULL_INDEX:
            self.__log(output_msg.invalid_memory(param_0))
            return False
        try:
            data = float(param_1)
            self.__set_memory_data(write_memory_index, data)
            self.__log(output_msg.save_value_to_memory(param_0, data))
            return True
        except ValueError:
            self.__log(output_msg.invalid_value(param_1))
            return False

    def __try_process_math_operation_command(self, params: list[str], operation: str) -> bool:
        if len(params) != 2:
            self.__log(output_msg.invalid_parameter_count(operation, len(params), 2))
            return False
        param_0 = params[0]
        param_1 = params[1]
        write_memory_index = self.__get_memory_index(param_0)
        read_memory_index = self.__get_memory_index(param_1)
        if write_memory_index == const.NULL_INDEX:
            self.__log(output_msg.invalid_memory(param_0))
            return False
        if read_memory_index == const.NULL_INDEX:
            self.__log(output_msg.invalid_memory(param_1))
            return False
        if not self.__is_memory_initialized(write_memory_index):
            self.__log(output_msg.uninitialized_memory(param_0))
            self.__raise_runtime_error()
            return False
        if not self.__is_memory_initialized(read_memory_index):
            self.__log(output_msg.uninitialized_memory(param_1))
            self.__raise_runtime_error()
            return False
        data_0 = self.__get_memory_data(write_memory_index)
        data_1 = self.__get_memory_data(read_memory_index)
        if data_1 == 0.0 and (operation == cmd.DIVIDE or operation == cmd.MOD):
            self.__log(output_msg.zero_division_error(param_0, param_1, cmd.get_symbol(operation)))
            self.__raise_runtime_error()
            return False
        data = self.__evaluate_math_operation(data_0, data_1, operation)
        self.__set_memory_data(write_memory_index, data)
        self.__log(output_msg.math_operation(param_0, param_1, data, cmd.get_symbol(operation)))
        return True

    def __try_process_if_command(self, params: list[str]) -> bool:
        if len(params) != 3:
            self.__log(output_msg.invalid_parameter_count(cmd.IF, len(params), 3))
            return False
        param_0 = params[0]
        param_1 = params[1]
        param_2 = params[2]
        cond = param_0
        if not condition.is_valid_condition(cond):
            self.__log(output_msg.invalid_condition(cond))
            return False
        memory_index_0 = self.__get_memory_index(param_1)
        memory_index_1 = self.__get_memory_index(param_2)
        if memory_index_0 == const.NULL_INDEX:
            self.__log(output_msg.invalid_memory(param_1))
            return False
        if not self.__is_memory_initialized(memory_index_0):
            self.__log(output_msg.uninitialized_memory(param_1))
            self.__raise_runtime_error()
            return False
        if memory_index_1 == const.NULL_INDEX:
            self.__log(output_msg.invalid_memory(param_2))
            return False
        if not self.__is_memory_initialized(memory_index_1):
            self.__log(output_msg.uninitialized_memory(param_2))
            self.__raise_runtime_error()
            return False
        data_0 = self.__get_memory_data(memory_index_0)
        data_1 = self.__get_memory_data(memory_index_1)
        result = self.__evaluate_equality_operation(data_0, data_1, cond)
        if not result:
            self.__skip_next_instruction()
        self.__log(output_msg.if_condition(param_1, param_2, cond, result))
        return True

    def __try_process_instruction(self, instruction: str) -> bool:
        if self.__should_skip_next_instruction:
            self.__cleanup_skip_next_instruction()
            self.__log(output_msg.skip_instruction(instruction))
            return True
        self.__cleanup_runtime_error()
        split_with_space = instruction.split(' ')
        command = split_with_space[0]
        if command == cmd.CLEAR:
            self.__process_clear_command()
            return True
        params = split_with_space[1].split(',')
        if command == cmd.PRINT:
            return self.__try_process_print_command(params)
        if command == cmd.SAVE:
            return self.__try_process_save_command(params)
        if command == cmd.ADD:
            return self.__try_process_math_operation_command(params, cmd.ADD)
        if command == cmd.SUBTRACT:
            return self.__try_process_math_operation_command(params, cmd.SUBTRACT)
        if command == cmd.MULTIPLY:
            return self.__try_process_math_operation_command(params, cmd.MULTIPLY)
        if command == cmd.DIVIDE:
            return self.__try_process_math_operation_command(params, cmd.DIVIDE)
        if command == cmd.MOD:
            return self.__try_process_math_operation_command(params, cmd.MOD)
        if command == cmd.IF:
            return self.__try_process_if_command(params)
        return False

    def __initialize_memory(self) -> None:
        self.__memories = [PrimitiveMemory(), PrimitiveMemory(), PrimitiveMemory()]

    def __log(self, msg) -> None:
        self.__logs.append(msg)

    def __skip_next_instruction(self):
        self.__should_skip_next_instruction = True

    def __cleanup_skip_next_instruction(self):
        self.__should_skip_next_instruction = False

    def __cleanup_runtime_error(self) -> None:
        self.__is_runtime_error_occur = False

    def __raise_runtime_error(self) -> None:
        self.__is_runtime_error_occur = True
