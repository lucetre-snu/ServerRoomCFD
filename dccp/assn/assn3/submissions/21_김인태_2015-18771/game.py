import random
import pygame

WHITE = (255, 255 , 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PINK = (125, 0 , 0)
GREEN = (0, 255, 0)
BLUE = (0, 0 ,255)
SKY = (0, 0 ,125)

class GridObject:
    dx = 0
    dy = 0
    def __init__(self, game, x, y, color):
        self.game = game
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])

class Player1(GridObject):
    x = 40
    y = 30
    color = BLUE
    tails = []
    def __init__(self, game):
        super().__init__(game, self.x, self.y, self.color)

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
    
    def move(self):
        if len(self.tails) == 0:
            self.x = self.x + self.dx
            self.y = self.y + self.dy
        elif len(self.tails) > 0:
            self.tails.insert(0, Tail1(self.game, self.x, self.y))
            self.tails.pop(-1)
            self.x = self.x + self.dx
            self.y = self.y + self.dy

    def longer(self):
        self.tails.insert(0, Tail1(self.game, self.x, self.y))
        if self.dx == -1 and self.dy == 0:
            self.x = self.x - 1
        elif self.dx == 1 and self.dy == 0:
            self.x = self.x + 1
        elif self.dx == 0 and self.dy == -1:
            self.y = self.y - 1
        elif self.dx == 0 and self.dy == 1:
            self.y = self.y + 1
        self.draw()

class Tail1(GridObject):
    color = SKY
    def __init__(self, game, x, y):
        super().__init__(game, x, y, self.color)


class Player2(GridObject):
    x = 20
    y = 50
    color = RED
    tails = []
    def __init__(self, game):
        super().__init__(game, self.x, self.y, self.color)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.dx = -1
                self.dy = 0
            elif event.key == pygame.K_d:
                self.dx = 1
                self.dy = 0
            elif event.key == pygame.K_w:
                self.dx = 0
                self.dy = -1
            elif event.key == pygame.K_s:
                self.dx = 0
                self.dy = 1
    def move(self):
        if len(self.tails) == 0:
            self.x = self.x + self.dx
            self.y = self.y + self.dy
        elif len(self.tails) > 0:
            self.tails.insert(0, Tail2(self.game, self.x, self.y))
            self.tails.pop(-1)
            self.x = self.x + self.dx
            self.y = self.y + self.dy

    def longer(self):
        self.tails.insert(0, Tail2(self.game, self.x, self.y))
        if self.dx == -1 and self.dy == 0:
            self.x = self.x - 1
        elif self.dx == 1 and self.dy == 0:
            self.x = self.x + 1
        elif self.dx == 0 and self.dy == -1:
            self.y = self.y - 1
        elif self.dx == 0 and self.dy == 1:
            self.y = self.y + 1
        self.draw()

class Tail2(GridObject):
    color = PINK
    def __init__(self, game, x, y):
        super().__init__(game, x, y, self.color)
    
class Food(GridObject):
    active = True
    color = GREEN
    def __init__(self, game):
        x = random.randint(0, game.n_rows-1) 
        y = random.randint(0, game.n_cols-1) 
        super().__init__(game, x, y, self.color)


class Game:
    block_size = 10
    def __init__(self, n_rows, n_cols):
        pygame.init()
        pygame.display.set_caption(('DCCP Snake Game'))
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((n_rows * self.block_size, n_cols * self.block_size))
        self.game_over = False
        
    def play(self, n_foods = 20):
        n_foods = 20
        player1 = Player1(self)
        player2 = Player2(self)
        foods = [Food(self) for _ in range(n_foods)]

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break
                player1.handle_event(event)
                player2.handle_event(event)
            player1.move()
            player2.move()
            self.display.fill(BLACK)
            player1.draw()
            player2.draw()

            if not (0 <= player1.x <= self.n_rows and 0 <= player1.y <= self.n_cols and 0 <= player2.x <= self.n_rows and 0 <= player2.y <= self.n_cols):
                self.game_over = True
                break

            for food in foods:
                if food.active:
                    food.draw()
                if player1.x == food.x and player1.y == food.y:                  
                    food.active = False
                    foods.remove(food)
                    foods.append(Food(self))
                    player1.longer()
                if player2.x == food.x and player2.y == food.y:                  
                    food.active = False
                    foods.remove(food)
                    foods.append(Food(self))
                    player2.longer()
                   
            for tail in player1.tails:
                tail.draw()
                if tail.x == player1.x and tail.y ==player1.y:
                    self.game_over = True

            for tail in player2.tails:
                tail.draw()
                if tail.x == player1.x and tail.y ==player1.y:
                    self.game_over = True

            for i in player1.tails:
                for j in player2.tails:
                    if player1.x == j.x and player1.y == j.y:
                        self.game_over = True
                    elif player2.x == i.x and player2.y == i.y:
                        self.game_over = True
            
            
            food_remains = False
            for food in foods:
                if food.active:
                    food_remains = True
            if not food_remains:
                game_over = True
            
            pygame.display.update()
            self.clock.tick(10)


if __name__ == "__main__":
    Game(n_rows = 80, n_cols = 60).play()
