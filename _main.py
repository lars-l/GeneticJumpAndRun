from system_settings import SCREEN_WIDTH, SCREEN_HEIGHT, \
    ARENAS, BORDER_HEIGHT, RENDER, FPS_CAP, GENERATION_TO_LOAD, PLAYER_CONTROL
from save_handler import save_generation, init_arenas, log_data
from arena import Arena
from cython_floor_gen import FloorGenerator

import Inheritance
from time import time
import random

arenas = list()
generation = 0
dead_arenas = list()
floor_maker = None
active_arenas = -1
printed = False

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
    global arenas, generation, floor_maker, dead_arenas, printed, active_arenas

    arenas, generation, floor_maker = init_arenas()


    while True:
        dead_arenas = []
        print("\nStarting generation {}".format(generation))

        # Show inital scores for generations to account for starting scores % 100 != 0
        score = floor_maker.get_score()
        print("Current score is ", score, ", ", len(arenas), " active arenas")
        printed = True

        # initialize/reset local scores to track current generation
        active_arenas = len(arenas)
        start_time = time()

        # Perform one generation
        # --main loop doing most of the work--
        while active_arenas > 0:
            floor_maker.next_frame()

            advance_arenas_by_one_frame()

            show_current_progress()

        print("generation took ", (time()-start_time))

        generate_next_generation()


def generate_next_generation():
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


def show_current_progress():
    global printed
    score = floor_maker.get_score()

    if not printed and score % 100 == 0:
        print("Current score is ", score, ", ", len(arenas), " active arenas")
        printed = True
    elif printed and score % 100 == 1:
        printed = False

    if RENDER:
        render()


def advance_arenas_by_one_frame():
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
            if calc_needed_for < 3:
                arena.apply_network()
        else:
            dead_arenas.append(arena)
            arenas.remove(arena)
            active_arenas -= 1
    calc_needed_for -= 1


def find_active_arena():
    for i, arena in enumerate(arenas):
        if arena.running:
            return i
    return 0


def render():
    current_arena = find_active_arena()
    current_arena %= len(arenas)
    find_active_arena()
    game_window.fill((255, 100, 0))
    score_label = myfont.render("Score: {} ".format(floor_maker.get_score()), 1, (0, 0, 0))
    if not PLAYER_CONTROL:
        gen_label = myfont.render("Generation: {} ".format(generation), 1, (0, 0, 0))
        arena_label = myfont.render("Arena: {}/{} ".format(current_arena + 1, len(arenas)), 1, (0, 0, 0))
        diff_label = myfont.render("Difficulty: {}".format(floor_maker.diff), 1, (0, 0, 0))
        game_window.blit(gen_label, (20, SCREEN_HEIGHT + 10))
        game_window.blit(arena_label, (200, SCREEN_HEIGHT + 10))
        game_window.blit(score_label, (380, SCREEN_HEIGHT + 10))
        game_window.blit(diff_label, (540, SCREEN_HEIGHT + 10))
    else:
        if not arenas[current_arena].running:
            lost_label = myfont.render("GAME OVER - PRESS R TO RESTART".format(generation), 1, (0, 0, 0))
            game_window.blit(lost_label, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        game_window.blit(score_label, (20, 10))

    arenas[current_arena].draw(game_window)
    pygame.display.update()
    if FPS_CAP:
        clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                current_arena += 1
            if event.key == pygame.K_LEFT:
                current_arena -= 1
            current_arena %= ARENAS




def play():
    from cython_agent import Agent
    global floor_maker
    current_arena = 0
    # main game loop
    floor_maker = FloorGenerator(seed=100)
    player = Agent()
    arena = Arena(floor_maker)
    arena.set_agent(player)
    arenas.append(arena)

    for _ in range(1000000):
        floor_maker.next_frame()
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
            main()
    except KeyboardInterrupt:
        print("Starting to save neural networks...")
        save_generation(arenas, generation)

