# LIBRARY IMPORTS

# Standard Library imports:
from time import time
import random

# External Imports:

# Internal Imports:
from system_settings import ARENAS
from save_handler import save_generation, init_arenas, log_data
from cython_floor_gen import FloorGenerator
import Inheritance

arenas = []
generation = 0
dead_arenas = []
floor_maker = None
active_arenas = ARENAS
printed = False


def main():
    global arenas, generation, floor_maker, dead_arenas, printed, active_arenas

    arenas, generation, floor_maker = init_arenas()

    while True:
        dead_arenas = []
        print("\nStarting generation {}".format(generation))

        # Show inital scores for generations
        score = floor_maker.get_score()
        print("Current score is ", score, ", ", len(arenas), " active arenas")
        printed = True

        # initialize/reset local scores to track current generation
        active_arenas = len(arenas)
        start_time = time()

        # Perform one generation
        while active_arenas > 0:
            floor_maker.next_frame()
            active_arenas = advance_arenas_one_frame()
            show_current_progress()

        print("generation took ", (time()-start_time))
        generate_next_generation()


def generate_next_generation() -> None:
    global floor_maker, arenas, generation
    log_data(generation, floor_maker.get_score())

    starting_score = max(floor_maker.get_score() - 750, 0)
    floor_maker = FloorGenerator(seed=random.random() * 1000, starting_diff=starting_score)
    start_time = time()
    arenas = Inheritance.generate_next_gen(arenas + dead_arenas, floor_maker)
    print("Inheritance took ", (time() - start_time))

    generation += 1
    if generation % 30 == 0:
        save_generation(arenas, generation, to_folder=generation)
    save_generation(arenas, generation)


def show_current_progress() -> None:
    global printed
    score = floor_maker.get_score()

    #if not printed and score % 100 == 0:
    if True:
        print("Current score is ", score, ", ", len(arenas), " active arenas")
        printed = True
    elif printed and score % 100 == 1:
        printed = False


def advance_arenas_one_frame():
    global active_arenas

    # if there are no holes in jumping distance of the agents,
    # it's not necessary to calculate their inputs
    calc_needed_for = 0
    for i in range(6):
        if floor_maker.floor[1 + i] == 0.0:
            calc_needed_for = 6

    for arena in arenas:
        if arena.running:
            arena.next_frame()
            if calc_needed_for > 3:
                arena.apply_network()
        else:
            dead_arenas.append(arena)
            arenas.remove(arena)
            active_arenas -= 1
    calc_needed_for -= 1
    return active_arenas


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Starting to save neural networks...")
        save_generation(arenas, generation)

