import pygame
import random

FOOD = (23, 119, 26) # GREEN
p1_HEAD = (255, 85, 0) # RED
p1_BODY = (151, 0, 0)
p2_HEAD = (0, 85, 255) # BLUE
p2_BODY = (0, 0, 151)
BACKGROUND = (252, 241, 200)


class Player():
    dx, dy = 0, 0
    speed = 1
    def __init__(self, display, block_size, p_coordinates, length):
        self.display = display
        self.block_size = block_size
        self.p_coordinates = p_coordinates # [(x_head, y_head), ...]
        self.length = length

    def tick(self):
        self.x_head += self.dx
        self.y_head += self.dy
        self.p_coordinates.append((self.x_head, self.y_head))
        if self.speed == 2:
            self.x_head += self.dx
            self.y_head += self.dy
            self.p_coordinates.append((self.x_head, self.y_head))     


class Player1(Player):
    x_head, y_head = 260, 300
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.dx, self.dy = -10, 0
            elif event.key == pygame.K_RIGHT:
                self.dx, self.dy = 10, 0
            elif event.key == pygame.K_UP:
                self.dx, self.dy = 0, -10
            elif event.key == pygame.K_DOWN:
                self.dx, self.dy = 0, 10
        
    def boost(self, event):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_RSHIFT]:
            self.speed = 2
        else:
            self.speed = 1

    def draw(self):
        pygame.draw.rect(self.display, p1_HEAD, [self.x_head, self.y_head, 10, 10]) # [x좌표, y좌표, 너비, 높이]
        while len(self.p_coordinates) > (self.length//10):
            del self.p_coordinates[0]
        if self.length >= 20:
            for i in range(self.length//10 - 1):
                pygame.draw.rect(self.display, p1_BODY, [self.p_coordinates[i][0], self.p_coordinates[i][1], 10, 10])   
                                     

class Player2(Player):
    x_head, y_head = 520, 300
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.dx, self.dy = -10, 0
            elif event.key == pygame.K_d:
                self.dx, self.dy = 10, 0
            elif event.key == pygame.K_w:
                self.dx, self.dy = 0, -10
            elif event.key == pygame.K_s:
                self.dx, self.dy = 0, 10
        
    def boost(self, event):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_LSHIFT]:
            self.speed = 2
        else:
            self.speed = 1

    def draw(self):
        pygame.draw.rect(self.display, p2_HEAD, [self.x_head, self.y_head, 10, 10]) # [x좌표, y좌표, 너비, 높이]
        while len(self.p_coordinates) > (self.length//10):
            del self.p_coordinates[0]
        if self.length >= 20:
            for i in range(self.length//10 - 1):
                pygame.draw.rect(self.display, p2_BODY, [self.p_coordinates[i][0], self.p_coordinates[i][1], 10, 10])   

    
class Food:
    active = True
    def __init__(self, display):
        self.x = random.randint(0, 79) * 10
        self.y = random.randint(0, 59) * 10
        self.display = display

    def draw(self):
        pygame.draw.rect(self.display, FOOD, [self.x, self.y, 10, 10])


class Game:
    block_size = 10
    def __init__(self, n_rows, n_cols):
        pygame.init()
        pygame.display.set_caption('냠 : Snake Game')
        self.display = pygame.display.set_mode((n_cols * self.block_size, n_rows * self.block_size))
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.clock = pygame.time.Clock()
        self.game_over = False
        
    def play(self, n_foods=20):
        player1 = Player1(self.display, self.block_size, [], 10)
        player2 = Player2(self.display, self.block_size, [], 10)
        foods = [Food(self.display) for _ in range(n_foods)]
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    self.game_over = True
                    break
                player1.handle_event(event)
                player2.handle_event(event)
                player1.boost(event)
                player2.boost(event)

            player1.tick()
            player2.tick()
            self.display.fill(BACKGROUND)
            player1.draw()
            player2.draw()
                    
            for food in foods:
                if food.active:
                    food.draw()

                if (food.x, food.y) in player1.p_coordinates:
                    food.active = False
                    i = foods.index(food)
                    del foods[i]
                    foods.insert(i, Food(self.display))
                    player1.length += 10

                if (food.x, food.y) in player2.p_coordinates:
                    food.active = False
                    i = foods.index(food)
                    del foods[i]
                    foods.insert(i, Food(self.display))
                    player2.length += 10
                
            pygame.display.update()

            if player1.x_head > self.n_cols * self.block_size or player1.x_head < 0 \
                or player1.y_head > self.n_rows * self.block_size or player1.y_head < 0:
                self.game_over = True # PLAYER1 화면 바깥으로 나감
            if player2.x_head > self.n_cols * self.block_size or player2.x_head < 0 \
                or player2.y_head > self.n_rows * self.block_size or player2.y_head < 0:
                self.game_over = True # PLAYER2 화면 바깥으로 나감
            
            if (player1.x_head, player1.y_head) in player1.p_coordinates[:player1.length//10 - 2] \
                or (player2.x_head, player2.y_head) in player2.p_coordinates[:player2.length//10 - 2]:
                self.game_over = True # PLAYER 자기 자신의 머리와 몸통이 겹침
            
            p1 = player1.p_coordinates
            p2 = player2.p_coordinates
            if list(set(p1).intersection(p2)) != []:
                self.game_over = True # PLAYER 서로의 머리와 몸통이 겹침

            self.clock.tick(10)


if __name__ == '__main__':
    Game(n_rows=60, n_cols=80).play(n_foods=20)