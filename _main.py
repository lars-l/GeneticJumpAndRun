from system_settings import SCREEN_WIDTH, SCREEN_HEIGHT, \
    ARENAS, BORDER_HEIGHT, RENDER, FPS_CAP, DISREGARD_SAVE, GENERATION_TO_LOAD, PLAYER_CONTROL
import pickle
import pathlib
from arena import Arena

from cython_neural_network import NeuralNetwork
from cython_floor_gen import FloorGenerator

import Inheritance
from time import time
import random

seed = 100
arenas = list()
generation = 0
floor_maker = FloorGenerator(seed=seed)
dead_arenas = list()


if RENDER:
    import pygame
    if PLAYER_CONTROL:
        pygame.key.set_repeat(1, 1)
    else:
        pygame.key.set_repeat(1, 250)
    pygame.init()
    myfont = pygame.font.SysFont("monospace", 15)
    game_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + BORDER_HEIGHT))
    pygame.display.set_caption("Genetic Jump and Run")

    clock = pygame.time.Clock()
    fps = 60


def main():
    global arenas
    global generation
    global floor_maker
    global seed
    current_arena = 0
    global dead_arenas

    program_active = True
    init_arenas()
    while program_active:
        dead_arenas = []
        generation += 1
        print()
        print("Starting generation {}".format(generation))

        if generation % 30 == 0:
            if generation != GENERATION_TO_LOAD:
                save_neural_networks(to_folder=generation)

        active_arenas = len(arenas)
        gen_running = True
        start_time = time()
        while gen_running:
            floor_maker.next_frame()

            for arena in arenas:
                if arena.running:
                    arena.next_frame()
                    arena.apply_network()
                else:
                    dead_arenas.append(arena)
                    arenas.remove(arena)
                    active_arenas -= 1

            current_arena, gen_running = find_active_arena(current_arena, gen_running)
            if RENDER:
                render(current_arena)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        program_active = False
                        gen_running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            current_arena += 1
                        if event.key == pygame.K_LEFT:
                            current_arena -= 1
                        current_arena %= ARENAS
        print("generation took ", (time()-start_time))
        print("Fitness was ", floor_maker.get_score())
        if program_active:  # = program wasn't manually exited previously
            with open("data.txt", "a") as log:
                log.write("{}, {}\n".format(generation, floor_maker.get_score()))

            floor_maker = FloorGenerator(seed=random.random()*1000, starting_diff=0)
            start_time = time()
            arenas = Inheritance.generate_next_gen(arenas + dead_arenas, floor_maker)
            print("Inheritance took ", (time() - start_time))
    # end main game loop
    save_neural_networks(to_folder=None)
    pygame.quit()
    quit()


def find_active_arena(current_arena, gen_running):
    searched = 0
    current_arena %= len(arenas)
    while (not arenas[current_arena].running) and gen_running:
        current_arena += 1
        current_arena %= len(arenas)
        searched += 1
        if searched >= len(arenas):
            gen_running = False
    return current_arena, gen_running


def init_arenas():
    reset_arenas()
    if not DISREGARD_SAVE:
        try:
            if GENERATION_TO_LOAD is None:
                print("Trying to load generation from folder 'last_save'")
            else:
                print("Trying to load generation from folder generation{}".format(GENERATION_TO_LOAD))
            load_generation(GENERATION_TO_LOAD)
            if GENERATION_TO_LOAD is None:
                print("Successfully loaded generation from folder 'last_save'")
            else:
                print("Successfully loaded generation from folder generation{}".format(GENERATION_TO_LOAD))
            return
        except IOError:
            if GENERATION_TO_LOAD is None:
                print("Failed to load generation from folder 'last_save'")
            else:
                print("Failed to load generation from folder generation{}".format(GENERATION_TO_LOAD))
    print("Starting from scratch...")
    reset_arenas()
    for arena in arenas:
        arena.set_network(NeuralNetwork())


def reset_arenas():
    global arenas
    arenas = []
    for _ in range(ARENAS):
        arenas.append(Arena(floor_maker))


def render(current_arena):
    if RENDER:
        current_arena %= len(arenas)
        game_window.fill((255, 100, 0))
        score_label = myfont.render("Score: {} ".format(floor_maker.get_score()), 1, (0, 0, 0))
        if not PLAYER_CONTROL:
            gen_label = myfont.render("Generation: {} ".format(generation), 1, (0, 0, 0))
            arena_label = myfont.render("Arena: {}/{} ".format(current_arena + 1, len(arenas)), 1, (0, 0, 0))
            game_window.blit(gen_label, (20, SCREEN_HEIGHT + 10))
            game_window.blit(arena_label, (200, SCREEN_HEIGHT + 10))
            game_window.blit(score_label, (380, SCREEN_HEIGHT + 10))
        else:
            if not arenas[current_arena].running:
                lost_label = myfont.render("GAME OVER - PRESS R TO RESTART".format(generation), 1, (0, 0, 0))
                game_window.blit(lost_label, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            game_window.blit(score_label, (20, 10))



        arenas[current_arena].draw(game_window)
        pygame.display.update()
        if FPS_CAP:
            clock.tick(fps)


def save_neural_networks(to_folder=None):
    for i, arena in enumerate(arenas + dead_arenas):
        if to_folder is not None:
            pathlib.Path("generation{}".format(to_folder)).mkdir(mode=0o777, parents=True, exist_ok=True)
            f1 = open("generation{}/arena{}.pickle".format(to_folder, i+1), "wb")
            g = open("generation{}/gen.pickle".format(to_folder), "wb")
        else:
            pathlib.Path("last_save").mkdir(mode=0o777, parents=True, exist_ok=True)
            f1 = open("last_save/arena{}.pickle".format(i + 1), "wb")
            g = open("last_save/gen.pickle", "wb")
        pickle.dump(arena.neural_network, f1)
        pickle.dump(generation, g)
        f1.close()
        g.close()
    if to_folder is not None:
        print("Neural networks in generation {0} successfully saved to folder generation{0}".format(to_folder))
    else:
        print("Neural networks in generation {} successfully saved to folder last_save before exiting program".format(generation))


def load_generation(folder_number=None):
    global generation
    for i, arena in enumerate(arenas):
        if folder_number is not None:
            a = open("generation{}/arena{}.pickle".format(folder_number, i + 1), "rb")
        else:
            a = open("last_save/arena{}.pickle".format(i + 1), "rb")
        arena.set_network(pickle.load(a))
        a.close()

    if folder_number is not None:
        g = open("generation{}/gen.pickle".format(folder_number), "rb")
    else:
        g = open("last_save/gen.pickle", "rb")
    generation = pickle.load(g)-1
    g.close()


def play():
    from cython_agent import Agent
    global floor_maker
    current_arena = 0
    # main game loop

    player = Agent()
    arena = Arena(floor_maker)
    arena.set_agent(player)
    arenas.append(arena)
    #for _ in range(15000):
        #floor_maker.next_frame()
    gen_running = True
    while gen_running:
        floor_maker.next_frame()
        if arenas[0].running:
            arenas[0].next_frame()

        if RENDER:
            render(current_arena)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gen_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    arenas[0].agent.jump()
                if event.key == pygame.K_r:
                    floor_maker = FloorGenerator(seed=seed)
                    #for _ in range(15000):
                        #floor_maker.next_frame()
                    arenas[0] = Arena(floor_maker)
                    arenas[0].set_agent(player)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    arenas[0].agent.terminate_early()
    arenas[0] = Arena(floor_maker)
    pygame.quit()
    quit()


if __name__ == "__main__":

    try:
        if PLAYER_CONTROL:
            play()
        else:
            #import cProfile

            #cProfile.run('main()', sort='cumulative')
            main()
    except KeyboardInterrupt:
        print("Starting to save neural networks...")
        save_neural_networks()
        pass

