import pygame
from pygame.constants import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_w, K_a, K_s, K_d, K_RSHIFT, K_LSHIFT
import random
import time
from colors import *

TILE_SIZE = 18

class GridObject():
    def __init__(self, x, y, game, color):
        self.game = game
        self.active = True
        self.color = color
        self.x = x
        self.y = y
    def handle_event(self, event):
        pass
    def tick(self):
        pass
    def draw(self):
        #draw rectangle: (display, RGB, [x,y,width,height])
        pygame.draw.rect(self.game.display, self.color, [self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE])
    def interact(self, other):
        pass

class Player(GridObject):
    def __init__(self, x, y, game, color, n):
        super().__init__(x, y, game, color)
        self.n = n #1P인지 2P인지
        self.dx = 0
        self.dy = 0
        self.speed = 1
        self.snake = []
        self.snake.append((self.x, self.y))
        self.prev_x = -1
        self.prev_y = -1
        self.head_color = tuple([x//3*2+80 for x in self.color]) #머리 밝은 색깔
        
    def handle_event(self, event):
        #Boost
        keys = pygame.key.get_pressed()
        if self.n == 1: #1P
            if keys[K_LSHIFT]:
                self.speed = 2
            else:
                self.speed = 1
        elif self.n == 2: #2P
            if keys[K_RSHIFT]:
                self.speed = 2
            else:
                self.speed = 1
                
        if event.type == KEYDOWN:
            #lP
            if self.n == 1:
                # 반대방향으로는 가지 못하게 함
                if len(self.snake)>1:
                    if event.key == K_a:
                        if self.dx != 1:
                            self.dx = -1
                            self.dy = 0
                    elif event.key == K_d:
                        if self.dx != -1:
                            self.dx = 1
                            self.dy = 0
                    elif event.key == K_w:
                        if self.dy != 1:
                            self.dy = -1
                            self.dx = 0
                    elif event.key == K_s:
                        if self.dy != -1:
                            self.dy = 1
                            self.dx = 0

                # 처음 길이 1일 때는 반대방향 갈 수 있음
                elif len(self.snake)==1:
                    if event.key == K_a:
                        self.dx = -1
                        self.dy = 0
                    elif event.key == K_d:
                        self.dx = 1
                        self.dy = 0
                    elif event.key == K_w:
                        self.dy = -1
                        self.dx = 0
                    elif event.key == K_s:
                        self.dy = 1
                        self.dx = 0
            
            #2P
            elif self.n == 2:
                # Boost  (ERROR!!! 방향 전환 시 부스터 씹힘)
                if event.key == K_RSHIFT:
                    self.speed = 2
                else:
                    self.speed = 1

                # 반대방향으로는 가지 못하게 함
                if len(self.snake)>1:
                    if event.key == K_LEFT:
                        if self.dx != 1:
                            self.dx = -1
                            self.dy = 0
                    elif event.key == K_RIGHT:
                        if self.dx != -1:
                            self.dx = 1
                            self.dy = 0
                    elif event.key == K_UP:
                        if self.dy != 1:
                            self.dy = -1
                            self.dx = 0
                    elif event.key == K_DOWN:
                        if self.dy != -1:
                            self.dy = 1
                            self.dx = 0
                # 처음 길이 1일 때는 반대방향 갈 수 있음
                elif len(self.snake)==1:
                    if event.key == K_LEFT:
                        self.dx = -1
                        self.dy = 0
                    elif event.key == K_RIGHT:
                        self.dx = 1
                        self.dy = 0
                    elif event.key == K_UP:
                        self.dy = -1
                        self.dx = 0
                    elif event.key == K_DOWN:
                        self.dy = 1
                        self.dx = 0

    def draw(self):
        # 몸통
        for a,b in self.snake[0:-1]:
            pygame.draw.rect(self.game.display, self.color, [a * TILE_SIZE, b * TILE_SIZE, TILE_SIZE, TILE_SIZE])
        # 머리
        pygame.draw.rect(self.game.display, self.head_color, [self.snake[-1][0] * TILE_SIZE, self.snake[-1][1] * TILE_SIZE, TILE_SIZE, TILE_SIZE])

        if self.speed == 1 or (self.speed == 2 and len(self.snake) == 1):
            self.snake.pop(0) #꼬리 지우고
            self.snake.append((self.x, self.y)) #머리 추가
        elif self.speed == 2 and len(self.snake)>1: 
            #두 칸씩 지우고, 추가
            self.snake.pop(0)
            self.snake.pop(0)
            self.snake.append((self.x-self.dx, self.y-self.dy))
            self.snake.append((self.x, self.y))
        
    def tick(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        
    def bite(self):
        if self.snake[-1] in self.snake[0:-1]:
            return True
        else:
            return False

    def interact(self, other, game):
        # 먹이를 먹으면 길이 길어짐
        if isinstance(other, Food):
            if ((self.x == other.x and self.y == other.y)
                or ( len(self.snake)>1 and self.snake[-2] == (other.x, other.y) )
                or ( self.speed==2 and (self.x-self.dx == other.x and self.y-self.dy == other.y)) 
                or (other.x,other.y) in self.snake):
                    self.prev_x, self.prev_y = self.x, self.y
                    self.tick()
                    if self.speed==2:
                        self.snake.append((self.x-self.dx, self.y-self.dy))
                        self.snake.pop(0)
                    self.snake.append((self.x, self.y))
        # 다른 뱀과 만나면 Game Over
        elif isinstance(other, Player):
            if ((self.x, self.y) in other.snake
                or (self.x-self.dx, self.y-self.dy) in other.snake):
                game.gameover("Snake is bitten!")

class Food(GridObject):
    color = GREEN
    def __init__(self, game):
        self.x = random.randint(0, game.WINDOW_WIDTH-1)
        self.y = random.randint(0, game.WINDOW_HEIGHT-1)
        super().__init__(self.x, self.y, game, self.color)

    def interact(self, other, game):
        # 뱀과 만날 경우 없어지고 다시 생성
        if isinstance(other, Player):
            if len(other.snake)>=2:
                if ((self.x == other.prev_x and self.y == other.prev_y)
                    or (self.x, self.y) == other.snake[-1]
                    or (self.x, self.y) == (other.x-other.dx*3, other.y-other.dy*3) 
                    or (self.x, self.y) in other.snake):
                    prev_x, prev_y = self.x, self.y
                    self.__init__(game)
                    # 현재랑 같은 위치에 생성될 경우 다시 생성
                    while self.x==prev_x and self.y==prev_y:
                        self.__init__(game)

class Game:
    def __init__(self, WINDOW_WIDTH = 80, WINDOW_HEIGHT = 40):
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        pygame.init()
        self.display = pygame.display.set_mode((self.WINDOW_WIDTH* TILE_SIZE, self.WINDOW_HEIGHT* TILE_SIZE))
        pygame.display.set_caption("BATTLE SNAKE")
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.objects = []

    def active_objects(self):
        for obj in self.objects:
            if obj.active:
                yield obj
    
    def __handle__event(self, event):
        for obj in self.active_objects():
            obj.handle_event(event)

    def gameover(self, reason):
        self.message("GAME OVER", 100, (self.WINDOW_WIDTH*TILE_SIZE//2, self.WINDOW_HEIGHT*TILE_SIZE//2))
        self.message(reason, 50, (self.WINDOW_WIDTH*TILE_SIZE//2, self.WINDOW_HEIGHT*TILE_SIZE//2+80))

        # game will restart in 5... 4...
        for i in range(5):
            if not self.game_over:
                self.message("game will restart in %d..."%(5-i), 50, (self.WINDOW_WIDTH*TILE_SIZE//2, self.WINDOW_HEIGHT*TILE_SIZE//2+150))
                time.sleep(1)
                # 숫자 겹쳐서 써지는 것을 막기위해 위해 검정색 덮어씌움
                # 아래는 WINDOW_WIDTH =80, WINDOW_HEIGHT = 40, TILE_SIZE=18 일 때만 적용됨
                if self.WINDOW_WIDTH == 80 and self.WINDOW_HEIGHT == 40 and TILE_SIZE == 18:
                    pygame.draw.rect(self.display, BLACK, [925, 485, 30, 45])
                    pygame.display.update()
                # X를 누르면 바로 창이 꺼짐   
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.game_over = True
                        break
            else:
                break

        self.play()

    def message(self, text:str, font_size:int, position: tuple):
        self.text = text
        self.font = pygame.font.Font('freesansbold.ttf', font_size)
        TextSurf, TextRect = self.text_objects(self.text, self.font)
        TextRect.center = (position)
        self.display.blit(TextSurf, TextRect)
        pygame.display.update()

    def text_objects(self, text, font):
        textSurface = font.render(text, True, WHITE)
        return textSurface, textSurface.get_rect()

    def play(self, n_foods=20):
        self.n_foods = n_foods
        Player1 = Player(self.WINDOW_WIDTH//3, self.WINDOW_HEIGHT/2, self, RED, 1)
        Player2 = Player(self.WINDOW_WIDTH*2//3, self.WINDOW_HEIGHT/2, self, BLUE, 2)
        self.objects = [Player1,
                        Player2,
                        *[Food(self) for _ in range(self.n_foods)]]
        while not self.game_over:
            for event in pygame.event.get():
                # X를 누르면 창이 꺼짐
                if event.type == QUIT:
                    self.game_over = True
                # Handle event
                self.__handle__event(event)            

            # Tick
            for obj in self.active_objects():
                obj.tick()
                
            # Draw
            self.display.fill(BLACK)  #Window color: fill RGB
            for obj in self.active_objects():
                obj.draw()
            pygame.display.update()
            
            # Interact        
            for obj1 in self.objects:
                for obj2 in self.objects:
                    if obj1!=obj2 and obj1.active and obj2.active:
                        obj1.interact(obj2, self)
                        obj2.interact(obj1, self)

            # Game over
            for obj in self.objects:
                if isinstance(obj, Player):
                    ## 테두리를 벗어나면 종료
                    if (obj.x<0 or obj.x>self.WINDOW_WIDTH-1 
                        or obj.y<0 or obj.y>self.WINDOW_HEIGHT-1):
                        self.gameover("%sP exceeded window" %obj.n)
                        
                    ## 자기 몸을 물면 종료
                    if len(obj.snake)>3:
                        if obj.bite():
                            self.gameover("%sP's snake bit itself" %obj.n)

                    ## 서로 물면 종료

            # #ticks per a second, #tiles per a second
            self.clock.tick(10) 

if __name__ == "__main__":
    Game(WINDOW_WIDTH = 80, WINDOW_HEIGHT = 40).play(n_foods=20)