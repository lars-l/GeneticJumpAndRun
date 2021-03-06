# LIBRARY IMPORTS

# Standard Library imports:
import copy

# External Imports:
from numpy.random import random
import numpy as np

# Internal Imports:
from arena import Arena
from cython_neural_network import NeuralNetwork
from system_settings import INPUT_NEURONS, HIDDEN_NEURONS, OUTPUT_NEURONS, ARENAS


BIASES = OUTPUT_NEURONS + HIDDEN_NEURONS
WEIGHTS = INPUT_NEURONS * HIDDEN_NEURONS + HIDDEN_NEURONS * OUTPUT_NEURONS
MUT_SPOTS = BIASES + WEIGHTS

LEFT_OVER = int(ARENAS/100)
AMOUNT = 5


def generate_next_gen(arenas, floor_maker):
    arenas = rank_fitness(arenas)

    networks = []
    for arena in arenas:
        networks.append(arena.neural_network)
    print_stats(arenas)
    del arenas
    arenas = []

    arenas.append(Arena(floor_maker, copy.deepcopy(networks[0])))
    arenas.append(Arena(floor_maker, copy.deepcopy(networks[1])))

    for i in range(LEFT_OVER):
        arenas.append(Arena(floor_maker, mutate(mutate(copy.deepcopy(networks[i+2])))))

    while len(arenas) < ARENAS:
        parents = [get_parent_e(networks) for _ in range(AMOUNT)]

        for i in range(AMOUNT):
            for j in range(i + 1, AMOUNT):
                child1, child2 = element_wise_crossover(parents[i], parents[j])
                arenas.append(Arena(floor_maker, child1))
                arenas.append(Arena(floor_maker, child2))

    return arenas[:ARENAS]


def get_parent(networks):
    for _ in range(int(np.log2(len(networks)))):
        if random() < 0.8:
            networks = networks[0:len(networks)//2]
        else:
            networks = networks[len(networks)//2:len(networks)]
    return networks[0]


def get_parent_e(networks):
    r = np.random.beta(1,100,1)-1.0/100.0
    while r < 0:
        r = np.random.beta(1, 100, 1) - 1.0 / 100.0
    return networks[int(ARENAS*r)]


def rank_fitness(arenas):
    return sorted(arenas, key=lambda arena: arena.fitness, reverse=True)


def print_stats(arenas):
    print("The best fitness was: {}, the worst {}".format(arenas[0].fitness, arenas[-1].fitness))
    print("The median agent had a fitness of {}".format(arenas[ARENAS//2].fitness))


def cull_the_meek(arenas):
    return arenas[:int(ARENAS*0.1)]


def element_wise_crossover(a, b):
    p1 = copy.deepcopy(a)
    p2 = copy.deepcopy(b)

    child1 = NeuralNetwork()
    child2 = NeuralNetwork()

    for i in range(len(child1.biases0)):
        if random() < 0.8:
            child1.biases0[i][0] = p1.biases0[i][0]
            child2.biases0[i][0] = p2.biases0[i][0]
        else:
            child1.biases0[i][0] = p2.biases0[i][0]
            child2.biases0[i][0] = p1.biases0[i][0]

    for i in range(len(child1.biases1)):
        if random() < 0.8:
            child1.biases1[i][0] = p1.biases1[i][0]
            child2.biases1[i][0] = p2.biases1[i][0]
        else:
            child1.biases1[i][0] = p2.biases1[i][0]
            child2.biases1[i][0] = p1.biases1[i][0]

    for i in range(len(child1.biases2)):
        if random() < 0.8:
            child1.biases2[i][0] = p1.biases2[i][0]
            child2.biases2[i][0] = p2.biases2[i][0]
        else:
            child1.biases2[i][0] = p2.biases2[i][0]
            child2.biases2[i][0] = p1.biases2[i][0]

    for i in range(len(child1.weights0)):
        for j in range(len(child1.weights0[i])):
            if random() < 0.8:
                child1.weights0[i][j] = p1.weights0[i][j]
                child2.weights0[i][j] = p2.weights0[i][j]
            else:
                child1.weights0[i][j] = p2.weights0[i][j]
                child2.weights0[i][j] = p1.weights0[i][j]
    for i in range(len(child1.weights1)):
        for j in range(len(child1.weights1[i])):
            if random() < 0.8:
                child1.weights1[i][j] = p1.weights1[i][j]
                child2.weights1[i][j] = p2.weights1[i][j]
            else:
                child1.weights1[i][j] = p2.weights1[i][j]
                child2.weights1[i][j] = p1.weights1[i][j]

    for i in range(len(child1.weights2)):
        for j in range(len(child1.weights2[i])):
            if random() < 0.8:
                child1.weights2[i][j] = p1.weights2[i][j]
                child2.weights2[i][j] = p2.weights2[i][j]
            else:
                child1.weights2[i][j] = p2.weights2[i][j]
                child2.weights2[i][j] = p1.weights2[i][j]
    return mutate(child1), mutate(child2)


def mutate(nn):
    # previous mutation rate =1/BIASES and 1/WEIGHTS
    for i in range(len(nn.biases0)):
        if random() < 0.04:
            nn.biases0[i] = np.random.randn()
    for i in range(len(nn.biases1)):
        if random() < 0.04:
            nn.biases1[i] = np.random.randn()
    for i in range(len(nn.biases2)):
        if random() < 0.04:
            nn.biases2[i] = np.random.randn()

    for i in range(len(nn.weights0)):
        for j in range(len(nn.weights0[i])):
            if random() < 0.04:
                nn.weights0[i][j] = np.random.randn()

    for i in range(len(nn.weights1)):
        for j in range(len(nn.weights1[i])):
            if random() < 0.04:
                nn.weights1[i][j] = np.random.randn()
    for i in range(len(nn.weights2)):
        for j in range(len(nn.weights2[i])):
            if random() < 0.04:
                nn.weights2[i][j] = np.random.randn()
    return nn

