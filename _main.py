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
    global dead_arenas
    current_arena = 0


    program_active = True
    arenas, generation = init_arenas()
    floor_maker = arenas[0].floor_maker

    while program_active:
        dead_arenas = []
        print("\nStarting generation {}".format(generation))



        active_arenas = len(arenas)
        gen_running = True
        printed = False
        start_time = time()
        while gen_running:
            floor_maker.next_frame()

            score = floor_maker.get_score()

            if not printed and score % 100 == 0:
                print("Current score is ", score, ", ", len(arenas), " active arenas")
                printed = True
            elif printed and score % 100 == 1:
                printed = False

            calc_needed = False
            for i in range(6):
                if floor_maker.floor[1+i] == 0.0:
                    calc_needed = True


            for arena in arenas:
                if arena.running:
                    arena.next_frame()
                    if calc_needed:
                        arena.apply_network()
                else:
                    dead_arenas.append(arena)
                    arenas.remove(arena)
                    active_arenas -= 1

            gen_running = active_arenas > 0

            if score > 15000:
                gen_running = False
                print("Score of 15000 reached! GG")

            if RENDER:
                current_arena, gen_running = find_active_arena(current_arena, gen_running)
                render(current_arena)


        print("generation took ", (time()-start_time))
        if program_active:  # = program wasn't manually exited previously
            log_data(generation, floor_maker.get_score())

            starting_score = max(floor_maker.get_score() - 750, 0)
            floor_maker = FloorGenerator(seed=random.random()*1000, starting_diff=starting_score)
            start_time = time()
            arenas = Inheritance.generate_next_gen(arenas + dead_arenas, floor_maker)
            print("Inheritance took ", (time() - start_time))

        generation += 1
        if generation % 30 == 0:
            save_generation(arenas, generation, to_folder=generation)
        save_generation(arenas, generation)

    # end main game loop
    save_generation(arenas, generation, to_folder=None)
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





def render(current_arena):
    current_arena %= len(arenas)
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

