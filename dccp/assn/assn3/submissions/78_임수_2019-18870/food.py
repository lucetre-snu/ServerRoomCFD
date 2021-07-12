import random as r
import pygame as p

class Food:
    def __init__(self, size, screen):
        range_x, range_y = size
        self.x = r.randint(0, range_x/10-1)*10
        self.y = r.randint(0, range_y/10-1)*10
        self.screen = screen
    
    def set_FoodColor(self, color):
        self.foodColor = color
    
    def draw(self):
        p.draw.rect(self.screen, self.foodColor, [self.x, self.y, 10, 10])