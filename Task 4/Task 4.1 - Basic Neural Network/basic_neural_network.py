from train_data import TrainData
import random


class BasicNeuralNetwork:
    __weights: list[float]
    __bias: float

    def __init__(self, input_count: int):
        self.__randomize_weights(input_count)
        self.__randomize_bias()

    def evaluate(self, inputs: list[int]) -> float:
        result = self.__bias
        for i in range(len(self.__weights)):
            result += self.__weights[i] * inputs[i]
        return result

    def train(self, data_set: list[TrainData], learn_rate: float) -> None:
        for i in range(len(data_set)):
            self.backpropagate(data_set[i], learn_rate)

    def test(self, data_set: list[TrainData]) -> None:
        cost_sum = 0.0
        for i in range(len(data_set)):
            h = self.evaluate(data_set[i].inputs)
            y = data_set[i].output
            cost = (h - y) ** 2
            cost_sum += cost
            print(f"Test {i}")
            print(f"{data_set[i]} => {h}")
            print(f"Cost: {cost}")
            print("-" * 100)
        average_cost = cost_sum / len(data_set)
        print(f"Average Cost: {average_cost} (The closer it gets to zero, the more accurate it gets)")

    def backpropagate(self, train_data: TrainData, learn_rate: float) -> None:
        h = self.evaluate(train_data.inputs)
        y = train_data.output
        bias_nudge = -2 * (h - y) * learn_rate
        self.__bias += bias_nudge
        for i in range(len(self.__weights)):
            weight_nudge = -2 * (h - y) * train_data.inputs[i] * learn_rate
            self.__weights[i] += weight_nudge

    def __randomize_weights(self, input_count: int) -> None:
        self.__weights = []
        for i in range(input_count):
            random_weight = BasicNeuralNetwork.__get_random_weight()
            self.__weights.append(random_weight)

    def __randomize_bias(self) -> None:
        self.__bias = BasicNeuralNetwork.__get_random_bias()

    @staticmethod
    def __get_random_weight() -> float:
        return random.random()

    @staticmethod
    def __get_random_bias() -> float:
        return random.random()
