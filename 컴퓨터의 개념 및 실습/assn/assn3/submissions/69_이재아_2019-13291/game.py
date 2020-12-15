import pygame
import random

# initialize tuples of the color
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
L_BLUE = (102, 102, 255)  # color of light blue
PINK = (255, 51, 255)
L_PINK = (255, 153, 255)  # color of light pink

# define the keys of the first player
R_KEYS = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
R_BOOST = pygame.KMOD_RSHIFT

# define the keys of the second player
L_KEYS = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]
L_BOOST = pygame.KMOD_LSHIFT

# define the key to exit the game
QUIT = pygame.QUIT

# define the velocity of the snake
# total velocity in the screen is MOVE * FPS (tiles/s)
MOVE = 10
FPS = 20

# define the size of the tile and the screen
TILE = 10
WIDTH = 80  # the width of the screen
HEIGHT = 60  # the height of the screen


# declare the class to set the items in the game
class Items:
    def __init__(self, display, color):
        self.display = display
        self.x = 0
        self.y = 0
        self.color = color
        self.active = True

    def draw(self):
        pygame.draw.rect(self.display, self.color, [self.x, self.y, 10, 10])

    def handle_boost(self, frame):
        return True

    def handle_event(self, event):
        pass

    def tick(self):
        pass

    def interact(self, other):
        pass

    def crash(self, other):
        pass


# define the item of the player
class Player(Items):
    def __init__(self, display, color, bodycolor, keys, boost):
        super().__init__(display, color)
        self.x = 0
        self.dx = 0
        self.y = 0
        self.dy = 0
        self.body = []
        self.body_color = bodycolor
        self.keys = keys
        self.boost = boost
        self.previous = None

    # function to set the starting point
    def start(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        super().draw()  # draw the head
        if self.body:
            for e in self.body:  # draw the body
                pygame.draw.rect(self.display, self.body_color, [e[0], e[1], 10, 10])

    # function to define if the key entered is valid
    def valid_key(self, event):
        keylist1 = self.keys[:2]
        keylist2 = self.keys[2:]
        if self.previous:
            for lst in [keylist1, keylist2]:
                if (self.previous.key in lst) and (event.key in lst):
                    return False
        return True

    # function to handle the boost(SHIFT key)
    def handle_boost(self, frame):
        if pygame.key.get_mods() & self.boost:
            return True
        else:
            if frame % 2 == 0:
                return True  # the speed decreases by half while the boost is not working
        return False

    def handle_event(self, event):
        keys = self.keys
        move = MOVE
        if event.key == keys[0]:
            self.dx = -move
            self.dy = 0
        elif event.key == keys[1]:
            self.dx = move
            self.dy = 0
        elif event.key == keys[2]:
            self.dx = 0
            self.dy = -move
        elif event.key == keys[3]:
            self.dx = 0
            self.dy = move

    # function to handle for moving the player
    def move(self, event):
        if self.valid_key(event):
            self.handle_event(event)
            self.previous = event

    def tick(self):
        if self.body:
            self.body = [(self.x, self.y)] + self.body[:-1]  # move the body
        self.x += self.dx
        self.y += self.dy  # move the head

    def interact(self, other):
        if isinstance(other, Food):
            if not self.body:  # if the player is not grown
                if self.x == other.x and self.y == other.y:
                    other.active = False
            else:  # if the length of the player is more than one tile
                x_range = sorted([self.x, self.body[0][0]])
                y_range = sorted([self.y, self.body[0][1]])
                if (x_range[0] <= other.x <= x_range[1]) and (y_range[0] <= other.y <= y_range[1]):
                    other.active = False

    # function to determine if players have crashed
    def crash(self, other):
        if isinstance(other, Player):
            p1_all = [(self.x, self.y)] + self.body
            p2_all = [(other.x, other.y)] + other.body
            for i in p1_all:
                for j in p2_all:
                    if i == j:
                        return True
        return False

    # function to decide whether the player is on the screen or not
    def in_screen(self, s_row, s_col):
        if 0 <= self.x <= s_row and 0 <= self.y <= s_col:
            return True
        return False

    # function to determine if the body and the head overlap
    def overlapped(self):
        if (self.x, self.y) in self.body:
            return False
        return True

    # function to grow the body
    def grow(self):
        if self.body:
            last = self.body[-1]
        else:
            last = [self.x, self.y]
        self.body.append((last[0] - self.dx, last[1] - self.dy))


# define the class of the food
class Food(Items):
    def __init__(self, display, color):
        super().__init__(display, color)
        self.x = random.randint(0, WIDTH - 1) * 10
        self.y = random.randint(0, HEIGHT - 1) * 10

    # check if the food is overlapped with other items
    def is_valid(self, locations):
        if (self.x, self.y) in locations:
            return False
        return True


pygame.init()
pygame.display.set_caption("DCCP Snake Game")
clock = pygame.time.Clock()


class Game:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.display = pygame.display.set_mode((self.row * TILE, self.col * TILE))

    def play(self, foods):
        screen = self.display

        game_over = False  # define the variable to decide if the game is over
        loop = 0  # define the variable to count the number of the while-loop below rotations
        # this value is equal to the number of frames executed

        objects = []  # list of all of objects in the game
        player1 = Player(screen, L_PINK, PINK, R_KEYS, R_BOOST)  # create the first player
        player1.start(self.row * 7.5, self.col * 5)
        player2 = Player(screen, L_BLUE, BLUE, L_KEYS, L_BOOST)  # create the second player
        player2.start(self.row * 2.5, self.col * 5)
        players = [player1, player2]  # declare the list of the players
        for p in players:
            objects.append(p)
        for _ in range(foods):
            objects.append(Food(screen, GREEN))

        while not game_over:
            screen.fill(BLACK)
            loop += 1  # count the number of loop rotations

            for event in pygame.event.get():
                if event.type == QUIT:
                    game_over = True  # the game ends
                elif event.type == pygame.KEYDOWN:
                    for p in players:
                        if event.key in p.keys:
                            p.move(event)

            for p in players:
                if p.handle_boost(loop):  # check if the boost is working
                    p.tick()

            for e in objects:
                if e.active:
                    e.draw()  # draw all objects

            locations = []  # define the list to store the location of all items
            for e in objects:
                if isinstance(e, Player):
                    locations.append((e.x, e.y))
                    if e.body:
                        locations.extend(e.body)  # save the location of players
                if isinstance(e, Food):
                    locations.append((e.x, e.y))  # save the location of foods

            for i in objects:
                for j in objects:
                    i.interact(j)
                    if not j.active:
                        objects.remove(j)  # food is eaten
                        while True:
                            newFood = Food(screen, GREEN)  # create new food
                            if newFood.is_valid(locations):  # check if the location of new food is valid
                                objects.append(newFood)  # add new food
                                break
                        i.grow()  # the body of the player grows

            pygame.display.update()
            clock.tick(FPS)

            # the game is over when the collision between players is occurred.
            if player1.crash(player2):
                game_over = True

            # the game is over when the player is out of the screen or the body is overlapped
            for p in players:
                if not (p.in_screen(self.row * TILE, self.col * TILE) and p.overlapped()):
                    p.active = False
            for p in players:
                if not p.active:
                    game_over = True


if __name__ == "__main__":
    Game(row=WIDTH, col=HEIGHT).play(foods=20)

pygame.quit()
