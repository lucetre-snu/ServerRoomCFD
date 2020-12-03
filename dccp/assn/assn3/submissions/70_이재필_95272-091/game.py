import pygame as pg
import time
import random

class Tail:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.prevX = x
        self.prevY = y

fruitColors = (
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (255,255,255)
)

BLOCK_SIZE = 20
TILE_WIDTH = 80
TILE_HEIGHT = 40
RANDOM_SCORE = False


pg.init()
screen = pg.display.set_mode((BLOCK_SIZE*TILE_WIDTH,BLOCK_SIZE*TILE_HEIGHT))


class Fruit:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score
    def render(self):
        pg.draw.rect(screen, fruitColors[self.score], pg.Rect(self.x*BLOCK_SIZE, self.y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

class Board:
    def __init__(self):
        self.fruits = []

    def makeFruits(self,n):
        self.fruits = []
        for i in range(n):
            x = random.randrange(0, TILE_WIDTH)
            y = random.randrange(0, TILE_HEIGHT)
            score = random.randrange(1, 8) if RANDOM_SCORE else 1
            fruit = Fruit(x, y, score)
            self.fruits.append(fruit)

    def check(self, x, y):
        for e in self.fruits:
            if abs(e.x - x) < 1 and abs(e.y - y) < 1:
                self.fruits.remove(e)

                x = random.randrange(0, TILE_WIDTH)
                y = random.randrange(0, TILE_HEIGHT)
                score = random.randrange(1, 8) if RANDOM_SCORE else 1
                fruit = Fruit(x, y, score)
                self.fruits.append(fruit)

                return e.score
        return 0

    def render(self):
        for e in self.fruits:
            e.render()

def checkBox(x1,y1,prevX1, prevY1, x2, y2, prevX2, prevY2):
    difX1 = (x1 - prevX1)/10
    difY1 = (y1 - prevY1)/10
    difX2 = (x2 - prevX2)/10
    difY2 = (y2 - prevY2)/10

    chx1 = prevX1
    chy1 = prevY1
    chx2 = prevX2
    chy2 = prevY2

    for i in range(10):
        if abs(chx1 - chx2) < 1 and abs(chy1 - chy2) < 1:
            return True
        chx1 += difX1
        chy1 += difY1
        chx2 += difX2
        chy2 += difY2
    return False

class Snake:
    def __init__(self, x, y, headColor, tailColor):
        self.x = x
        self.y = y
        self.prevX = x
        self.prevY = y
        self.tails = []
        self.add = 0
        self.direction = (0,1)
        self.boost = False
        self.start = False
        self.headColor = headColor
        self.tailColor = tailColor

    def check(self, oppoent):
        if self != oppoent:
            if checkBox(self.x, self.y, self.prevX, self.prevY, oppoent.x, oppoent.y, oppoent.prevX, oppoent.prevY):
                return False
            for e in oppoent.tails:
                if checkBox(self.x, self.y, self.prevX, self.prevY, e.x, e.y, e.prevX, e.prevY):
                    return False
        else:
            for e in oppoent.tails:
                if abs(self.x-e.x) < 1 and abs(self.y-e.y) <1:
                    return False

        return True

    def setBoost(self, v):
        self.boost = v

    def update(self):
        if self.start == False:
            return True
        return self.move(self.direction) and self.check(self)
    
    def setDirection(self, dir):
        self.start = True
        self.direction = dir

    def move(self, dir):
        x = self.x
        y = self.y

        self.prevX = self.x
        self.prevY = self.y
        self.x += dir[0]
        self.y += dir[1]

        if self.x < 0 or self.x >= TILE_WIDTH or self.y < 0 or self.y >= TILE_HEIGHT:
            return False

        if len(self.tails) > 0:
            if abs(self.x - self.tails[0].x) < 1 and abs(self.y - self.tails[0].y) < 1:
                return False

        lastX = self.x
        lastY = self.y
        for e in self.tails:
            nX = e.x
            nY = e.y
            e.prevX = e.x
            e.prevY = e.y
            lastX = e.x = x
            lastY = e.y = y
            x = nX
            y = nY
        
        if self.add > 0:
            self.add -= 1
            self.tails.append(Tail(x, y))
        
        return True
    
    def addTail(self,n):
        self.add += n
    def render(self):
        pg.draw.rect(screen, self.headColor, pg.Rect(self.x*BLOCK_SIZE, self.y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        for e in self.tails:
            pg.draw.rect(screen, self.tailColor, pg.Rect(e.x*BLOCK_SIZE,e.y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def makeSnake(n):
    if n == 0:
        return Snake(TILE_WIDTH//2-10, TILE_HEIGHT//2, (255, 128, 0), (0, 128, 128))
    else:
        return Snake(TILE_WIDTH//2+10, TILE_HEIGHT//2, (0, 128, 255), (128, 128, 0))

gameContinue = True
gameBoard = Board()
gameBoard.makeFruits(20)
snake = makeSnake(0)
snake2 = makeSnake(1)
prevTick = time.time()*1000.0
while gameContinue:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameContinue = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                snake.setDirection((-1,0))
            elif event.key == pg.K_w:
                snake.setDirection((0, -1))
            elif event.key == pg.K_s:
                snake.setDirection((0,1))
            elif event.key == pg.K_d:
                snake.setDirection((1,0))
            elif event.key == pg.K_LSHIFT:
                snake.setBoost(True)
            elif event.key == pg.K_LEFT:
                snake2.setDirection((-1,0))
            elif event.key == pg.K_UP:
                snake2.setDirection((0, -1))
            elif event.key == pg.K_DOWN:
                snake2.setDirection((0,1))
            elif event.key == pg.K_RIGHT:
                snake2.setDirection((1,0))
            elif event.key == pg.K_RSHIFT:
                snake2.setBoost(True)
        if event.type == pg.KEYUP:
            if event.key == pg.K_RSHIFT:
                snake2.setBoost(False)
            elif event.key == pg.K_LSHIFT:
                snake.setBoost(False)

    curTick = time.time() * 1000.0
    if curTick - prevTick > 100:
        prevTick = curTick
        snake.addTail(gameBoard.check(snake.x, snake.y))
        if snake.update() != True:
            gameContinue = False
        snake2.addTail(gameBoard.check(snake2.x, snake2.y))
        if snake2.update() != True:
            gameContinue = False
        crashRet1 = snake.check(snake2)
        crashRet2 = snake2.check(snake)
        if crashRet1 != True:
            gameContinue = False
        if crashRet2 != True:
            gameContinue = False
        if snake.boost:
            snake.addTail(gameBoard.check(snake.x, snake.y))
            if snake.update() != True:
                gameContinue = False
        if snake2.boost:
            snake2.addTail(gameBoard.check(snake2.x, snake2.y))
            if snake2.update() != True:
                gameContinue = False
        if snake.boost or snake2.boost:
            crashRet1 = snake.check(snake2)
            crashRet2 = snake2.check(snake)
            if crashRet1 != True:
                gameContinue = False
            if crashRet2 != True:
                gameContinue = False
    
    screen.fill((0,0,0))
    gameBoard.render()
    snake.render()
    snake2.render()
    pg.display.flip()
