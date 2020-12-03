import pygame
import random

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

REDS = [(255, 0, 0), (255, 200, 200)]
BLUES = [(0, 0, 255), (200, 200, 255)]


class GridObject:
    last_x = 0
    last_y = 0

    def __init__(self, x, y, game, color):
        self.game = game
        self.color = color
        self.x = x  # grid col idx
        self.y = y  # gird row idx

    def draw(self):
        block_size = self.game.BLOCK_SIZE
        pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])


class PlayerBody(GridObject):
    def __init__(self, game, color, facing_grid_object):
        self.facing_grid_object = facing_grid_object
        super().__init__(facing_grid_object.last_x, facing_grid_object.last_y, game, color)

    def move(self):
        self.last_x = self.x
        self.last_y = self.y
        self.x = self.facing_grid_object.last_x
        self.y = self.facing_grid_object.last_y


class PlayerHead(GridObject):
    dx = 0
    dy = 0
    facing = -1
    bodys = []

    def __init__(self, x, y, game, colors, player_idx):
        super().__init__(x, y, game, colors[0])
        self.last_grid_object = self
        self.bodyColor = colors[1]
        self.player_idx = player_idx

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.player_idx == 1:
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
            elif self.player_idx == 2:
                if event.key == pygame.K_a:
                    self.dx = -1
                    self.dy = 0
                elif event.key == pygame.K_d:
                    self.dx = 1
                    self.dy = 0
                elif event.key == pygame.K_w:
                    self.dx = 0
                    self.dy = -1
                elif event.key == pygame.K_s:
                    self.dx = 0
                    self.dy = 1

    def move(self, keys):
        # shift 처리
        multiply_factor = 1
        if keys[pygame.K_RSHIFT] and self.player_idx == 1:
            multiply_factor = 2
        elif keys[pygame.K_LSHIFT] and self.player_idx == 2:
            multiply_factor = 2

        for _ in range(0, multiply_factor):
            self.last_x = self.x
            self.last_y = self.y

            self.x += self.dx
            self.y += self.dy

            for body in self.bodys:
                body.move()

            self.check_eat()

    def add_body(self):
        new_body = PlayerBody(self.game, self.bodyColor, self.last_grid_object)
        self.last_grid_object = new_body
        self.bodys.append(new_body)

    def draw(self):
        super().draw()
        for body in self.bodys:
            body.draw()

    def check_eat(self):
        for food in self.game.foods:
            if self.x == food.x and self.y == food.y:
                food.active = False
                self.game.foods.remove(food)
                self.game.foods.append(Food(self.game))
                self.add_body()


class Food(GridObject):
    color = GREEN
    active = True

    def __init__(self, game):
        x = random.randint(0, game.n_cols)
        y = random.randint(0, game.n_rows)
        super().__init__(x, y, game, self.color)


class Game:
    BLOCK_SIZE = 10
    TICK_PER_SEC = 10
    foods = []

    def __init__(self, n_rows, n_cols):
        pygame.init()
        pygame.display.set_caption("Snake Game")

        self.display = pygame.display.set_mode((n_cols * self.BLOCK_SIZE, n_rows * self.BLOCK_SIZE))
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.clock = pygame.time.Clock()
        self.game_over = False

    def play(self, n_foods = 20):
        player1 = PlayerHead(self.n_cols/2-2, self.n_rows/2, self, REDS, 1)
        player2 = PlayerHead(self.n_cols/2+2, self.n_rows/2, self, BLUES, 2)
        self.foods = [Food(self) for _ in range(n_foods)]
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break
                player1.handle_event(event)
                player2.handle_event(event)

            # BackGround Setting
            self.display.fill(BLACK)

            # player
            keys = pygame.key.get_pressed()
            player1.move(keys)
            player2.move(keys)
            player1.draw()
            player2.draw()

            if player1.x < 0 or player1.x > self.n_cols or player1.y < 0 or player1.y > self.n_rows:
                self.game_over = True
            if player2.x < 0 or player2.x > self.n_cols or player2.y < 0 or player2.y > self.n_rows:
                self.game_over = True

            # food
            for food in self.foods:
                if food.active:
                    food.draw()

            # Game Over - Food
            food_remains = False
            for food in self.foods:
                if food.active:
                    food_remains = True

            if not food_remains:
                self.game_over = True

            # Game Over - Head Cross Body
            for body in player1.bodys:
                if player1.x == body.x and player1.y == body.y:
                    self.game_over = True
                    break
                if player2.x == body.x and player2.y == body.y:
                    self.game_over = True
                    break

            for body in player2.bodys:
                if player1.x == body.x and player1.y == body.y:
                    self.game_over = True
                    break
                if player2.x == body.x and player2.y == body.y:
                    self.game_over = True
                    break

            if player1.x == player2.x and player1.y == player2.y:
                self.game_over = True

            pygame.display.update()
            self.clock.tick(self.TICK_PER_SEC)


if __name__ == "__main__":
    Game(n_rows=60, n_cols=80).play(n_foods=30)
