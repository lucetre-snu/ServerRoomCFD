import pygame
import random

pygame.init()

class Constants:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    ORANGE = (255, 165, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    SKY_BLUE = (135, 206, 235)

class Tile():
    def __init__(self, game, pos, color):
        self.game = game
        self.size = game.tile_size
        self.display = game.display
        self.pos = pos
        self.color = color
    
    def draw(self):
        pygame.draw.rect(self.display, self.color, 
        [self.size * self.pos[0], self.size * self.pos[1], self.size, self.size]
        )

class Snake(Tile):
    def __init__(self, game, pos, color_head, color_body, number):
        Tile.__init__(self, game, pos, color_head)
        self.dx, self.dy = 0, 0
        self.color_body = color_body
        self.body_length = 0
        self.number = number
        self.speed = game.default_snake_speed
        self.past = [self.pos]
        self.eat_count = 0
        self.eat_switch = False
        self.boost_switch = False
        self.death = False
    
    def change_direction(self):
        if self.number == 1 and game.current_event.type == pygame.KEYDOWN:
            if self.game.current_event.key == pygame.K_LEFT:
                if self.dx == 1 and self.dy == 0:
                    pass
                else:
                    self.dx, self.dy = -1, 0
            elif self.game.current_event.key == pygame.K_RIGHT:
                if self.dx == -1 and self.dy == 0:
                    pass
                else:
                    self.dx, self.dy = 1, 0
            elif self.game.current_event.key == pygame.K_UP:
                if self.dx == 0 and self.dy == 1:
                    pass
                else:
                    self.dx, self.dy = 0, -1
            elif self.game.current_event.key == pygame.K_DOWN:
                if self.dx == 0 and self.dy == -1:
                    pass
                else:
                    self.dx, self.dy = 0, 1
        elif self.number == 2 and game.current_event.type == pygame.KEYDOWN:
            if self.game.current_event.key == pygame.K_a:
                if self.dx == 1 and self.dy == 0:
                    pass
                else:
                    self.dx, self.dy = -1, 0
            elif self.game.current_event.key == pygame.K_d:
                if self.dx == -1 and self.dy == 0:
                    pass
                else:
                    self.dx, self.dy = 1, 0
            elif self.game.current_event.key == pygame.K_w:
                if self.dx == 0 and self.dy == 1:
                    pass
                else:
                    self.dx, self.dy = 0, -1
            elif self.game.current_event.key == pygame.K_s:
                if self.dx == 0 and self.dy == -1:
                    pass
                else:
                    self.dx, self.dy = 0, 1

    def boost(self):
        if self.number == 1:
            if self.game.current_event.type == pygame.KEYDOWN and \
                self.game.current_event.key == pygame.K_RSHIFT:
                self.speed = 2 * self.game.default_snake_speed
                self.boost_switch = True
            elif self.game.current_event.type == pygame.KEYUP and \
                self.game.current_event.key == pygame.K_RSHIFT:
                self.speed = self.game.default_snake_speed
                self.boost_switch = False
        elif self.number == 2:
            if self.game.current_event.type == pygame.KEYDOWN and \
                self.game.current_event.key == pygame.K_LSHIFT:
                self.speed = 2 * self.game.default_snake_speed
                self.boost_switch = True
            elif self.game.current_event.type == pygame.KEYUP and \
                self.game.current_event.key == pygame.K_LSHIFT:
                self.speed = self.game.default_snake_speed
                self.boost_switch = False

    def move(self):
        self.pos = (
            self.pos[0] + self.speed * self.dx,
            self.pos[1] + self.speed * self.dy
        )
        if self.boost_switch:
            self.past.insert(0, 
                (self.past[0][0] + self.game.default_snake_speed * self.dx, self.past[0][1] + self.game.default_snake_speed * self.dy)
            )

    def eat(self, food):
        self.eat_switch = False
        if self.pos == food.pos:
            self.eat_count += 1
            self.eat_switch = True
        if self.boost_switch and self.past[0] == food.pos:
            self.eat_count += 1
            self.eat_switch = True

    def outside(self):
        if self.pos[0] < 0 or \
            self.pos[0] >= self.game.n_row or \
            self.pos[1] < 0 or \
            self.pos[1] >= self.game.n_col:
            self.death = True

    def collude_me(self):
        if self.pos in self.past[:self.body_length]:
            self.death = True

    def collude_another(self, another):
        if self.pos == another.pos or \
            self.pos in another.past[:another.body_length]:
            self.death = True 

    def draw_tails(self):
        for i in range(self.body_length):
            # print(self.past)
            # print(self.body_length)
            tail = Tile(self.game, self.past[i], self.color_body)
            tail.draw()

    def next(self):
        self.past.insert(0, self.pos)
        self.body_length += self.eat_count
        if self.boost_switch:
            if self.eat_count == 0:
                self.past.remove(self.past[-2])
                self.past.remove(self.past[-1])
            elif self.eat_count == 1:
                self.past.remove(self.past[-1])
        else:
            if self.eat_count == 0:
                self.past.remove(self.past[-1])
        self.eat_count = 0

class Food(Tile):
    def test_duplication(self):
        if len(self.game.Foods) == 0:
            return False
        elif self.pos in [food.pos for food in self.game.Foods]:
            return True
        elif self.pos == self.game.snake_1.pos:
            return True
        elif self.pos in self.game.snake_1.past[:self.game.snake_1.body_length]:
            return True
        elif self.pos == self.game.snake_2.pos:
            return True
        elif self.pos in self.game.snake_2.past[:self.game.snake_2.body_length]:
            return True
        else:
            return False


class Snake_Game:
    def __init__(self, *, n_row, n_col, caption,
        n_food, colors, tile_size, default_snake_speed, 
        fps):
        self.n_col = n_col
        self.n_row = n_row
        self.display = pygame.display.set_mode((n_row * tile_size, n_col * tile_size))
        pygame.display.set_caption(f"{caption}")
        self.n_food = n_food
        self.colors = colors
        self.tile_size = tile_size
        self.default_snake_speed = default_snake_speed
        self.fps = fps
        self.game_over = False
        self.current_event = None
        self.Foods = []
        self.snake_1 = None
        self.snake_2 = None

    def start(self):
        self.display.fill(Constants.BLACK)

        self.snake_1 = Snake(self, (self.n_row - 1, self.n_col - 1), 
            self.colors[0], self.colors[1], 1)
        self.snake_1.draw()

        self.snake_2 = Snake(self, (0, 0), 
            self.colors[2], self.colors[3], 2)
        self.snake_2.draw()

        while len(self.Foods) < self.n_food:
            food = Food(self, 
                (random.randint(0, self.n_row - 1), random.randint(0, self.n_col - 1)), 
                self.colors[4])
            if (not food.test_duplication()):
                self.Foods.append(food)
        
        for fd in self.Foods:
            fd.draw()
        
        pygame.display.update()

    def play(self):
        self.start()
        while not self.game_over:
            for event in pygame.event.get():
                self.current_event = event
                self.quit()
                if self.quit():
                    break

                self.snake_1.change_direction()
                self.snake_2.change_direction()

                self.snake_1.boost()
                self.snake_2.boost()

            self.snake_1.move()
            self.snake_2.move()

            # print(self.snake_1.past)
            # print(self.snake_1.pos)

            self.eat()

            self.snake_1.outside()
            self.snake_2.outside()

            self.snake_1.collude_me()
            self.snake_2.collude_me()

            self.snake_1.collude_another(self.snake_2)
            self.snake_2.collude_another(self.snake_1)

            self.display.fill(Constants.BLACK)

            self.snake_1.draw()
            self.snake_1.draw_tails()
            self.snake_2.draw()
            self.snake_2.draw_tails()

            for food in self.Foods:
                food.draw()
                
            pygame.display.update()

            self.snake_1.next()
            self.snake_2.next()

            self.test_game_over()
            
            pygame.time.Clock().tick(self.fps)
    
    def eat(self):
        for food in self.Foods:
            self.snake_1.eat(food)
            if self.snake_1.eat_switch:
                self.Foods.remove(food)

        while len(self.Foods) < self.n_food:
            new_food = Food(self, 
            (random.randint(0, self.n_row - 1), random.randint(0, self.n_col - 1)), 
            self.colors[4])
            if not new_food.test_duplication():
                self.Foods.append(new_food)

        for food in self.Foods:
            self.snake_2.eat(food)
            if self.snake_2.eat_switch:
                self.Foods.remove(food)

        while len(self.Foods) < self.n_food:
            new_food = Food(self, 
            (random.randint(0, self.n_row - 1), random.randint(0, self.n_col - 1)), 
            self.colors[4])
            if not new_food.test_duplication():
                self.Foods.append(new_food)
    
    def test_game_over(self):
        if self.snake_1.death or self.snake_2.death:
            self.game_over = True
            return True

    def quit(self):
        if self.current_event.type == pygame.QUIT:
            self.game_over = True
            return True
        else:
            return False

game = Snake_Game(
    n_col = 60,
    n_row = 80,
    caption = "DCCP_Snake_Game_2016-10147",
    n_food = 20,
    colors = [Constants.RED, Constants.ORANGE, Constants.BLUE, Constants.SKY_BLUE, Constants.GREEN],
    tile_size = 10,
    default_snake_speed = 1,
    fps = 10
)

game.play()