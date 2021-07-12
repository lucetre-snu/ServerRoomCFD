import pygame
from food import Food
from body import Body

class Player:
    def __init__(self, x, y, dx, dy, color, bodycolor, display, boostkey, lkey, rkey, ukey, dkey):
        self.x = x
        self.y = y
        self.color = color
        self.bodycolor = bodycolor
        self.display = display
        self.dx = dx
        self.dy = dy
        self.body = []
        self.boost = 1
        self.boostkey = boostkey
        self.lkey = lkey
        self.rkey = rkey
        self.ukey = ukey
        self.dkey = dkey
        self.game_over = False
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.mod == self.boostkey:
                self.boost = 2
            if event.key == self.lkey:
                self.dx = -10*self.boost
                self.dy = 0
            elif event.key == self.rkey:
                self.dx = 10*self.boost
                self.dy = 0
            elif event.key == self.ukey:
                self.dx = 0
                self.dy = -10*self.boost
            elif event.key == self.dkey:
                self.dx = 0
                self.dy = 10*self.boost
            
    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.boost = 1
        for body in self.body:
            body.move()
    
    def draw(self):
        if not self.body:
            pygame.draw.rect(self.display, self.color, [self.x, self.y, 10, 10])
        else:
            if self.dx == 20:
                pygame.draw.rect(self.display, self.color, [self.x-10, self.y, 20, 10])
            elif self.dx == -20:
                pygame.draw.rect(self.display, self.color, [self.x, self.y, 20, 10])
            elif self.dy == 20:
                pygame.draw.rect(self.display, self.color, [self.x, self.y-10, 10, 20])
            elif self.dy == -20:
                pygame.draw.rect(self.display, self.color, [self.x, self.y, 10, 20])    
            else:
                pygame.draw.rect(self.display, self.color, [self.x, self.y, 10, 10])
            for body in self.body:
                body.draw()
    
    def extend_body(self):
        if not self.body:
            self.body.append(Body(self, self.display, self.bodycolor))
        else:
            self.body.append(Body(self.body[-1], self.display, self.bodycolor))
    
    def interact(self, other):
        if isinstance(other, Food):
            if self.x == other.x and self.y == other.y:
                other.pos_update()
                self.extend_body()

        # 몸통이나 다른 플레이어와 부딪히는 경우
        elif isinstance(other, Player):
            if self != other:
                if self.x == other.x and self.y == other.y:
                    self.game_over = True
        
        elif isinstance(other, Body):
            if self.x == other.x and self.y == other.y:
                self.game_over = True

    def body_movecopy(self):
        for body in reversed(self.body):
            body.movecopy()

