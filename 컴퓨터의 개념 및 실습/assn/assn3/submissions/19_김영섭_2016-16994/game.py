import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
RED_B = (255, 75, 75)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLUE_B = (75, 75, 255)

class Gridobject :
    def __init__(self, x, y, game, color) :
        self.game = game
        self.active = True
        self.color = color
        self.x = x # grid column index
        self.y = y # grid row index

    def handle_event(self, event) :
        pass
    
    def tick(self) :
        pass

    def draw(self) :
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])

    def interact(self, other) :
        pass

class Player1(Gridobject) :
    dx = 0
    dy = 0
    color = RED_B   
    tail_color = RED

    def __init__(self, x, y, game) :
        super().__init__(x, y, game, self.color) 
        self.tails = []
        self.prestate = [self.x, self.y]
        self.eaten = 1
        self.acceleration = 1

    def draw(self) :
        block_size = self.game.block_size
        if self.acceleration == 1 :
            if self.eaten == len(self.tails) :
                self.tails.insert(0, [self.x, self.y])
                self.tails.pop()
            else :
                self.tails.insert(0, [self.x, self.y])
        else : 
            if self.eaten == len(self.tails) :
                self.tails.insert(0, [(self.x + self.tails[0][0])//2, (self.y + self.tails[0][1])//2])
                self.tails.insert(0, [self.x, self.y])
                self.tails.pop()
                self.tails.pop()
            else :
                self.tails.insert(0, [(self.x + self.tails[0][0])//2, (self.y + self.tails[0][1])//2]) # when body len 1
                self.tails.pop(-1)
                self.tails.insert(0, [self.x, self.y])

        for tail in self.tails :
            pygame.draw.rect(self.game.display, self.tail_color, [block_size*tail[0], block_size*tail[1] , block_size, block_size])
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])
        self.prestate = [self.x, self.y]

    def handle_event(self, event) :
        self.acceleration = 1
        if event.type == pygame.KEYDOWN : 
            if event.key == pygame.K_RSHIFT :
                self.acceleration = 2 
            elif event.key == pygame.K_LEFT :
                self.dx = -1
                self.dy = 0
            elif event.key == pygame.K_RIGHT :
                self.dx = 1
                self.dy = 0
            elif event.key == pygame.K_UP :
                self.dx = 0
                self.dy = -1 
            elif event.key == pygame.K_DOWN :
                self.dx = 0
                self.dy = 1
        elif event.type == pygame.KEYUP :
            if event.key == pygame.K_RSHIFT :
                self.acceleration = 1

    def tick(self) :
        self.x += self.dx * self.acceleration
        self.y += self.dy * self.acceleration

    def interact(self, other) :
        if isinstance(other, Food) :
            if self.acceleration == 2 and len(self.tails) == 1 :
                if (self.x == other.x and self.y == other.y) or (self.x + self.prestate[0] == 2*other.x and self.y + self.prestate[1] == 2*other.y) :
                    other.active = False
                    self.eaten += 1
            else :
                if (self.x == other.x and self.y == other.y) or ([other.x, other.y] in self.tails) :
                    other.active = False
                    self.eaten += 1

class Player2(Player1) :
    color = BLUE_B
    tail_color = BLUE
    def handle_event(self, event) :
        self.acceleration = 1
        if event.type == pygame.KEYDOWN : 
            if event.key == pygame.K_LSHIFT :
                self.acceleration = 2 
            elif event.key == pygame.K_a :
                self.dx = -1
                self.dy = 0
            elif event.key == pygame.K_d :
                self.dx = 1
                self.dy = 0
            elif event.key == pygame.K_w :
                self.dx = 0
                self.dy = -1 
            elif event.key == pygame.K_s :
                self.dx = 0
                self.dy = 1
        elif event.type == pygame.KEYUP :
            if event.key == pygame.K_LSHIFT :
                self.acceleration = 1 #KEY AND SHIFT

class Food(Gridobject) :
    color = GREEN

    def __init__(self, game) :
        x = random.randint(0, game.n_cols-1)
        y = random.randint(0, game.n_rows-1)
        super().__init__(x, y, game, self.color)
        
class Game :
    block_size = 10
    def __init__(self, n_rows, n_cols) :
        pygame.init()
        pygame.display.set_caption('DCCP Snake Game')
        self.display = pygame.display.set_mode((n_cols*self.block_size, n_rows*self.block_size))
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.objects = []

    def active_objects(self) :
        for obj in self.objects :
            if obj.active :
                yield obj

    def play(self, n_foods = 20) :
        self.objects = [
            Player1(60, 30, self), # respawning
            Player2(20, 30, self),
            *[Food(self) for _ in range(n_foods)]
        ]
        player_1 = self.objects[0]
        player_2 = self.objects[1]
        temp = 0

        while not self.game_over :
            if  (not(0 <= player_1.x < self.n_cols)) or (not(0 <= player_1.y < self.n_rows)) :
                self.game_over = True
                break 

            if  (not(0 <= player_2.x < self.n_cols)) or (not(0 <= player_2.y < self.n_rows)) :
                self.game_over = True
                break        

            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    self.game_over = True
                    break

                for obj in self.active_objects() :
                    obj.handle_event(event)
            
            if [player_1.x, player_1.y] in player_1.tails[1:] :
                self.game_over = True
                break

            if [player_2.x, player_2.y] in player_2.tails[1:] :
                self.game_over = True
                break

            if [player_2.x, player_2.y] in player_1.tails : 
                self.game_over = True
                break

            if [player_1.x, player_1.y] in player_2.tails :
                self.game_over = True
                break
            
            if [player_1.x, player_1.y] == [player_2.x, player_2.y] :
                self.game_over = True
                break
  
            if temp != [food.active for food in self.objects[2:]].count(False) :
                self.objects.append(Food(self))
                temp = [food.active for food in self.objects[2:]].count(False)

            # tick
            for obj in self.objects :
                obj.tick()

            # interact
            for obj1 in self.active_objects() :
                for obj2 in self.active_objects() :
                    obj1.interact(obj2)
                    obj2.interact(obj1)

            # draw
            self.display.fill(BLACK)
            
            for obj in self.active_objects() :
                obj.draw()

            food_remains = False

            for obj in self.active_objects() :
                if isinstance(obj, Food)  :
                    food_remains = True

            if not food_remains :
                self.game_over = True

            pygame.display.update()     

            self.clock.tick(10)

if __name__ == '__main__' :
    Game(n_rows = 60, n_cols = 80).play(n_foods = 20)