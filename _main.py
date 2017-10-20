from system_settings import SCREEN_WIDTH, SCREEN_HEIGHT, \
    ARENAS, BORDER_HEIGHT, RENDER, FPS_CAP, GENERATION_TO_LOAD, PLAYER_CONTROL
from save_handler import save_generation, init_arenas, log_data
from arena import Arena
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
    global dead_arenas
    current_arena = 0


    program_active = True
    arenas, generation = init_arenas()
    floor_maker = arenas[0].floor_maker
    while program_active:
        dead_arenas = []
        generation += 1
        print("\nStarting generation {}".format(generation))


        if generation % 30 == 0:
            if generation != GENERATION_TO_LOAD:
                save_generation(arenas, generation, to_folder=generation)

        active_arenas = len(arenas)
        gen_running = True
        start_time = time()
        while gen_running:
            floor_maker.next_frame()

            if floor_maker.get_score() > 15000:
                gen_running = False
                print("Score of 10000 reached! GG")

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


        print("generation took ", (time()-start_time))
        if program_active:  # = program wasn't manually exited previously
            log_data(generation, floor_maker.get_score())

            floor_maker = FloorGenerator(seed=random.random()*1000, starting_diff=0)
            start_time = time()
            arenas = Inheritance.generate_next_gen(arenas + dead_arenas, floor_maker)
            print("Inheritance took ", (time() - start_time))
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
            main()
    except Exception:
        print("Starting to save neural networks...")
        save_generation(arenas, generation)

