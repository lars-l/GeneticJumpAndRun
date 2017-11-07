# LIBRARY IMPORTS

# Standard Library imports:
import pathlib
import pickle

# External Imports:

# Internal Imports:
from system_settings import ARENAS,  DISREGARD_SAVE, GENERATION_TO_LOAD
from arena import Arena
from cython_floor_gen import FloorGenerator
from cython_neural_network import NeuralNetwork



def save_generation(arenas, generation, to_folder=None):
    if to_folder is not None:
        pathlib.Path("generation{}".format(to_folder)).mkdir(mode=0o777, parents=True, exist_ok=True)
        for i in range(ARENAS//10000):
            f = open("generation{}/arenas{}.pickle".format(to_folder, i), "wb")
            pickle.dump(arenas[i*10000:(i+1)*10000], f)
            f.close()

        g = open("generation{}/gen.pickle".format(to_folder), "wb")
        pickle.dump(generation, g)
        g.close()
    else:
        pathlib.Path("last_save").mkdir(mode=0o777, parents=True, exist_ok=True)
        for i in range(ARENAS//10000):
            f = open("last_save/arenas{}.pickle".format(i), "wb")
            pickle.dump(arenas[i*10000:(i+1)*10000], f)
            f.close()

        g = open("last_save/gen.pickle", "wb")
        pickle.dump(generation, g)
        g.close()


    if to_folder is not None:
        print("Neural networks in generation {0} successfully saved to folder generation{0}".format(to_folder))
    else:
        print("Neural networks in generation {} successfully saved to folder last_save".format(generation))


def load_generation(folder_number=None):

    arenas = []

    folder = "last_save/" if folder_number is None else "generation{}/".format(folder_number)

    print("Trying to load generation from folder " + folder)

    for i in range(ARENAS//10000):
        a = open(folder + "arenas{}.pickle".format(i), "rb")
        arenas += pickle.load(a)
        a.close()

    g = open(folder + "gen.pickle", "rb")
    generation = pickle.load(g)
    g.close()

    print("Successfully loaded generation from folder " + folder)
    return arenas, generation

def restart_arenas():
    print("Starting from scratch...")
    generation = 0

    arenas = []
    floor_maker = FloorGenerator()
    for _ in range(ARENAS):
        arenas.append(Arena(floor_maker, NeuralNetwork()))
    return arenas, generation, floor_maker

def init_arenas() :
    if DISREGARD_SAVE:
        return restart_arenas()
    else:
        try:
            arenas, generation = load_generation(GENERATION_TO_LOAD)
            return arenas, generation, arenas[0].floor_maker
        except IOError as ioerr:
            print("IOError during loading: ", ioerr)
            return restart_arenas()




def log_data(generation, score):
    with open("data.txt", "a") as log:
        log.write("{}, {}\n".format(generation, score))
