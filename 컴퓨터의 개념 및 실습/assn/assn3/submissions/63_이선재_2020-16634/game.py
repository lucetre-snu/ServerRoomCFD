import random
import pygame 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHTRED = (255, 133, 122)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (115, 176, 255)

class GridObject:
    def __init__(self, x, y, game, maincolor):
        self.game = game
        self.active = True
        self.maincolor = maincolor
        self.x = x #grid column index
        self.y = y #grid row index

    def handle_event(self, event):
        pass
    def tick(self):
        pass
    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.maincolor, [self.x * block_size, self.y * block_size, block_size, block_size])

class Player(GridObject):
    dx = 0
    dy = 0
    prevx = 0
    prevy = 0
    
    def __init__(self, x, y, game, maincolor, subcolor):
        super().__init__(x, y, game, maincolor)
        self.length = 1
        self.subcolor = subcolor
        self.speed_level = 1
        self.snakechain = []
        self.midx = x
        self.midy = y
        
    def handle_event(self, event):
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.dx = -1
            self.dy = 0
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.dx = 1
            self.dy = 0
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.dx = 0
            self.dy = -1
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.dx = 0
            self.dy = 1
        elif event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
            self.speed_level += 1
    
    def update_snakechain(self):
        middle = [(self.prevx + self.x)//2, (self.prevy + self.y)//2]
        snakehead = [self.x, self.y]
        if middle != [self.prevx, self.prevy] and middle != snakehead:
            self.snakechain.append(middle)
            self.midx = middle[0]
            self.midy = middle[1]
        self.snakechain.append(snakehead)

        while len(self.snakechain) > self.length:
            del self.snakechain[0]

        for body in self.snakechain[:-1]:
            if body == snakehead:
                self.game.game_over = True
                break

    def player_collision(self, otherplayer):
        for body in otherplayer.snakechain:
            if ((self.x == body[0]) and (self.y == body[1])) or ((self.midx == body[0]) and (self.midy == body[1])):
                self.game.game_over = True

    def draw(self):
        block_size = self.game.block_size
        snakechain = self.snakechain
        for body in snakechain:
            if body == snakechain[-1]:
                pygame.draw.rect(self.game.display, self.maincolor, [body[0] * block_size, body[1] * block_size, block_size, block_size])
            else:
                pygame.draw.rect(self.game.display, self.subcolor, [body[0] * block_size, body[1] * block_size, block_size, block_size])

    def tick(self):
        self.prevx = self.x
        self.prevy = self.y
        self.x += self.dx*self.speed_level  
        self.y += self.dy*self.speed_level   


class Food(GridObject):
    maincolor = GREEN

    def __init__(self, game):
        x = random.randint(0, game.n_cols - 1)
        y = random.randint(0, game.n_rows - 1)
        super().__init__(x, y, game, self.maincolor)

class Game:
    block_size = 10

    def __init__(self, n_rows, n_cols):
        pygame.init()
        self.display = pygame.display.set_mode((n_cols*self.block_size, n_rows*self.block_size))
        self.n_rows = n_rows
        self.n_cols = n_cols
        pygame.display.set_caption('DCCP Snake Game')
        self.clock = pygame.time.Clock()
        self.game_over = False

    def play(self, n_foods=20):
        player1 = Player(60, 45, self, BLUE, LIGHTBLUE)
        player2 = Player(20, 15, self, RED, LIGHTRED)
        players = [player1, player2]

        arrow_controls = {pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RSHIFT}
        wasd_controls = {pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_LSHIFT}

        foods = [Food(self) for _ in range(n_foods)] # init food list

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key in arrow_controls:
                        player1.handle_event(event)
                    if event.key in wasd_controls:
                        player2.handle_event(event)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RSHIFT:
                        player1.speed_level -= 1
                    if event.key == pygame.K_LSHIFT:
                        player2.speed_level -= 1
            
            self.display.fill(BLACK)
            
            for player in players:  
                player.tick()
                player.update_snakechain()
                player.draw()

            player1.player_collision(player2) # check for collision between player 1 and 2
            player2.player_collision(player1)

            for food in foods: # draw food if active
                if food.active:
                    food.draw()
                
                for player in players: # If player touches food, eat and generate new food
                    if (player.x == food.x and player.y == food.y) or (player.midx == food.x and player.midy == food.y):
                        if food.active == True:
                            food.active = False
                            player.length += 1
                            
                            newfood = Food(self) #generate new food that doesn't overlap with players
                            while ([newfood.x, newfood.y] in player1.snakechain) or ([newfood.x, newfood.y] in player2.snakechain):
                                newfood = Food(self)
                            foods.append(newfood)                            
                
            pygame.display.update()             
            
            for player in players: # End game if any player exits frame
                if player.x < 0 or player.x > self.n_cols-1 or player.y < 0 or player.y > self.n_rows-1:
                    self.game_over = True
            

            self.clock.tick(10) 

if __name__ == "__main__":
    Game(n_rows=60, n_cols=80).play(n_foods=20)