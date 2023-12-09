import random

from basic_neural_network import BasicNeuralNetwork
from data_set import train_data_set


SEED = 35
INPUT_COUNT = 3
TRAIN_ITERATION_COUNT = 1000
LEARN_RATE = 0.1


def main():
    random.seed(SEED)
    network = BasicNeuralNetwork(INPUT_COUNT)
    for i in range(TRAIN_ITERATION_COUNT):
        network.train(train_data_set, LEARN_RATE)
    network.test(train_data_set)


if __name__ == '__main__':
    main()
