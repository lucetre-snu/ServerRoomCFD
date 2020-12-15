import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

HEAD_1 = (254, 195, 198)
TAIL_1 = (254, 117, 119)
HEAD_2 = (194, 195, 255)
TAIL_2 = (124, 125, 255)

class GridObject:

    def __init__(self, x, y, game, color):
        self.x = x
        self.y = y
        self.game = game
        self.color = color

    def draw(self):
        b = self.game.BLOCK_SIZE
        pygame.draw.rect(self.game.display, self.color, [self.x*b, self.y*b, b, b])


class Player(GridObject):

    dx = 0
    dy = 0
    boost = 0

    def __init__(self, x, y, game, color, tailcolor, left, right, up, down, boostkey):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.boostkey = boostkey
        self.tailcolor = tailcolor
        super().__init__(x, y, game, color)


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.left:
                self.dx = -1
                self.dy = 0
            elif event.key == self.right:
                self.dx = 1
                self.dy = 0
            elif event.key == self.up:
                self.dx = 0
                self.dy = -1
            elif event.key == self.down:
                self.dx = 0
                self.dy = 1
            elif event.key == self.boostkey:
                self.boost = 1-self.boost
        elif event.type == pygame.KEYUP:
            if event.key == self.boostkey:
                self.boost = 1-self.boost

    def update(self):
        self.x += self.dx*(1+self.boost)
        self.y += self.dy*(1+self.boost)


    def handle_tails(self, tails):
        if len(tails) > 0:
            tails[0].follow(self, self)
            for i in range(len(tails)-1):
                tails[i+1].follow(self, tails[i])
        for tail in tails:
            tail.draw()
    
    def eat(self, tails, foods):
        for food in foods[:]:
            food.draw()
            if self.boost == 1:
                for tail in tails:
                    if tail.x == food.x and tail.y == food.y:
                        foods.remove(food)
                        tails.append(Tail(-100, -100, self.game, self.tailcolor))
            if self.x == food.x and self.y == food.y:
                foods.remove(food)
                tails.append(Tail(-100, -100, self.game, self.tailcolor))
        if len(foods) < self.game.n_foods:
            foods.append(Food(self.game))

    def kill(self, other, othertails):
        for tail in othertails:
            if self.x == tail.x and self.y == tail.y:
                self.game.game_over = True
                break

class Tail(GridObject):

    def follow(self, head, lead):
        self.lx = self.x
        self.ly = self.y
        self.x = lead.x-lead.dx
        self.y = lead.y-lead.dy
        if abs((self.x-self.lx)/(1+head.boost)) == 1/2:
            self.dx = lead.dx
            self.dy = lead.dy
        else:
            self.dx = (self.x-self.lx)/(1+head.boost)
            self.dy = (self.y-self.ly)/(1+head.boost)

class Food(GridObject):
    color = GREEN

    def __init__(self, game):
        x = random.randint(0, game.n_cols - 1)
        y = random.randint(0, game.n_rows - 1)
        super().__init__(x, y, game, self.color)

class Game:
    BLOCK_SIZE = 10

    def __init__(self, n_rows = 40, n_cols = 80, n_foods = 20):
        pygame.init()
        pygame.display.set_caption("DCCP Snake Game")
        self.display = pygame.display.set_mode((n_cols*self.BLOCK_SIZE, n_rows*self.BLOCK_SIZE))
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.n_foods = n_foods

    def multiplay(self):
        head1 = Player(int(self.n_cols/3*2), self.n_rows/2, self, HEAD_1, TAIL_1, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RSHIFT)
        head2 = Player(int(self.n_cols/3), self.n_rows/2, self, HEAD_2, TAIL_2, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_LSHIFT)
        tails1 = []
        tails2 = []
        foods = [Food(self) for i in range (self.n_foods)]

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break
                head1.handle_event(event)
                head2.handle_event(event)
            head1.update()
            head2.update()
            self.display.fill(BLACK)
            head1.draw()
            head2.draw()

            # Tails
            head1.handle_tails(tails1)
            head2.handle_tails(tails2)

            # Foods
            head1.eat(tails1, foods)
            head2.eat(tails2, foods)

            # Out of screen
            if head1.x >= self.n_cols or head1.x < 0 or head1.y < 0 or head1.y >= self.n_rows:
                self.game_over = True
            if head2.x >= self.n_cols or head2.x < 0 or head2.y < 0 or head2.y >= self.n_rows:
                self.game_over = True

            # Death
            for tail in tails1:
                if head1.x == tail.x and head1.y == tail.y:
                    self.game_over = True
            for tail in tails2:
                if head2.x == tail.x and head2.y == tail.y:
                    self.game_over = True
            
            # Kill
            head1.kill(head2, tails2)
            head2.kill(head1, tails1)

            # Update
            pygame.display.update()
            self.clock.tick(10)

if __name__ == "__main__":
    Game().multiplay()