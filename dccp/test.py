import pygame
import time
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
LIGHT_RED = (255, 175, 173)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
LIGHT_BLUE = (100, 237, 253)

class Object:
    def __init__(self, game, pos, color):
        self.game = game
        self.pos = pos
        self.color = color

    def draw(self):
        pygame.draw.rect(self.game.dis, self.color, 
        [self.pos[0], self.pos[1], self.game.BLOCK_SIZE, self.game.BLOCK_SIZE])

    def is_wrong_pos(self):
        return self.pos[0] >= self.game.dis_width or self.pos[0] < 0 or self.pos[1] >= self.game.dis_height or self.pos[1] < 0

    def is_same_pos(self, obj):
        return self.pos[0] == obj.pos[0] and self.pos[1] == obj.pos[1]
    
    def get_same_pos_objs(self):
        return list(filter(lambda obj: self.is_same_pos(obj), self.game.objects))

class Food(Object):
    def __init__(self, game, pos):
        Object.__init__(self, game, pos, GREEN)

class Snake(Object):
    def __init__(self, game, pos, color=BLUE, head_color=LIGHT_BLUE):
        self.body = [pos]
        self.length = 1
        self.boost_mode = False
        self.dir = ""
        self.head_color = head_color
        Object.__init__(self, game, pos, color)
        
    def turn(self, dir):
        self.dir = dir
        
    def move(self):
        n_iter = 1
        if self.boost_mode: n_iter += 1

        for _ in range(n_iter):
            new_pos = self.pos[:]
            if self.dir == 'left':      new_pos[0] -= self.game.BLOCK_SIZE
            elif self.dir == 'right':   new_pos[0] += self.game.BLOCK_SIZE
            elif self.dir == 'up':      new_pos[1] -= self.game.BLOCK_SIZE
            elif self.dir == 'down':    new_pos[1] += self.game.BLOCK_SIZE

            self.body.append(new_pos)
            if len(self.body) > self.length:
                del self.body[0]
            self.pos = new_pos

    def grow(self):
        self.length += 1

    def toggle_boost(self, boost_mode):
        self.boost_mode = boost_mode

    def draw(self):
        for x in self.body:
            pygame.draw.rect(self.game.dis, self.color,
            [x[0], x[1], self.game.BLOCK_SIZE, self.game.BLOCK_SIZE])
        pygame.draw.rect(self.game.dis, self.head_color, 
        [self.pos[0], self.pos[1], self.game.BLOCK_SIZE, self.game.BLOCK_SIZE])


class SnakeGame:
    BLOCK_SIZE = 10
    SPEED = 15
    def __init__(self, width, height):
        pygame.init()
 
        self.dis_width = width * self.BLOCK_SIZE
        self.dis_height = height * self.BLOCK_SIZE
        
        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption('DCCP Snake Game')
        
        self.clock = pygame.time.Clock()
        self.objects = []
        
    def print_log(self, msg):
        font_style = pygame.font.SysFont("consolas", 15)
        mesg = font_style.render(msg, True, WHITE)
        self.dis.blit(mesg, [0, 0])

    def create_food(self):
        while True:
            x = round(random.randrange(0, self.dis_width - self.BLOCK_SIZE) / self.BLOCK_SIZE) * self.BLOCK_SIZE
            y = round(random.randrange(0, self.dis_height - self.BLOCK_SIZE) / self.BLOCK_SIZE) * self.BLOCK_SIZE
            food = Food(self, [x, y])
            if len(food.get_same_pos_objs()): continue
            break
        self.objects.append(food)

    def start(self, food_count):
        LEFT_snake = Snake(self, [self.dis_width / 4, self.dis_height / 2])
        RIGHT_snake = Snake(self, [self.dis_width*3 / 4, self.dis_height / 2])
        self.objects.append(LEFT_snake)
        self.objects.append(RIGHT_snake)

        game_over = False
        game_close = False
        LEFT_lose = False
        RIGHT_lose = False

        for i in range(food_count):
            self.create_food()

        while not game_over:

            while game_close:
                if LEFT_lose:   self.print_log("RIGHT player won! Press any key to quit...")
                if RIGHT_lose: self.print_log("LEFT player won! Press any key to quit...")
    
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        game_over = True
                        game_close = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:           game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:    game_over = True
                    elif event.key == pygame.K_LEFT:    RIGHT_snake.turn('left')
                    elif event.key == pygame.K_RIGHT:   RIGHT_snake.turn('right')
                    elif event.key == pygame.K_UP:      RIGHT_snake.turn('up')
                    elif event.key == pygame.K_DOWN:    RIGHT_snake.turn('down')
                    elif event.key == pygame.K_RSHIFT:  RIGHT_snake.toggle_boost(True)
                    elif event.key == pygame.K_a:       LEFT_snake.turn('left')
                    elif event.key == pygame.K_d:       LEFT_snake.turn('right')
                    elif event.key == pygame.K_w:       LEFT_snake.turn('up')
                    elif event.key == pygame.K_s:       LEFT_snake.turn('down')
                    elif event.key == pygame.K_LSHIFT:  LEFT_snake.toggle_boost(True)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RSHIFT:    RIGHT_snake.toggle_boost(False)
                    if event.key == pygame.K_LSHIFT:    LEFT_snake.toggle_boost(False)
                    
            LEFT_snake.move()
            RIGHT_snake.move()

            if LEFT_snake.is_wrong_pos():
                LEFT_lose = True
                game_close = True
            if RIGHT_snake.is_wrong_pos():
                RIGHT_lose = True
                game_close = True

            for x in LEFT_snake.body[:-1]:
                if x == LEFT_snake.pos:
                    LEFT_lose = True
                    game_close = True
                if x == RIGHT_snake.pos:
                    RIGHT_lose = True
                    game_close = True

            for x in RIGHT_snake.body[:-1]:
                if x == LEFT_snake.pos:
                    LEFT_lose = True
                    game_close = True
                if x == RIGHT_snake.pos:
                    RIGHT_lose = True
                    game_close = True

            # display clear
            self.dis.fill(BLACK)
            #self.print_log(f"L player:{LEFT_snake.length}, R player:{RIGHT_snake.length}")

            for obj in self.objects: 
                obj.draw()
            pygame.display.update()

            objs = LEFT_snake.get_same_pos_objs()
            for obj in objs[1:]:
                if isinstance(obj, Food):
                    self.objects.remove(obj)
                    self.create_food()
                    LEFT_snake.grow()

            objs = RIGHT_snake.get_same_pos_objs()
            for obj in objs[1:]:
                if isinstance(obj, Food):
                    self.objects.remove(obj)
                    self.create_food()
                    RIGHT_snake.grow()
    
            self.clock.tick(self.SPEED)
        pygame.quit()
    
if __name__ == "__main__":
    SnakeGame(width=40, height=30).start(food_count=10)