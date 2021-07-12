import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 50, 255)
RED_TAIL = (255,0,153)
BLUE_TAIL = (0,200,255)
block_size = 0

class GridObject:
    def __init__(self, x, y, game, color):
        self.game = game
        self.active = True
        self.color = color
        self.x = x
        self.y = y
        self.shift_pressed = False

    def handle_event(self, event, keys):
        pass

    def tick(self):
        pass

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])

    def interact(self, other):
        pass

class Player(GridObject):
    dx = 0 
    dy = 0
    tmp_x = 0
    tmp_y = 0

    def __init__(self, x, y, game, color):
        super().__init__(x, y, game, color)
        self.body = 0
        self.tail_list = [self]

    def handle_event(self, event, keys):
        pass
    
    def tick(self):
        pass

    def interact(self, other):
        if isinstance(other, Food):
            if (self.x == other.x and self.y == other.y) or (self.x - self.dx == other.x and self.y - self.dy == other.y):
                other.active = False
                self.game.objects.append(Food(self.game))
                self.body += 1
                self.tail_list.append(tail(self.game, self.tail_list[-1]))
                self.game.objects.append(self.tail_list[-1])
        elif isinstance(other, Player):
            if (self.x == other.x and self.y == other.y):
                self.game.game_over = True

class tail(Player):
    def __init__(self, game, player):
        if player.color == RED:
            self.color = RED_TAIL
        elif player.color == BLUE:
            self.color = BLUE_TAIL
        else:
            self.color = player.color
        self.player = player
        self.order = player.body
        super().__init__(player.tmp_x, player.tmp_y, game, self.color)
    
    def handle_event(self, event, keys):
        self.shift_pressed = self.player.shift_pressed

    def tick(self):
        self.tmp_x = self.x
        self.tmp_y = self.y
        self.x = self.player.tmp_x
        self.y = self.player.tmp_y
        
class Player1(Player):
    color = RED
    def __init__(self, x, y, game):
        super().__init__(x, y, game, self.color)

    def handle_event(self, event, keys):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.dx = -1
                self.dy = 0 
            elif event.key == pygame.K_RIGHT:
                self.dx = 1
                self.dy = 0
            elif event.key == pygame.K_UP:
                self.dy = -1
                self.dx = 0 
            elif event.key == pygame.K_DOWN:
                self.dy = 1
                self.dx = 0
        if keys[pygame.K_RSHIFT]:
            self.shift_pressed = True
        else:
            self.shift_pressed = False
    
    def tick(self):
        self.tmp_x = self.x
        self.tmp_y = self.y
        self.x += self.dx
        self.y += self.dy

class Player2(Player):
    color = BLUE
    def __init__(self, x, y, game):
        super().__init__(x, y, game, self.color)

    def handle_event(self, event, keys):
        if event.type == pygame.KEYDOWN:
            if event.key == ord('a'):
                self.dx = -1
                self.dy = 0 
            elif event.key == ord('d'):
                self.dx = 1
                self.dy = 0 
            elif event.key == ord('w'):
                self.dy = -1
                self.dx = 0 
            elif event.key == ord('s'):
                self.dy = 1
                self.dx = 0
        if keys[pygame.K_LSHIFT]:
            self.shift_pressed = True
        else:
            self.shift_pressed = False

    def tick(self):
        self.tmp_x = self.x
        self.tmp_y = self.y
        self.x += self.dx
        self.y += self.dy


class Food(GridObject):
    color = GREEN 
    def __init__(self, game):
        x = random.randint(0, game.n_cols-1)
        y = random.randint(0, game.n_rows-1)
        super().__init__(x, y, game, self.color)

class Game:
    block_size = 10
    def __init__(self, n_rows, n_cols):
        pygame.init()
        pygame.display.set_caption("DCCP Snake Game")
        self.display = pygame.display.set_mode((n_cols * self.block_size, n_rows * self.block_size))
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.objects = []

    def play(self, n_foods=20):
        player1 = Player1(60, 30, self)
        player2 = Player2(30, 30, self)
        foods = [Food(self) for _ in range(n_foods)]
        self.objects = [player1, player2, *foods]

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break

                # handle event 
                for obj in self.objects:
                    if obj.active:
                        keys = pygame.key.get_pressed()
                        obj.handle_event(event, keys)
            
            # tick
            for obj in self.objects:
                if obj.active:
                    obj.tick()
            
            # when snake is outside the box
            for obj in self.objects:
                if obj.active:
                    if obj.x > self.n_cols or obj.x < 0:
                        self.game_over = True
                        print("GAME OVER", obj.x, self.n_cols)
                    if obj.y > self.n_rows or obj.y < 0:
                        self.game_over = True
                        print("GAME OVER", obj.y, self.n_rows)

            # interact
            for obj1 in self.objects[:2]:
                for obj2 in self.objects:
                    if obj1 != obj2 and obj1.active and obj2.active:
                            obj1.interact(obj2)
                            obj2.interact(obj1)

            # tick one more if shift pressed
            for obj in self.objects:
                if obj.active and obj.shift_pressed:
                    obj.tick()

            # draw
            self.display.fill(BLACK)
            for obj in self.objects:
                if obj.active:
                    obj.draw()
            pygame.display.update()

            # Shutdown
            food_remains = False
            for obj in self.objects:
                if isinstance(obj, Food) and obj.active:
                    food_remains = True
            if not food_remains:
                self.game_over = True

            self.clock.tick(10)

if __name__ == "__main__":
    Game(n_rows=60, n_cols=80).play(n_foods=20)
