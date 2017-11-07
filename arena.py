# LIBRARY IMPORTS

# Standard Library imports:

# External Imports:

# Internal Imports:
from system_settings import SEG_LEN, MAX_JUMPS, JUMP_VELOCITY, MAX_HEIGHT, START_Y, EARLY_TERMINATION_VELOCITY
from cython_agent import Agent

from cython_neural_network import NeuralNetwork

class Arena:
    def __init__(self, floor_maker, neural_network=None):
        self.floor_maker = floor_maker
        self.agent = Agent()
        self.running = True
        self.fitness = 0
        self.neural_network = neural_network if neural_network is not None else NeuralNetwork()

    def next_frame(self):
        self.agent.update()
        if self.floor_maker.agent_died(self.agent):
            self.fitness = self.calculate_fitness()
            self.running = False

    def set_network(self, network):
        self.neural_network = network

    def apply_network(self):
        if self.agent.in_air and self.agent.velocity <= EARLY_TERMINATION_VELOCITY:
            return
        else:
            inp = self.calculate_meta_neurons() + self.floor_maker.get_segment_neurons()
            jump = self.neural_network.calculate_output_neurons(inp)
            self.agent.apply(jump)

    def calculate_meta_neurons(self):
        neurons = []
        neurons.append(float(abs(self.agent.y-START_Y)/MAX_HEIGHT))
        neurons.append(float(self.floor_maker.offset/SEG_LEN))
        neurons.append(float(self.agent.velocity/JUMP_VELOCITY))
        return neurons

    def calculate_fitness(self):
        return self.floor_maker.get_score()

    def set_agent(self, agent):
        self.agent = agent
