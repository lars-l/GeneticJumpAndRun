import pathlib
import pickle
from system_settings import ARENAS,  DISREGARD_SAVE, GENERATION_TO_LOAD
from arena import Arena
from cython_neural_network import NeuralNetwork


def save_generation(arenas, generation, to_folder=None):
    if to_folder is not None:
        pathlib.Path("generation{}".format(to_folder)).mkdir(mode=0o777, parents=True, exist_ok=True)
        f = open("generation{}/arenas.pickle".format(to_folder), "wb")
        g = open("generation{}/gen.pickle".format(to_folder), "wb")
    else:
        pathlib.Path("last_save").mkdir(mode=0o777, parents=True, exist_ok=True)
        f = open("last_save/arenas.pickle", "wb")
        g = open("last_save/gen.pickle", "wb")
    pickle.dump(arenas, f)
    pickle.dump(generation, g)
    f.close()
    g.close()
    if to_folder is not None:
        print("Neural networks in generation {0} successfully saved to folder generation{0}".format(to_folder))
    else:
        print("Neural networks in generation {} successfully saved to folder last_save".format(generation))


def load_generation(folder_number=None):
    if folder_number is not None:
        a = open("generation{}/arenas.pickle".format(folder_number), "rb")
    else:
        a = open("last_save/arenas.pickle", "rb")
    arenas = pickle.load(a)
    a.close()

    if folder_number is not None:
        g = open("generation{}/gen.pickle".format(folder_number), "rb")
    else:
        g = open("last_save/gen.pickle", "rb")
    generation = pickle.load(g)-1
    g.close()
    return arenas, generation

def init_arenas():
    reset_arenas()
    if not DISREGARD_SAVE:
        try:
            if GENERATION_TO_LOAD is None:
                print("Trying to load generation from folder 'last_save'")
            else:
                print("Trying to load generation from folder generation{}".format(GENERATION_TO_LOAD))
            arenas, generation = load_generation(GENERATION_TO_LOAD)
            if GENERATION_TO_LOAD is None:
                print("Successfully loaded generation from folder 'last_save'")
            else:
                print("Successfully loaded generation from folder generation{}".format(GENERATION_TO_LOAD))
            return arenas, generation
        except IOError:
            if GENERATION_TO_LOAD is None:
                print("Failed to load generation from folder 'last_save'")
            else:
                print("Failed to load generation from folder generation{}".format(GENERATION_TO_LOAD))
    print("Starting from scratch...")
    generation = 0

    arenas = reset_arenas()
    for arena in arenas:
        arena.set_network(NeuralNetwork())
    return arenas, generation


def reset_arenas():
    from _main import floor_maker
    arenas = []
    for _ in range(ARENAS):
        arenas.append(Arena(floor_maker))
    return arenas


def log_data(generation, score):
    with open("data.txt", "a") as log:
        log.write("{}, {}\n".format(generation, score))
