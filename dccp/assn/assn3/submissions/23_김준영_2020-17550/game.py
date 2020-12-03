import pygame
import random

pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
PINK = (255,100,100)
GREEN = (0,255,0)
BLUE = (0,0,255)
GREY = (200,200,200)
YELLOW = (255,255,0)

class GridObject:
    def __init__(self, x, y, game, color):
        self.game = game
        self.active = True
        self.color = color
        self.x = x #grid column index
        self.y = y #gird row index

    def handle_event(self, event):
        pass

    def tick(self):
        pass

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x*block_size,self.y*block_size,block_size, block_size])


class Player1(GridObject):
    dx = 0
    dy = 0
    ticks = 1
    score = 0
    score_s = 0

    def __init__(self, x, y, game, color=WHITE):
        self.color = color
        super().__init__(x, y, game, self.color)
        self.place = [self.x, self.y]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.dx = -1
                self.dy = 0
            elif event.key == pygame.K_RIGHT:                
                self.dx = 1
                self.dy = 0
            elif event.key == pygame.K_UP:                
                self.dx = 0
                self.dy = -1
            elif event.key == pygame.K_DOWN:
                self.dx = 0
                self.dy = 1
            elif event.key == pygame.K_RSHIFT:
                self.ticks = self.ticks*2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RSHIFT:
                self.ticks = self.ticks//2

    def tick(self):
        self.x += self.dx
        self.y += self.dy

class Player2(GridObject):
    dx = 0
    dy = 0
    ticks = 1
    score = 0
    score_s = 0

    def __init__(self, x, y, game, color=RED):
        self.color = color
        super().__init__(x, y, game, self.color)
        self.place = [self.x, self.y]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == ord("a"):
                self.dx = -1
                self.dy = 0
            elif event.key == ord("d"):                
                self.dx = 1
                self.dy = 0
            elif event.key == ord("w"):                
                self.dx = 0
                self.dy = -1
            elif event.key == ord("s"):
                self.dx = 0
                self.dy = 1
            elif event.key ==  pygame.K_LSHIFT:
                self.ticks = self.ticks*2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                self.ticks = self.ticks//2

    def tick(self):
        self.x += self.dx
        self.y += self.dy

class Food(GridObject):
    color = GREEN

    def __init__(self, game):
        x = random.randint(0, game.n_cols - 1)
        y = random.randint(0, game.n_rows - 1)
        super().__init__(x, y, game, self.color)

class Game:
    block_size = 10
    def __init__(self, n_rows, n_cols):
        pygame.init()
        pygame.display.set_caption("DCCP Snake Game")
        self.display = pygame.display.set_mode((n_cols*self.block_size,n_rows*self.block_size))
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.stop = False
        self.result = ""

    def show_info(self, player, score, ticks, location=0):
        font = pygame.font.Font(None, 32)
        text = font.render("score: "+str(score)+", speed: "+str(ticks), True, GREY)
        if location == 0:
            self.display.blit(text, (10,5))
        elif location == 1:
            self.display.blit(text, (590, 5))

    def show_again(self, score1, score2):
        font = pygame.font.Font(None, 30)
        GO = font.render("GAME OVER", True, YELLOW)
        self.display.blit(GO, (350,250))
        text = font.render("Press ENTER to continue, SPACE to quit", True, YELLOW)
        self.display.blit(text,(225,300))

        # if score1 > score2:
        #     text_result = font.render("Player1 Wins!", True, YELLOW)
        # elif score1 < score2:
        #     text_result = font.render("Player2 Wins!", True, YELLOW)
        # elif score1 == score2: 
        #     text_result = font.render("Both Tied", True, YELLOW)
        # self.display.blit(text_result, (370, 220))

    def play(self, n_foods=20):
        player = Player1(40, 30, self)
        player2 = Player2(30, 40, self)
        playertail = [player]
        playertail2 = [player2]
        foods = [Food(self) for _ in range(n_foods)]

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break
                ##
                if self.stop == True:
                    if event.type == pygame.KEYDOWN:
                        if event.key == ord("\r"):
                            return True
                        if event.key == pygame.K_SPACE:
                            return False
                eventinput = event
                #print(eventinput)
                player.handle_event(eventinput)
                player2.handle_event(eventinput)


            for i in range(player.ticks):
                #playertail follow
                for i in range(len(playertail)-1):
                    playertail[-(i+1)].x = playertail[-(i+2)].x
                    playertail[-(i+1)].y = playertail[-(i+2)].y

                #player move                
                player.tick()

                #player draw
                self.display.fill(BLACK)
                for i in range(len(playertail)-1):
                    playertail[i+1].draw()
                player.draw()

                #players crush
                for i in playertail[1:]:
                    if player.x == i.x and player.y == i.y:
                        #print("player1 crushed!")
                        #self.game_over = True
                        self.stop = True
                
                for i in playertail:
                    if player2.x == i.x and player2.y == i.y:
                        #self.game_over = True
                        self.stop = True
                        #print("you both crushed!")
                
                #player eat food
                for food in foods:
                    if food.active:
                        food.draw()

                        if player.x == food.x and player.y == food.y:
                            #create another food
                            food.active = False
                            foods.append(Food(self))
                            
                            #lengthen player
                            playertail.append(Player1(playertail[-1].x, playertail[-1].y, self, GREY))
                            player.score += 1; 
                            if player.score == 10:
                                player.ticks += 1; player.score_s = player.score
                            if player.score - player.score_s == 30: 
                                player.ticks += 1; player.score_s = player.score
                            #print(player.score)


            for i in range(player2.ticks):
                for i in range(len(playertail2)-1):
                    playertail2[-(i+1)].x = playertail2[-(i+2)].x
                    playertail2[-(i+1)].y = playertail2[-(i+2)].y

                #player2 tick
                player2.tick()

                #player2 crush
                
                for i in playertail2[1:]:
                    if player2.x == i.x and player2.y == i.y:
                        #print("player2 crushed!")
                        #self.game_over = True
                        self.stop = True
                
                for i in playertail2:
                    if player.x == i.x and player.y == i.y:
                        #self.game_over = True
                        self.stop = True
                        #print("You both crushed!")

                
                #player draw
                for i in range(len(playertail2)-1):
                    playertail2[i+1].draw()
                player2.draw()

                #food and player interact
                for food in foods:
                    if food.active:
                        food.draw()
                        
                        if player2.x == food.x and player2.y == food.y:
                            #create another food
                            food.active = False
                            foods.append(Food(self))
                            
                            #lengthen player2
                            playertail2.append(Player2(playertail2[-1].x, playertail2[-1].y, self, PINK))
                            player2.score += 1
                            if player2.score == 10:
                                player2.ticks += 1; player2.score_s = player2.score
                            if player2.score - player2.score_s == 30: 
                                player2.ticks += 1; player2.score_s = player2.score
                            #print(player2.score)
                
            self.show_info("player1", player.score, player.ticks, 1)
            self.show_info("player2", player2.score, player2.ticks, 0)

            #player out of range
            if player.x >= self.n_cols or player.x <= 0 or player.y >= self.n_rows or player.y <= 0:
                self.stop = True
                #self.game_over = True

            if player2.x >= self.n_cols or player2.x <= 0 or player2.y >= self.n_rows or player2.y <= 0:
                self.stop = True
                #self.game_over = True
            
            if self.stop == True:
                player.ticks = 0; player2.ticks = 0
                #self.show_again(pygame.event.get())
                self.show_again(player.score, player2.score)

            pygame.display.update()

            self.clock.tick(10)
        

if __name__ == "__main__":
    game_over = False
    while game_over != True:
        start = Game(n_rows=60, n_cols=80).play(n_foods=20)
        if start  == True:
            pass
        else: break
