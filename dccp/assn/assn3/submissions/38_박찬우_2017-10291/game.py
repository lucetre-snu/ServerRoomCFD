import pygame as pg
import random

#Global Constants
##Colors
BLACK = (0,0,0)
RED = (255, 0, 0)
BRIGHTRED = (255,204,204)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BRIGHTBLUE = (51,51,255)
WHITE = (255, 255, 255)
DEFUALT = WHITE
FOODCOLOR = GREEN
PLAYER1COLORS = (RED, BRIGHTRED)
PLAYER2COLORS = (BLUE, BRIGHTBLUE)
##Directions
GOUP = (0, -1)
GODOWN = (0, 1)
GOLEFT = (-1, 0)
GORIGHT = (1, 0)
##Keyboard Arguments
KEYLIST1 = [pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT, pg.KMOD_RSHIFT]
KEYLIST2 = [pg.K_w, pg.K_s, pg.K_a, pg.K_d, pg.KMOD_LSHIFT]
##Other Cosntants
FPS = 10

class Game():
    tilesize = 10
    players = []
    foods = []

    def __init__(self, x, y):
        self.cols = x
        self.rows = y
        pg.init()
        pg.display.set_caption('2017-10291 Chanwoo Park')
        self.display = pg.display.set_mode((self.cols * self.tilesize, self.rows * self.tilesize))
        self.clock = pg.time.Clock()
        self.game_over = False
        GridObject.display = self.display
        Food.game = self
        Player.game = self

    def check_game_over(self):
        pass

    def play(self, nfood, playernum = 1):

        for i in range(nfood):
            Food()

        if playernum == 1:
            Player((self.cols//2, self.rows//2)).set_name('player 1')
        elif playernum == 2:
            Player((self.cols * 2//3, self.rows//2)).set_name('player 1')
            Player((self.cols//3, self.rows//2), KEYLIST2, PLAYER2COLORS).set_name('PUBG')

        while not self.game_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_over = True
                for player in self.players:
                    player.handle_event(event)
            #tick & interact : do twice if boosted
            for player in self.players:
                #print(player, player.boost)
                for i in range(player.boost + 1):
                    player.tick()
                    for player2 in self.players:
                        player.interact(player2)
                        player2.interact(player)
                    for food in self.foods:
                        player.interact(food)

            #draw
            self.display.fill(BLACK)
            for player in self.players:
                player.draw()
            for food in self.foods:
                food.draw()
            pg.display.update()

            #aftermath
            for player in self.players:
                #print(player.live)
                if not player.live: self.game_over = True
                player.set_boost()

            self.clock.tick(FPS)

    def position_empty(self, cord):
        for player in self.players:
            for obj in player.loc:
                if obj.cord == cord:
                    return False
        for obj in self.foods:
            if obj.cord == cord:
                return False
        return True

    def print_foods(self):
        pass
        '''print('print_foods called')
        i = 0
        for food in self.foods:
            print(food, end = '\t')
            i += 1
            if i % 5 == 0:
                print()
                i = 0
        print()'''


class GridObject(Game):
    game = None
    display = None
    def __init__(self, cord, color):
        self.cord = cord
        self.color = color

    def tick(self):
        pass

    def draw(self):
        size = self.tilesize
        pg.draw.rect(self.display, self.color, list(map(lambda x: 10 * x, self.cord))+[size,size])
        pass

    def handle_event(self):
        pass

class Player(Game):
    game = None
    def __init__(self, cord, keylist = KEYLIST1, colors = PLAYER1COLORS):
        self.set_colors(colors)
        self.loc = [PlayerBody(cord, self.headcolor, self)]
        self.len = 1
        self.direction = (0,0)
        self.live = True
        self.boost = False
        self.treat = 0
        self.players.append(self)
        self.set_keycontrol(keylist)

    def set_name(self, name):
        self.name = name

    def __str__(self):
        return self.name +' len: ' +str(self.len)

    def tick(self):
        self.move()
        if self.out_of_grid(): self.live = False

    def move(self):
        x = self.loc[0].cord[0] + self.direction[0]
        y = self.loc[0].cord[1] + self.direction[1]
        self.loc.insert(0, PlayerBody((x, y), self.headcolor, self))
        self.loc[1].color = self.bodycolor
        if not self.treat:
            self.toremove = self.loc.pop()
        else:
            self.treat -= 1

    def out_of_grid(self):
        x, y = self.loc[0].cord
        return not (x in range(0, self.game.cols) and y in range(0, self.game.rows))

    def interact(self, other):
        head = self.loc[0]
        if isinstance(other, Player):
            otherhead = [other.loc[0]]
            if self == other: otherhead = []
            for obj in( other.loc[1:] + otherhead):
                if head.cord == obj.cord:
                    self.live = False
                    return 1
        elif isinstance(other, Food):
            if head.cord == other.cord:
                self.eat(other)

    def draw(self):
        for obj in self.loc[:self.len]:
            obj.draw()

    def eat(self, other):
        self.len += 1
        self.treat += 1
        self.game.foods.remove(other)
        Food()

    def set_colors(self, colors):
        self.headcolor = colors[0]
        self.bodycolor = colors[1]

    def set_keycontrol(self, keylist):
        self.keycontrol = keylist
        self.keyup = keylist[0]
        self.keydown = keylist[1]
        self.keyleft = keylist[2]
        self.keyright = keylist[3]
        self.keyboost = keylist[4]

    def handle_event(self, event):
        key = None
        if event.type == pg.KEYDOWN:
            key = event.key
        if key == self.keyup and (not self.direction == GODOWN):
            self.direction = GOUP
        elif key == self.keydown and (not self.direction == GOUP):
            self.direction = GODOWN
        elif key == self.keyleft and (not self.direction == GORIGHT):
            self.direction = GOLEFT
        elif key == self.keyright and (not self.direction == GOLEFT):
            self.direction = GORIGHT

    def set_boost(self):
        #print(pg.key.get_mods())
        if (pg.key.get_mods() & self.keyboost):
            self.boost = 1
        else: self.boost = 0

class PlayerBody(GridObject):
    def __init__(self, cord, color, player):
        super().__init__(cord, color)
        self.player = player

class Food(GridObject):
    game = None
    color = FOODCOLOR
    def __init__(self):
        #generate pos if pos empty
        while True:
            x = random.randint(0, self.game.cols - 1)
            y = random.randint(0, self.game.rows - 1)
            if self.game.position_empty((x,y)): break
        super().__init__((x, y), FOODCOLOR)
        self.foods.append(self)

    def __str__(self):
        return 'FoodObject: '+str(self.cord)

if __name__ == "__main__":
    Game(80, 60).play(20, 2)
