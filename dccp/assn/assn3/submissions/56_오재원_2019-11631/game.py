import random
import pygame

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
RED_s = (255,167,167)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLUE_s = (178,204,255)


class Player1:
    x = 600
    y = 300
    dx = 0
    dy = 0

    def __init__(self, display):
        self.display = display
        self.position = [(self.x, self.y)]

    def handel_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if len(self.position) >1 and self.dx == 10 and self.dy == 0:
                    return
                self.dx = -10
                self.dy = 0
            elif event.key == pygame.K_RIGHT:
                if len(self.position) >1 and self.dx == -10 and self.dy == 0:
                    return
                self.dx = 10
                self.dy = 0
            elif event.key == pygame.K_UP:
                if len(self.position) >1 and self.dx == 0 and self.dy == 10:
                    return
                self.dx = 0
                self.dy = -10               
            elif event.key == pygame.K_DOWN:
                if len(self.position) >1 and self.dx == 0 and self.dy == -10:
                    return
                self.dx = 0
                self.dy = 10
        
            
    def tick(self):
        self.x += self.dx
        self.y += self.dy
        a = self.x + self.dx * 2
        b = self.y + self.dy * 2
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RSHIFT]:
            self.x = a; self.y = b
        else:
            pass

    def draw(self):
        pygame.draw.rect(self.display, RED_s, [self.x,self.y,10,10])

    def draw_body(self):
        self.position.append((self.x, self.y))
        del self.position[0]

        for (x,y) in self.position[:-1]:
            pygame.draw.rect(self.display, RED, [x,y,10,10])
    
    def extend(self):
        self.position.append((self.x, self.y))

        for (x,y) in self.position[:-1]:
            pygame.draw.rect(self.display, RED, [x,y,10,10])

class Player2:
    x = 200
    y = 300
    dx = 0
    dy = 0

    def __init__(self, display):
        self.display = display
        self.position = [(self.x, self.y)]

    def handel_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                if len(self.position) >1 and self.dx == 10 and self.dy == 0:
                    return
                self.dx = -10
                self.dy = 0
            elif event.key == pygame.K_d:
                if len(self.position) >1 and self.dx == -10 and self.dy == 0:
                    return
                self.dx = 10
                self.dy = 0
            elif event.key == pygame.K_w:
                if len(self.position) >1 and self.dx == 0 and self.dy == 10:
                    return
                self.dx = 0
                self.dy = -10               
            elif event.key == pygame.K_s:
                if len(self.position) >1 and self.dx == 0 and self.dy == -10:
                    return
                self.dx = 0
                self.dy = 10
        
    def tick(self):
        self.x += self.dx
        self.y += self.dy
        a = self.x + self.dx * 2
        b = self.y + self.dy * 2
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            self.x = a; self.y = b
        else:
            pass


    def draw(self):
        pygame.draw.rect(self.display, BLUE_s, [self.x,self.y,10,10])



    def draw_body(self):
        self.position.append((self.x, self.y))
        del self.position[0]

        for (x,y) in self.position[:-1]:
            pygame.draw.rect(self.display, BLUE, [x,y,10,10])
    
    def extend(self):
        self.position.append((self.x, self.y))

        for (x,y) in self.position[:-1]:
            pygame.draw.rect(self.display, BLUE, [x,y,10,10])

class Food:
    active = True
    def __init__(self, display):
        self.x = random.randint(0, 79) * 10
        self.y = random.randint(0, 59) * 10
        self.display = display

    def draw(self):
        pygame.draw.rect(self.display, GREEN, [self.x,self.y,10,10])

class Game:
    block_size = 10
    def __init__(self, n_rows, n_cols):
        pygame.init()
        pygame.display.set_caption("DCCP Snake game")
        self.display = pygame.display.set_mode((n_cols * self.block_size,n_rows * self.block_size))
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.clock = pygame.time.Clock()
        self.game_over = False

    def play(self, n_foods = 20):
        players = [Player1(self.display), Player2(self.display)]
        foods = [Food(self.display) for _ in range(n_foods)]

        while not self.game_over:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break
                for player in players:
                    player.handel_event(event)
                
            for player in players:
                player.tick()
            
            self.display.fill(BLACK)
            for player in players:
                player.draw()
            
            for food in foods:
                if food.active:
                    food.draw()

                    for player in players:
                        if player.x == food.x and player.y == food.y:
                            food.active = False
                            foods.append(Food(self.display))    
                            player.extend()
                else:
                    pass

            for player in players:
                player.draw_body()


            for player in players:
                for (x,y) in player.position[:-2]:
                    if (player.x == x and player.y == y):
                        self.game_over = True


            food_remains = False 
            for food in foods:
                if food.active:
                    food_remains = True
            if not food_remains:
                self.game_over = True 

            for player in players:
                if player.x > self.n_cols * self.block_size or player.x < 0 or player.y > self.n_rows * self.block_size or player.y < 0:
                    self.game_over = True
            

            for (x1,x2) in players[0].position:
                for (y1,y2) in players[1].position:
                    if x1==y1 and x2==y2:
                        self.game_over = True
            
            pygame.display.update() 
            self.clock.tick(10)




if __name__ == "__main__":
    Game(n_rows = 60, n_cols = 80).play(n_foods=20)
    
