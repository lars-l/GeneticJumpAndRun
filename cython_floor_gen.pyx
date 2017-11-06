from system_settings import SEG_LEN, SEG_AMOUNT,  OFFSET_DELTA, MAX_DIFF, MIN_DIFF, START_Y, RENDER, SEGMENT_NEURONS
from random import random, Random
import pygame
pygame.init()

cdef class FloorGenerator:
    cdef int current_gap
    cdef public int score
    cdef public double diff
    cdef double offset
    cdef object rng
    cdef readonly object floor

    def __init__(self, starting_diff=None, seed=None):
        self.score = starting_diff if starting_diff is not None else 0
        if seed is not None:
            self.rng = Random(seed)
        else:
            self.rng = Random()
        self.offset = 0
        self.floor = [1.0 for _ in range(3)]
        self.floor.append(0.0)
        self.current_gap = 0
        self.diff = calc_difficulty(self.score)
        for _ in range(SEG_AMOUNT):
            if self.rng.random() > self.diff and self.current_gap <= 5:
                self.floor.append(0.0)
                self.current_gap += 1
            else:
                self.floor.append(1.0)
                self.current_gap = 0

    def get_segment_neurons(self):
        return self.floor[2:SEGMENT_NEURONS+2]

    def get_score(self):
        return self.score

    cpdef next_frame(self):
        if self.offset >= SEG_LEN:
            self.score += 1
            self.diff = calc_difficulty(self.score)
            self.floor.pop(0)
            if self.rng.random() > self.diff and self.current_gap <= 5:
                self.floor.append(0.0)
                self.current_gap += 1
            else:
                self.floor.append(1.0)
                self.current_gap = 0
            self.offset = 0
        else:
            self.offset += OFFSET_DELTA




    def draw(self, game_window):
        for i, x in enumerate(self.floor):
            if x:
                pygame.draw.line(game_window, (0, 0, 0), (i * SEG_LEN - self.offset, 200), ((i + 1) * SEG_LEN - self.offset - 1, 200), 2)

    cpdef bint agent_died(self, agent):
        if agent.y < START_Y:
            return False
        # Agents x coordinate is fixed, only y moves. START_X is this fixed position.
        # Check if right most OR left most corner is still on solid ground

        # Rightmost and leftmost corner are in segment 2
        if self.offset < 5:
            return self.floor[2] == 0


        # both corners in segment 3
        if self.offset >= 15:
            return self.floor[3] == 0

        # rightmost corner in segment 3, leftmost in segment 2
        if self.offset < 15:
            return self.floor[2] == 0 and self.floor[3] == 0


cdef double calc_difficulty(x):
    cdef double k = -(((MIN_DIFF-MAX_DIFF)*100.0)/1500000.0)*x + MIN_DIFF
    return max(MAX_DIFF, min(MIN_DIFF, k))