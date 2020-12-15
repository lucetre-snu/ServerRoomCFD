import pygame as p
import random

WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class GridObject:
    def __init__(self, x, y, game, color):
        self.game =game
        self.active = True
        self.color = color
        self.x = x
        self.y = y

    def move(self, event):
        pass

    def tick(self):
        pass

    def nowaxis(self):
        return self.x, self.y

    def draw(self):
        block_size = self.game.block_size
        p.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])

    def interact(self, other):
        pass


class Player(GridObject):
    bodycolor = BLACK
    dx = 0
    dy = 0

    def __init__(self, x, y, game, LEFT, RIGHT, UP, DOWN, COLOR, SHIFT):
        self.LEFT = LEFT
        self.RIGHT = RIGHT
        self.UP = UP
        self.DOWN = DOWN
        self.color = COLOR
        self.SHIFT = SHIFT
        super().__init__(x, y, game, self.color)

    def stop(self):
        self.x += 0
        self.y += 0

    def move(self, event):
        if event.type == p.KEYDOWN:
            if event.key == self.LEFT:
                if event.mod == self.SHIFT:
                    self.dx = -2
                else:
                    self.dx = -1
                self.dy = 0

            elif event.key == self.RIGHT:
                if event.mod == self.SHIFT:
                    self.dx = +2
                else:
                    self.dx = +1
                self.dy = 0
            elif event.key == self.UP:
                if event.mod == self.SHIFT:
                    self.dy = -2
                else:
                    self.dy = -1
                self.dx = 0
            elif event.key == self.DOWN:
                if event.mod == self.SHIFT:
                    self.dy = +2
                else:
                    self.dy = +1
                self.dx = 0

    def tick(self):
        self.x += self.dx
        self.y += self.dy

    def interact(self, other):
        if isinstance(other, Food):
            if self.x == other.x and self.y == other.y:
                other.active = False

class Food(GridObject):
    active = True
    color = GREEN
    def __init__(self, game):
        x = random.randint(0, game.n_cols -1)
        y = random.randint(0, game.n_rows -1)
        super().__init__(x, y, game, self.color)


class Game:
    block_size = 10
    def __init__(self, n_cols, n_rows):
        p.init()
        p.display.set_caption('Snake Game')
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.display_axis = n_cols*self.block_size, n_rows*self.block_size
        self.display = p.display.set_mode(self.display_axis)
        self.clock = p.time.Clock()
        self.game_over = False
        self.objects = []
        self.PlayerA = Player(60, 30, self, p.K_LEFT, p.K_RIGHT, p.K_UP, p.K_DOWN, RED, p.KMOD_RSHIFT)
        self.PlayerB = Player(30, 30, self, p.K_a, p.K_d, p.K_w, p.K_s, BLUE, p.KMOD_LSHIFT)


    def isactive(self):
        for obj in self.objects:
            if obj.active:
                yield obj

    def play(self, n_foods=20):

        self.objects = [self.PlayerA, self.PlayerB, *[Food(self) for _ in range(n_foods)]]

        while not self.game_over:
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.game_over = True
                    break

                #  Handle events
                for obj in self.isactive(): # active = True이
                    obj.move(event) # 좌우상하 움직면 dx

            # Tick
            for obj in self.isactive():
                obj.tick()  # x += dx


            # Is player in display range?a
            for i in 0, 1:
                for player in (self.PlayerA, self.PlayerB):
                    if player.nowaxis()[i] * self.block_size<0 or\
                            player.nowaxis()[i] * self.block_size>self.display_axis[i]:
                        player.stop()
                        self.game_over = True

            # Interact
            for obj1 in self.isactive():
                for obj2 in self.isactive():
                    obj1.interact(obj2)
                    obj2.interact(obj1)
                    if obj2.active is False:
                        self.objects.append(Food(self))

            #Draw
            self.display.fill(WHITE)
            for obj in self.isactive():
                obj.draw()

            p.display.update()

            # Global Decision
            food_remains = False
            for obj in self.isactive():
                if isinstance(obj, Food):
                    food_remains = True
            if not food_remains:
                self.game_over = True

            self.clock.tick(10)

if __name__ == "__main__":
    Game(n_rows=60, n_cols=80).play(n_foods=20)


