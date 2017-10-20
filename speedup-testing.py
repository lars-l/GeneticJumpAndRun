from cython_floor_gen import FloorGenerator
from arena import Arena
from cython_neural_network import NeuralNetwork
import cProfile
import Inheritance

def test():
    f = FloorGenerator(1111)
    arenas = [Arena(f, NeuralNetwork()) for _ in range(1000)]
    gen_running = True
    for i in range(1000):
        f.next_frame()
        for arena in arenas:
            arena.next_frame()
            arena.apply_network()


def floor_maker_test():
    f = FloorGenerator(1000)
    for _ in range(3000000):
        f.next_frame()


def inherit_test():
    f = FloorGenerator(1)
    arenas = [Arena(f, NeuralNetwork()) for _ in range(50000)]
    arenas = Inheritance.generate_next_gen(arenas, f)




if __name__ == "__main__":
    cProfile.run('test()', sort="cumulative")
