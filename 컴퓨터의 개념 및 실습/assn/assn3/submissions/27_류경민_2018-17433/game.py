import random
import pygame
from utils import *
from snake import *
class Player(GridObject):
    color = WHITE 
    dx = 0
    dy = 0
    
    def __init__(self, x, y, game):
        super().__init__(x, y, game, self.color)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.dx = -1
                self.dy = 0
            elif event.key == pygame.K_RIGHT:
                self.dx = 1
                self.dy = 0
            elif event.key == pygame.K_UP:
                self.dx = 0
                self.dy = -1
            elif event.key == pygame.K_DOWN:
                self.dx = 0
                self.dy = 1

    def tick(self):
        self.x += self.dx
        self.y += self.dy

    def out_of_screen(self):
        if self.x > self.game.n_cols or self.y > self.game.n_rows:
            return True
        elif self.x < 0 or self.y < 0:
            return True
        else:
            return False

class Game:
    block_size = 10
    def __init__(self, n_rows, n_cols):
        pygame.init()
        pygame.display.set_caption('DCCP Snake Game')
        self.display = pygame.display.set_mode((n_cols * self.block_size, n_rows * self.block_size))
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.objects = []

    def active_objects(self):
        for obj in self.objects:
            if obj.active:
                yield obj
    
    def play(self, n_foods=20):
        snake1 = Snake( 40,20, self, RED, BLUE, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RSHIFT)
        snake2 = Snake(20,20, self, YELLOW, WHITE, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_LSHIFT)

        self.objects = [
            snake1, 
            snake2, 
            *[Food(self, snake1, snake2) for _ in range(n_foods)]
        ]


        while not self.game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break

                # Handle Event
                for obj in self.active_objects():
                    obj.handle_event(event)

            # Tick
            for obj in self.active_objects():
                obj.tick()

            # Interact
            for obj1 in self.active_objects():
                for obj2 in self.active_objects():
                        obj1.interact(obj2)                    
                        obj2.interact(obj1)                    

            for obj in self.active_objects():
                if isinstance(obj, Food):
                    obj.change_position(self.objects[0], self.objects[1])


            # Draw
            self.display.fill(BLACK)
            for obj in self.active_objects():
                obj.draw()
            pygame.display.update()

        
            for obj in self.active_objects():
                if isinstance(obj, Snake):
                    if obj.out_of_screen() or obj.if_touched:
                        self.game_over= True

            # Global Decision
            food_remains = False
            for obj in self.active_objects():
                if isinstance(obj, Food):
                    food_remains = True
            if not food_remains:
                self.game_over = True
            self.clock.tick(10)

if __name__ == "__main__":
    Game(n_rows=60, n_cols=80).play(n_foods=20)






