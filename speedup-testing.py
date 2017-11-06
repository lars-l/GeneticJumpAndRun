from cython_floor_gen import FloorGenerator
from arena import Arena
from cython_neural_network import NeuralNetwork
import cProfile
import Inheritance

def test():
    floor_maker = FloorGenerator(1111)
    arenas = [Arena(floor_maker, NeuralNetwork()) for _ in range(50000)]
    dead_arenas = []
    gen_running = True
    active_arenas = len(arenas)
    while gen_running:
        floor_maker.next_frame()

        score = floor_maker.get_score()
        if score > 15000:
            gen_running = False
            print("Score of 15000 reached! GG")

        for arena in arenas:
            if arena.running:
                arena.next_frame()
                arena.apply_network()
            else:
                dead_arenas.append(arena)
                arenas.remove(arena)
                active_arenas -= 1

        gen_running = active_arenas > 0


def floor_maker_test():
    f = FloorGenerator(1000)
    for _ in range(3000000):
        f.next_frame()


def inherit_test():
    f = FloorGenerator(1)
    arenas = [Arena(f, NeuralNetwork()) for _ in range(100000)]
    arenas = Inheritance.generate_next_gen(arenas, f)




if __name__ == "__main__":
    cProfile.run('inherit_test()', sort="cumulative")
