import pygame
import random

# CONSTANTS
## COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTRED = (255, 127, 127)
LIGHTBLUE = (127, 127, 255)

## DISPLAY
X_PIXEL, Y_PIXEL = 80, 60
TILE_SIZE = 10
DISPLAY_SIZE = (X_PIXEL * TILE_SIZE, Y_PIXEL * TILE_SIZE)
DISPLAY_CAPTION = 'Battle Snake by 2020-19851 오이석'
FPS = 10

## GAME_INFO
FOOD_NUM = 20
PLAYER1_KEYS = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_LSHIFT]
PLAYER2_KEYS = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RSHIFT]
PLAYER1_COORDINATES = (100, 300)
PLAYER2_COORDINATES = (700, 300)

# classes
class character():
    def __init__(self, coordinates = False):
        try:
            self.x = coordinates[0]
            self.y = coordinates[1]
        except:
            self.x = 0
            self.y = 0
        
    # 화면에 표시됨
    # 위치 정보 변수
    def draw(self, color, display):
        pygame.draw.rect(display, color, [self.x, self.y, TILE_SIZE, TILE_SIZE]) # 색(r, g, b), [x, y, w, h]; 위치&크기


class player(character):
    D = TILE_SIZE # 이동 속도 (기본)
    def __init__(self, keys, coordinates = False):
        self.left = keys[0]
        self.right = keys[1]
        self.up = keys[2]
        self.down = keys[3]
        self.boost = keys[4]
        
        super().__init__(coordinates)
        self.dx = 0
        self.dy = 0
        self.boosted = 1
        
    def movement(self, updown, key_input):
        if updown == 'down':
            if key_input == self.left: self.dx, self.dy = - player.D, 0
            elif key_input == self.right: self.dx, self.dy = player.D, 0
            elif key_input == self.up: self.dx, self.dy = 0, - player.D
            elif key_input == self.down: self.dx, self.dy = 0, player.D

            if key_input == self.boost:
                self.boosted = 2
        elif updown == 'up':
            if key_input == self.boost and self.boosted == 2:
                self.boosted = 1


class food(character):
    coordinates = {}
    def __init__(self):
        super().__init__(self)
        self.random_placement()


    def random_placement(self):
        self.x = random.randint(0,X_PIXEL - 1) * TILE_SIZE # randint(a,b): a와 b 사이의 임의의 정수
        self.y = random.randint(0,Y_PIXEL - 1) * TILE_SIZE
        if (self.x, self.y) in food.coordinates:
            self.random_placement()
        elif (self.x, self.y) in moving_coordinates_1 or (self.x, self.y) in moving_coordinates_2:
            self.random_placement() 
        else:
            food.coordinates[(self.x, self.y)] = self


class clone(character):
    def __init__(self, original):
        self.x = original.x
        self.y = original.y



def update_display(display):
    display.fill(BLACK) # 이거 안해주면 아까 그거에 아래 rectangle이 덮어쓰인다.
    for food in foods:
        food.draw(GREEN, display)
    for c1 in clones1[1:]:
        c1.draw(LIGHTRED, display)
    for c2 in clones2[1:]:
        c2.draw(LIGHTBLUE, display)        
    player1.draw(RED, display)
    player2.draw(BLUE, display)

    pygame.display.update() # display update


# variables
game_display = pygame.display.set_mode(DISPLAY_SIZE)
clock = pygame.time.Clock()
game_over = False
i = 0
moving_coordinates_1 = []
moving_coordinates_2 = []

# instances
player1 = player(PLAYER1_KEYS, PLAYER1_COORDINATES)
player2 = player(PLAYER2_KEYS, PLAYER2_COORDINATES)
foods = [food() for _ in range(FOOD_NUM)]
clones1 = [player1]
clones2 = [player2]


# main program
pygame.init() # pygame 실행
pygame.display.set_caption(DISPLAY_CAPTION)

while not game_over:
    if player1.x < 0 or player1.y < 0 or player1.x >= DISPLAY_SIZE[0] or \
        player1.y >= DISPLAY_SIZE[1] or player2.x < 0 or player2.y < 0 or player2.x >= DISPLAY_SIZE[0] or player2.y >= DISPLAY_SIZE[1]:
        #print("나가서 죽음")
        game_over = True
    elif (player1.x, player1.y) in moving_coordinates_1[1:] or (player1.x, player1.y) in moving_coordinates_2:
        #print("1번이 죽거나 2번 꼬리 묾")
        game_over = True
    elif (player2.x, player2.y) in moving_coordinates_1 or (player2.x, player2.y) in moving_coordinates_2[1:]:
        #print("2번이 죽거나 1번 꼬리 묾")
        game_over = True
    
    elif (player1.x, player1.y) in food.coordinates:
        food.coordinates[(player1.x, player1.y)].random_placement()
        del food.coordinates[(player1.x, player1.y)]
        clones1.append(clone(clones1[-1]))
    
    elif (player2.x, player2.y) in food.coordinates:
        food.coordinates[(player2.x, player2.y)].random_placement()
        del food.coordinates[(player2.x, player2.y)]
        clones2.append(clone(clones2[-1]))

    if player1.boosted == 2 or player2.boosted == 2:
        if (player1.x - player1.dx, player1.y - player1.dy) in food.coordinates:
            food.coordinates[(player1.x - player1.dx, player1.y - player1.dy)].random_placement()
            del food.coordinates[(player1.x - player1.dx, player1.y - player1.dy)]
            clones1.append(clone(clones1[-1]))
    
        if (player2.x - player2.dx, player2.y - player2.dy) in food.coordinates:
            food.coordinates[(player2.x - player2.dx, player2.y - player2.dy)].random_placement()
            del food.coordinates[(player2.x - player2.dx, player2.y - player2.dy)]
            clones2.append(clone(clones2[-1]))

        if player1.boosted == 2:
            if (player1.x - player1.dx, player1.y - player1.dy) in moving_coordinates_1[2:] or (player1.x - player1.dx, player1.y - player1.dy) in moving_coordinates_2:
                game_over = True

        if player2.boosted == 2:
            if (player2.x - player2.dx, player2.y - player2.dy) in moving_coordinates_1 or (player2.x - player2.dx, player2.y - player2.dy) in moving_coordinates_2[2:]:
                game_over = True
    
    if (player1.dx * player2.dx) < 0 and player1.y == player2.y:
        if (player1.x - player2.x) * ((player1.x - player1.dx * player1.boosted) - (player2.x - player2.dx * player2.boosted)) <= 0:
            game_over = True
    elif (player1.dy * player2.dy) < 0 and player1.x == player2.x:
        if (player1.y - player2.y) * ((player1.y - player1.dy * player1.boosted) - (player2.y - player2.dy * player2.boosted)) <= 0:
            game_over = True

    temp = (player1.dx, player1.dy, player2.dx, player2.dy)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #print("종료 버튼 누름")
            game_over = True
        else:
            if event.type == pygame.KEYDOWN:
                player1.movement('down', event.key)
                player2.movement('down', event.key)
            if event.type == pygame.KEYUP:
                player1.movement('up', event.key)
                player2.movement('up', event.key)

    if player1.dx * temp[0] < 0 or player1.dy * temp[1] < 0 or player2.dx * temp[2] < 0 or player2.dy * temp[3] < 0:
        game_over = True 

    for _ in range(player1.boosted):
        for i in range(len(clones1) - 1):
            clones1[-(i+1)].x, clones1[-(i+1)].y = clones1[-(i+2)].x, clones1[-(i+2)].y

        player1.x += player1.dx 
        player1.y += player1.dy 

    for _ in range(player2.boosted):
        for i in range(len(clones2) - 1):
            clones2[-(i+1)].x, clones2[-(i+1)].y = clones2[-(i+2)].x, clones2[-(i+2)].y  

        player2.x += player2.dx 
        player2.y += player2.dy 

    moving_coordinates_1 = [(c1.x, c1.y) for c1 in clones1] # 클론을 포함한 위치정보
    moving_coordinates_2 = [(c2.x, c2.y) for c2 in clones2] # 클론을 포함한 위치정보


    update_display(game_display)
    pygame.display.update() #display update
    
    # print("\nplayer1: ", moving_coordinates_1)
    # print("player2: ", moving_coordinates_2)

    clock.tick(FPS)