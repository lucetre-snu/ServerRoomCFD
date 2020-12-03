import pygame
import random as rd

[RIGHT, LEFT, UP, DOWN] = [[1,0], [-1,0], [0,-1], [0,1]]
MAP_SIZE=(100,50)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FOOD_COLOR = GREEN

BLOCK = 10 #한 칸의 크기
FPS = 8 #초당 8 프레임
class pixel:
    
    def __init__(self, position, color):
        self.position = position
        self.color = color

    def __del__(self):
        pass

    def draw(self):
        pygame.draw.rect(game_display, self.color, pygame.Rect(self.position,(BLOCK, BLOCK)))

class snake:
    speed = BLOCK #1틱 당 한 칸 전진
    length = 1
    game_over = False
    boost = False
    def __init__(self, position, direction, color):
        self.body_color=color
        self.head_color=(255-color[0],255-color[1],255-color[2])
        self.list = [pixel(position, self.head_color)]
        self.direction = direction
        self.speed = snake.speed
        self.length = snake.length
        self.game_over = snake.game_over
        self.boost = snake.boost

    def eat(self,f):
        self.length += 1
        del _food[_food.index(f)]

    def proceed(self):
        head=self.list[0]
        position=[head.position[0]+self.direction[0]*self.speed,
                  head.position[1]+self.direction[1]*self.speed]
        for f in _food:
            if position == f.position:
                self.eat(f)
        
        self.list[0].color=self.body_color
        del self.list[self.length-1:]
        self.list = [pixel(position, self.head_color)]+self.list
        
        self.check_lose()

    def check_lose(self):
        head_position=self.list[0].position
        if ((not 0 <=  head_position[0] <= (MAP_SIZE[0]-1)*BLOCK) 
            or (not 0 <= head_position[1] <= (MAP_SIZE[1]-1)*BLOCK)):
            self.lose()
            return
        for p in player:
            for b in p.list:
                if b.position == head_position and not p==self:
                    self.lose()
                    return


    def lose(self):
        self.game_over = True

    def turn(self, direction):
        if -self.direction[0]==direction[0] and -self.direction[1]==direction[1]:
            pass
        else:
            self.direction=direction



class food(pixel):
    
    def __init__(self, position, color):
        super().__init__(position, color)


pygame.init() #게임 시작

game_display = pygame.display.set_mode((MAP_SIZE[0]*BLOCK,
                                       MAP_SIZE[1]*BLOCK))
clock = pygame.time.Clock()
#화면 크기 800-600, 게임 시간 시작

pygame.display.set_caption('DCCP Snake Game')
#화면 이름 붙이기

def update_display():
    game_display.fill(BLACK)
    for p in player:
        for body in p.list[:]:
            body.draw()
    
    for f in _food:
        f.draw()
            
    pygame.display.update()

def add_player(pos,color):
    player.append(snake(pos, RIGHT, color))

def spawn_food():
    while len(_food) <= 20:
        x = rd.randint(0,MAP_SIZE[0]-1)
        y = rd.randint(0,MAP_SIZE[1]-1)
        for f in _food:
            if [x,y] == f.position:
                continue
        _food.append(food([BLOCK*x, BLOCK*y], FOOD_COLOR))

game_over = False
player = []
_food = []
add_player([200,200],BLUE)
add_player([600,200],RED)

while not game_over:
    clock.tick(FPS*2)
    spawn_food()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player[0].turn(RIGHT)
            elif event.key == pygame.K_LEFT:
                player[0].turn(LEFT)
            elif event.key == pygame.K_UP:
                player[0].turn(UP)
            elif event.key == pygame.K_DOWN:
                player[0].turn(DOWN)
            elif event.key == 1073742053:
                player[0].boost=True

            elif event.key == 100:
                player[1].turn(RIGHT)
            elif event.key == 97:
                player[1].turn(LEFT)
            elif event.key == 119:
                player[1].turn(UP)
            elif event.key == 115:
                player[1].turn(DOWN)
            elif event.key == 1073742049:
                player[1].boost=True

        elif event.type == pygame.KEYUP:
            if event.key == 1073742053:
                player[0].boost=False
            elif event.key == 1073742049:
                player[1].boost=False
    for p in player:
        p.proceed()
        if p.game_over:
            game_over=True
            break
        clock.tick(FPS*2)
        if p.boost:
            p.proceed()
            if p.game_over:
                game_over=True
                break
            
    

    update_display()





        
