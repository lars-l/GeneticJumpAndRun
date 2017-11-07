# LIBRARY IMPORTS

# Standard Library imports:

# External Imports:

# Internal Imports:
from system_settings import START_X, START_Y, AGENT_WIDTH, AGENT_HEIGHT, GRAVITY, JUMP_VELOCITY, EARLY_TERMINATION_VELOCITY, RENDER

cdef class Agent:

    cdef public double x, y, velocity
    cdef public int jumps
    cdef public bint in_air, can_jump

    def __init__(self):
        self.x = START_X
        self.y = START_Y
        self.velocity = 0
        self.in_air = False

    cpdef update(self):
        if self.in_air:  # currently jumping
            self.velocity -= GRAVITY 
            self.y -= self.velocity
            if self.y >= START_Y: # agent hit the ground
                self.y = START_Y
                self.velocity = 0
                self.in_air = False

    cpdef jump(self):
        self.velocity = JUMP_VELOCITY
        self.in_air = True
        self.can_jump = False

    def terminate_early(self):
        self.velocity = min(self.velocity, EARLY_TERMINATION_VELOCITY)
        self.can_jump = False

    cpdef void apply(self, bint jump_pressed):
        if jump_pressed and not self.in_air:
            self.jump()
        elif self.in_air and not jump_pressed:
            self.terminate_early()
