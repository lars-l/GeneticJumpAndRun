 #  from random import randint, random
from numpy.random import random, choice
from random import randint
import numpy as np
from arena import Arena
from cython_neural_network import NeuralNetwork
from system_settings import INPUT_NEURONS, HIDDEN_NEURONS, OUTPUT_NEURONS, ARENAS
from floor import FloorGenerator
import copy

BIASES = OUTPUT_NEURONS + HIDDEN_NEURONS
WEIGHTS = INPUT_NEURONS * HIDDEN_NEURONS + HIDDEN_NEURONS * OUTPUT_NEURONS
MUT_SPOTS = BIASES + WEIGHTS

LEFT_OVER = int(ARENAS/100)


def generate_next_gen(arenas, floor_maker):
    arenas = rank_fitness(arenas)
    networks = []
    for arena in arenas:
        networks.append(copy.deepcopy(arena.neural_network))
    arenas = []

    arenas.append(Arena(floor_maker, copy.deepcopy(networks[0])))



    x = copy.deepcopy(networks[:LEFT_OVER])
    for nn in x:
        arenas.append(Arena(floor_maker, mutate(mutate(copy.deepcopy(nn)))))

    y = copy.deepcopy(networks)
    child_nns = []
    for _ in range(int((ARENAS-LEFT_OVER)/2)):
        children = element_wise_crossover(y)
        child_nns.append(children[0])
        child_nns.append(children[1])


    for i in range(ARENAS-LEFT_OVER-1):
        nn = choice(child_nns)
        child_nns.remove(nn)
        arenas.append(Arena(floor_maker, nn))
    return arenas


# Higher odds of picking an agent at the start of the list.
def get_parent(networks):
    n = sum(n+1 for n in range(len(networks)))
    x = randint(1, n)
    k = len(networks)
    i = 0
    while n > 0:
        n -= (k-i)
        if x > n:
            return networks[i]
        i += 1


def get_all_agents(arenas):
    agents = []
    for arena in arenas:
        agents.append(arena.agent)
    return agents


def rank_fitness(arenas):
    return sorted(arenas, key=lambda arena: arena.fitness, reverse=True)


def print_stats(arenas):
    print("The best fitness was: {}".format(arenas[0].fitness))


def cull_the_meek(arenas):
    return arenas[:int(ARENAS*0.1)]


def element_wise_crossover(networks):
    p1 = get_parent(networks)
    p2 = get_parent(networks)

    while p1 is p2 or p1.biases0[0] == p2.biases0[0]:
        p2 = get_parent(networks)
        #p2 = mutate(p2)

    child1 = NeuralNetwork()
    child2 = NeuralNetwork()

    for i in range(len(child1.biases0)):
        if random() < 0.8:
            child1.biases0[i] = p1.biases0[i]
            child2.biases0[i] = p2.biases0[i]
        else:
            child1.biases0[i] = p2.biases0[i]
            child2.biases0[i] = p1.biases0[i]

    for i in range(len(child1.biases1)):
        if random() < 0.8:
            child1.biases1[i] = p1.biases1[i]
            child2.biases1[i] = p2.biases1[i]
        else:
            child1.biases1[i] = p2.biases1[i]
            child2.biases1[i] = p1.biases1[i]

    for i in range(len(child1.biases2)):
        if random() < 0.8:
            child1.biases2[i] = p1.biases2[i]
            child2.biases2[i] = p2.biases2[i]
        else:
            child1.biases2[i] = p2.biases2[i]
            child2.biases2[i] = p1.biases2[i]

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



if __name__ == "__main__":
    a = NeuralNetwork(1)
    test = [NeuralNetwork(0), NeuralNetwork(1)]
    element_wise_crossover(test)
