import pygame
import random

class Food:
    color = (0, 191, 0) # Green
    def __init__(self, display):
        self.x = random.randint(0, 79)*10
        self.y = random.randint(0, 59)*10
        self.display = display
    
    def pos_update(self):
        self.x = random.randint(0, 79)*10
        self.y = random.randint(0, 59)*10
    
    def draw(self):
        pygame.draw.rect(self.display, self.color, [self.x, self.y, 10, 10])