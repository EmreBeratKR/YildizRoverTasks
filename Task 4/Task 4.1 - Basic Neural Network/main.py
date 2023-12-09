import random

from basic_neural_network import BasicNeuralNetwork
from data_set import train_data_set


SEED = 35
INPUT_COUNT = 3
TRAIN_ITERATION_COUNT = 1000
LEARN_RATE = 0.1


def train_neural_network(neural_network: BasicNeuralNetwork) -> None:
    for i in range(TRAIN_ITERATION_COUNT):
        neural_network.train(train_data_set, LEARN_RATE)


def test_neural_network(neural_network: BasicNeuralNetwork) -> None:
    neural_network.test(train_data_set)


def main():
    random.seed(SEED)
    network = BasicNeuralNetwork(INPUT_COUNT)
    train_neural_network(network)
    test_neural_network(network)


if __name__ == '__main__':
    main()
