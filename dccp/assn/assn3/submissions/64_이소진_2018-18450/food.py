import pygame
import random
from colors import GREEN

class GridObject2:
    def __init__(self, x, y, game, color):
        self.x = x
        self.y = y
        self.game = game
        self.color = color
        self.active = True

    def handle_event(self, event):
        pass

    def tick(self):
        pass

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])
    
    def interact(self, other):
        pass

class Food(GridObject2):
    color = GREEN
    def __init__(self, game):
        x = random.randint(0, game.w - 1)
        y = random.randint(0, game.h - 1)
        super().__init__(x, y, game, self.color)