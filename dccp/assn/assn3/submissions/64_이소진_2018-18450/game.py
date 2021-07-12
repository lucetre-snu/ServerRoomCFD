# youtube assn3 tutorial 영상을 다수 참고하였습니다.
import pygame
from colors import BLACK
from player import Player
from food import Food

class Game:
    block_size = 10
    def __init__(self, w, h):    # w = width, h = height
        pygame.init()
        pygame.display.set_caption('2018-18450 dccp59 Snake Game')
        self.display = pygame.display.set_mode((w * self.block_size, h * self.block_size))
        self.w = w
        self.h = h
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.objects = []        
    
    def active_object(self):
        for obj in self.objects:
            if obj.active:
                yield obj

    def __handle_event(self, event):
        for obj in self.active_object():
            obj.handle_event(event)

    def __tick(self):
        for obj in self.active_object():
            obj.tick()
            if obj.x < 0 or obj.x >= self.w or obj.y < 0 or obj.y >= self.h:    # 화면 밖으로 나가면 게임 종료
                self.game_over = True
                break
    
    def __interact(self):
        for obj1 in self.active_object():
            for obj2 in self.active_object():
                obj1.interact(obj2)
                obj2.interact(obj1)
    
    def __garbage_collect(self):
        for obj in self.objects:
            if not obj.active:
                self.objects.remove(obj)
    
    def __draw(self):
        self.display.fill(BLACK)
        for obj in self.active_object():
            obj.draw()
        pygame.display.update()

    def play(self, n_foods=20):
        self.objects = [
            Player(60, 40, self),
            Player(20, 20, self),
            *[Food(self) for _ in range(n_foods)]
        ]
        
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break
                self.__handle_event(event)
            self.__tick()
            self.__interact()
            self.__draw()
            self.__garbage_collect    # 먹힌 food를 object list에서 삭제
            self.clock.tick(10)

if __name__ == '__main__':
    Game(80, 60).play()