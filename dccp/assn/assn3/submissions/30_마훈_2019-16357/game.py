import pygame
from random import randint

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

HEAD_RED = (255, 128, 128)
HEAD_BLUE = (128, 128, 255)

class Object():
    def __init__(self, color, x, y, tile_size, game_display):
        self.color = color
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.length = 1
        self.game_display = game_display
    
    def drawObject(self):
        pygame.draw.rect(self.game_display, self.color, [self.x*self.tile_size, self.y*self.tile_size, self.tile_size, self.tile_size])

class Food(Object):
    def __init__(self, color, x, y, tile_size, game_display):
        super().__init__(color, x, y, tile_size, game_display)

class Player(Object):
    def __init__(self, color, x, y, tile_size, game_display, head_color, upkey, downkey, leftkey, rightkey, boostkey):
        self.color = color
        self.body_coordinate_list = [BodyCoordinate(x, y, 0, 0)]
        self.length = 1
        self.tile_size = tile_size
        self.game_display = game_display
        self.head_color = head_color
        self.upkey = upkey
        self.downkey = downkey
        self.leftkey = leftkey
        self.rightkey = rightkey
        self.boostkey = boostkey
        self.boostON = False
    
    def eventHandler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.upkey:
                self.body_coordinate_list[0].setDir(0, -1)
            elif event.key == self.downkey:
                self.body_coordinate_list[0].setDir(0, 1)
            elif event.key == self.leftkey:
                self.body_coordinate_list[0].setDir(-1, 0)
            elif event.key == self.rightkey:
                self.body_coordinate_list[0].setDir(1, 0)
            
            if self.length == 2:
                next_dir = self.body_coordinate_list[0].getDir()
                last_dir = self.body_coordinate_list[1].getDir()

                if next_dir[0] + last_dir[0] == 0 and next_dir[1] + last_dir[1] == 0:
                    raise Exception
            
            if event.key == self.boostkey:
                self.boostON = True
        elif event.type == pygame.KEYUP:
            if event.key == self.boostkey:
                self.boostON = False
    
    def update(self):
        for i in range(self.length):
            self.body_coordinate_list[i].update()

        for i in range(self.length-1, 0, -1):
            next_dir = self.body_coordinate_list[i-1].getDir()
            self.body_coordinate_list[i].setDir(*next_dir)
    
    def foodEaten(self):
        self.length += 1
        last_pos, last_dir = self.body_coordinate_list[-1].getPos(), self.body_coordinate_list[-1].getDir()
        next_pos = []
        for i in range(2):
            next_pos.append(last_pos[i] - last_dir[i])
        self.body_coordinate_list.append(BodyCoordinate(next_pos[0], next_pos[1], last_dir[0], last_dir[1]))
    
    def drawObject(self):
        for i in range(self.length):
            pos = self.body_coordinate_list[i].getPos()
            if i == 0:
                pygame.draw.rect(self.game_display, self.head_color, [pos[0]*self.tile_size, pos[1]*self.tile_size, self.tile_size, self.tile_size])
            else:
                pygame.draw.rect(self.game_display, self.color, [pos[0]*self.tile_size, pos[1]*self.tile_size, self.tile_size, self.tile_size])
    
    def isInsideGrid(self, x_tile_lim, y_tile_lim):
        head_pos = self.getHeadPos()
        if 0 <= head_pos[0] <= x_tile_lim and 0 <= head_pos[1] <= y_tile_lim:
            return True
        else:
            return False
    
    def isBodyOverlapped(self, other):
        body_pos_list = self.getBodyPos()
        head_pos = body_pos_list[0]
        if head_pos in body_pos_list[1:]:
            return True
        
        if isinstance(other, Player):
            other_body_pos_list = other.getBodyPos()
            if len(set(body_pos_list) & set(other_body_pos_list)) != 0:
                return True

    def isBoosted(self):
        return self.boostON
    
    def getHeadPos(self):
        return self.body_coordinate_list[0].getPos()
    
    def getBodyPos(self):
        return [i.getPos() for i in self.body_coordinate_list]

class BodyCoordinate():
    def __init__(self, x, y, dx, dy):
        self.x, self.y = x, y
        self.dx, self.dy = dx, dy
    
    def getPos(self):
        return self.x, self.y
    
    def getDir(self):
        return self.dx, self.dy
    
    def setDir(self, dx, dy):
        self.dx, self.dy = dx, dy
    
    def update(self):
            self.x += self.dx
            self.y += self.dy

class Game():
    def __init__(self, x_tile, y_tile, tile_size):
        self.x_tile = x_tile
        self.y_tile = y_tile
        self.tile_size = tile_size

        pygame.init()
        self.game_display = pygame.display.set_mode((self.x_tile * self.tile_size, self.y_tile * self.tile_size))
        pygame.display.set_caption('DCCP Snake Game')
        self.clock = pygame.time.Clock()
        self.game_over = False
    
    def play(self):
        self.p1 = Player(RED, self.x_tile*3//4, self.y_tile//2, self.tile_size, self.game_display, HEAD_RED, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RSHIFT)
        self.p2 = Player(BLUE, self.x_tile//4, self.y_tile//2, self.tile_size, self.game_display, HEAD_BLUE, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LSHIFT)
        self.food_list = []
        self.food_coordinate = []
        while len(self.food_coordinate) != 20:
            new_food_coordinate = (randint(1, self.x_tile-1), randint(1, self.y_tile-1))
            if new_food_coordinate not in self.food_coordinate:
                self.food_coordinate.append(new_food_coordinate)
                self.food_list.append(Food(GREEN, new_food_coordinate[0], new_food_coordinate[1], self.tile_size, self.game_display))
       
        self.game_display.fill(BLACK)
        pygame.display.update()

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break

                try:
                    self.p1.eventHandler(event)
                    self.p2.eventHandler(event)
                except:
                    self.game_over = True
                    break

            for player in (self.p1, self.p2):
                if player.isBoosted():
                    repeatNum = 2
                else:
                    repeatNum = 1
                
                repeat = 0
                while repeat < repeatNum:
                    repeat += 1
                    player.update()
                    other = (set([self.p1, self.p2]) - set([player])).pop()
                    if not player.isInsideGrid(self.x_tile, self.y_tile) or player.isBodyOverlapped(other):
                        self.game_over = True
                        break

                    i = 0
                    foodEaten = False
                    while i < len(self.food_list):
                        if player.getHeadPos() == self.food_coordinate[i]:
                            foodEaten = True
                            player.foodEaten()
                            del self.food_list[i]
                            del self.food_coordinate[i]
                            break
                        else:
                            i += 1
                    
                    if foodEaten:
                            while True:
                                new_food_coordinate = (randint(1, self.x_tile-1), randint(1, self.y_tile-1))
                                if new_food_coordinate not in self.food_coordinate:
                                    self.food_coordinate.append(new_food_coordinate)
                                    self.food_list.append(Food(GREEN, new_food_coordinate[0], new_food_coordinate[1], self.tile_size, self.game_display))
                                    break

            self.game_display.fill(BLACK)
            for gameObj in (self.p1, self.p2, *self.food_list):
                gameObj.drawObject()
            pygame.display.update()
            self.clock.tick(10)

if __name__ == '__main__':
    newgame = Game(80, 60, 10)
    newgame.play()