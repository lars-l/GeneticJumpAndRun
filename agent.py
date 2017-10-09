from system_settings import START_X, START_Y, AGENT_WIDTH, AGENT_HEIGHT, MAX_JUMPS, GRAVITY, JUMP_VELOCITY, EARLY_TERMINATION_VELOCITY, RENDER
if RENDER:
    import pygame
    pygame.init()


class Agent:
    if RENDER:
        image = pygame.Surface((AGENT_WIDTH, AGENT_HEIGHT))
        image.fill((0, 0, 0))

    def __init__(self):
        #pygame.sprite.Sprite.__init__(self)
        self.x = START_X
        self.y = START_Y
        self.velocity = 0
        self.in_air = False
        self.jumps = MAX_JUMPS
        self.can_jump = True

    def update(self):
        if self.in_air:  # currently jumping
            self.velocity -= GRAVITY
            self.y -= self.velocity
            if self.y >= START_Y:
                self.y = START_Y
                self.velocity = 0
                self.in_air = False
                self.jumps = MAX_JUMPS
                self.can_jump = True

    def jump(self):
        if self.can_jump:
            self.velocity = JUMP_VELOCITY
            self.in_air = True
            self.jumps -= 1
            self.can_jump = False

    def terminate_early(self):
        self.velocity = min(self.velocity, EARLY_TERMINATION_VELOCITY)
        self.can_jump = self.jumps > 0

    def draw(self, screen):
        pygame.init()
        screen.blit(Agent.image, (self.x, self.y-AGENT_HEIGHT))

    def apply(self, jump_pressed):
        if jump_pressed and self.jumps > 0:
            self.jump()
        elif self.in_air and not jump_pressed:
            self.terminate_early()
