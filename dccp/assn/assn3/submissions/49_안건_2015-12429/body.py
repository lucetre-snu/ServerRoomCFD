import pygame

class Body:
    def __init__(self, ahead, display, bodycolor):
        self.ahead = ahead
        self.x = ahead.x - ahead.dx
        self.y = ahead.y - ahead.dy
        self.dx = ahead.dx
        self.dy = ahead.dy
        self.display = display
        self.bodycolor = bodycolor

    def movecopy(self):
        self.dx = self.ahead.dx
        self.dy = self.ahead.dy

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        if self.dx == 20:
            pygame.draw.rect(self.display, self.bodycolor, [self.x-10, self.y, 20, 10])
        elif self.dx == -20:
            pygame.draw.rect(self.display, self.bodycolor, [self.x, self.y, 20, 10])
        elif self.dy == 20:
            pygame.draw.rect(self.display, self.bodycolor, [self.x, self.y-10, 10, 20])
        elif self.dy == -20:
            pygame.draw.rect(self.display, self.bodycolor, [self.x, self.y, 10, 20])    
        else:
            pygame.draw.rect(self.display, self.bodycolor, [self.x, self.y, 10, 10])