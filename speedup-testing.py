from cython_floor_gen import FloorGenerator
from arena import Arena
from neural_network import NeuralNetwork as PythonNeuralNetwork
from cython_neural_network import NeuralNetwork
import cProfile

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

if __name__ == "__main__":
    print("Best python score was: 1.967")

    cProfile.run('test()', sort='cumulative')
