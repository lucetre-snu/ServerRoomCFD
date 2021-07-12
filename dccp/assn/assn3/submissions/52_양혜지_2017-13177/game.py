import pygame
import random
 
pygame.init()

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED1 = (255, 0, 0)
RED2 = (150, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 0, 150)
GREEN = (0, 255, 0)

# KEYSETS
keyset1 = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RSHIFT]
keyset2 = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_LSHIFT]

# DISPLAY
width = 800
height = 600
 
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('DCCP Snake Game')
clock = pygame.time.Clock()

unit = 10
tick = 10

# START PONIT
Q = [0, 0]
M = [width-unit, height-unit]

########## CLASS PLAYER ##########
class Player:

    dx = 0
    dy = 0
    boost = False
    
    def __init__(self, display, start, keyset):
        self.display = display
        self.keyset = keyset
        self.x = start[0]
        self.y = start[1]
        self.bodylen = 1
        self.head = []
        self.body = []
        self.direction = ''

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.keyset[0]:
                self.dx = -unit
                self.dy = 0
                self.direction = 0
            elif event.key == self.keyset[1]:
                self.dx = unit
                self.dy = 0
                self.direction = 1
            elif event.key == self.keyset[2]:
                self.dx = 0
                self.dy = -unit
                self.direction = 2
            elif event.key == self.keyset[3]:
                self.dx = 0
                self.dy = unit
                self.direction = 3

    def tick(self):
        if self.boost:
            self.x += self.dx*2
            self.y += self.dy*2
        else:
            self.x += self.dx
            self.y += self.dy

    def grow(self):
        self.head = [self.x, self.y]
        self.body.append(self.head)
        if len(self.body) > self.bodylen:
            del self.body[0]

    def draw(self, color1, color2):
        for i in range(len(self.body)):
            if i == len(self.body)-1:
                pygame.draw.rect(game_display, color1, [self.body[i][0], self.body[i][1], unit, unit])
            else:
                pygame.draw.rect(game_display, color2, [self.body[i][0], self.body[i][1], unit, unit])

########## CLASS FOOD ##########
class food:
    active = True
    
    def __init__(self, x, y, display):
        self.x = x
        self.y = y
        self.display = display
    
    def check_active(self, player):
        if player.boost:
            if player.direction == 0:
                if player.x+unit == self.x and player.y == self.y:
                    player.bodylen += 1
                    self.active = False
            if player.direction == 1:
                if player.x-unit == self.x and player.y == self.y:
                    player.bodylen += 1
                    self.active = False
            if player.direction == 2:
                if player.x == self.x and player.y+unit == self.y:
                    player.bodylen += 1
                    self.active = False
            if player.direction == 3:
                if player.x == self.x and player.y-unit == self.y:
                    player.bodylen += 1
                    self.active = False
        if player.x == self.x and player.y == self.y:
            player.bodylen += 1
            self.active = False
            
    
    def draw(self):
        pygame.draw.rect(self.display, GREEN, [self.x, self.y, unit, unit])

########## 종료 조건 ##########

# 종료 조건 1: display 밖으로 나가면 return True
def check_range(player):
    if (player.x > width) or (player.x < 0) or (player.y > height) or (player.y < 0):
        return True
    else:
        return False

# 종료 조건 2: 머리가 몸/머리와 접촉하면 return True
def check_cross(player1, player2):
    for block in player1.body[:-1]:
        if (block == player1.head):
            return True
    for block in player1.body:
        if (block == player2.head):
            return True
    else:
        return False

########## MAIN ##########

# 먹이 설정
rx = width/unit - 1
ry = height/unit - 1
food_num = 20

foods = [food(random.randint(0, rx)*unit, random.randint(0, ry)*unit, game_display) for f in range(food_num)]

# Player 설정
p1 = Player(game_display, M, keyset1)
p2 = Player(game_display, Q, keyset2)

# GAME
game_over = False

while not game_over:

    p1.boost = False
    p2.boost = False

    game_display.fill(BLACK)

    # EVENT; 종료 조건 1: x 누름
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            break
        p1.handle_event(event)
        p2.handle_event(event)

    pygame.event.pump()
    key_list = pygame.key.get_pressed()
    if key_list[p1.keyset[4]]:
        p1.boost = True
    if key_list[p2.keyset[4]]:
        p2.boost = True

    p1.tick()
    p2.tick()

    # 밥 먹으면 재생성 + snake 길이 증가 + 그리기
    for fd_s in foods:
        if fd_s.active:
            fd_s.draw()

        fd_s.check_active(p1)
        fd_s.check_active(p2)
        
        while not fd_s.active:
            fd_s.x = random.randint(0, rx)*unit
            fd_s.y = random.randint(0, ry)*unit
            for fd_o in foods:
                if (fd_s.x == fd_o.x) and (fd_s.y == fd_o.y):
                    pass
                else:
                    fd_s.active = True
                    fd_s.draw()
    
    p1.grow()
    p2.grow()
    p1.draw(RED1, RED2)
    p2.draw(BLUE1, BLUE2)

    # 종료 조건
    if check_range(p1) or check_range(p2) or check_cross(p1, p2) or check_cross(p2, p1):
        game_over = True

    # 업데이트
    pygame.display.update()
    
    clock.tick(tick)

# 덤으로 먹은 먹이 개수 PRINT...!
if game_over == True:
    print('############## SCORE ##############')
    print('player1(RED): ', p1.bodylen-1, 'player2(BLUE): ', p2.bodylen-1)
