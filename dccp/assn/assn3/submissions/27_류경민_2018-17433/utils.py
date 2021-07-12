import pygame
import random 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)



class GridObject:
    def __init__(self, x, y, game, color):
        self.game = game
        self.active = True
        self.color = color
        self.x = x
        self.y = y

    def handle_event(self,event):
        pass

    def tick(self):
        pass

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])

    def interact(self, other):
        pass


class Food(GridObject):
    color = GREEN

    def __init__(self, game, snake1, snake2):
        self.game = game
        self.x = random.randint(0, self.game.n_cols -1)
        self.y= random.randint(0, self.game.n_rows -1)
        self.change_position(snake1, snake2)
        super().__init__(self.x, self.y, game, self.color)

    def interact(self, other):
        pass

    def different(self, snake):
        if self.x == snake.head.x and self.y == snake.head.y:
            return False
        for body in snake.snake_list:
            if self.x == body.x and self.y == body.y:
                return False        
        return True

    def change_position(self, snake1, snake2):
        while not self.different(snake1) or not self.different(snake2):
            self.x = random.randint(0, self.game.n_cols -1)
            self.y= random.randint(0, self.game.n_rows -1)


