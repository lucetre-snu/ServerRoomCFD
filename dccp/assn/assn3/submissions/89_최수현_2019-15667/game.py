import pygame
import random

BLACK = (0, 0, 0)
BLUE_HEAD = (227, 246, 245)
BLUE_BODY = (186, 232, 232)
GREEN_HEAD = (233, 250, 221)
GREEN_BODY = (184, 228, 201)
PINK = (255, 175, 155)
BLOCK = 10

pygame.init()

game_display = pygame.display.set_mode((800, 600))
pygame.display.set_caption("DCCP Snake Game")
clock = pygame.time.Clock()

KEY_RIGHT = {
    pygame.K_UP: 'N',
    pygame.K_DOWN: 'S',
    pygame.K_LEFT: 'W',
    pygame.K_RIGHT: 'E',
    pygame.K_RSHIFT: "Shift"
}

KEY_LEFT = {
    pygame.K_w: 'N',
    pygame.K_s: 'S',
    pygame.K_a: 'W',
    pygame.K_d: 'E',
    pygame.K_LSHIFT: "Shift"
}


def draw_block(display, color, position):
    block = pygame.Rect((position[0], position[1]), (BLOCK, BLOCK))
    pygame.draw.rect(display, color, block)


class Player:
    boost = False
    move_block = 20 if boost else BLOCK

    def __init__(self, display, color_head, color_body):
        self.display = display
        self.color_head = color_head
        self.color_body = color_body
        self.positions = [[0, 0]]
        self.after_head = []
        self.direction = ""
        self.dx, self.dy = 0, 0

    def handle_event(self):
        if self.direction == "W":
            self.dx = -self.move_block
            self.dy = 0
        elif self.direction == "E":
            self.dx = self.move_block
            self.dy = 0
        elif self.direction == "N":
            self.dx = 0
            self.dy = -self.move_block
        elif self.direction == "S":
            self.dx = 0
            self.dy = self.move_block

        if self.direction == "Shift":
            self.boost = True

    def tick(self):
        x, y = self.positions[0]
        new_x = x + self.dx
        new_y = y + self.dy
        self.positions = [[new_x, new_y]] + self.positions[:-1]

        if self.boost:
            for position in self.positions:
                position[0] += self.dx
                position[1] += self.dy

    def grow_body_right(self):
        x, y = self.positions[-1]

        if event.key == pygame.K_LEFT:
            self.positions.append([x - BLOCK, y])
        elif event.key == pygame.K_RIGHT:
            self.positions.append([x + BLOCK, y])
        elif event.key == pygame.K_UP:
            self.positions.append([x, y - BLOCK])
        elif event.key == pygame.K_DOWN:
            self.positions.append([x, y + BLOCK])

    def grow_body_left(self):
        x, y = self.positions[-1]

        if event.key == pygame.K_a:
            self.positions.append([x - BLOCK, y])
        elif event.key == pygame.K_d:
            self.positions.append([x + BLOCK, y])
        elif event.key == pygame.K_w:
            self.positions.append([x, y - BLOCK])
        elif event.key == pygame.K_s:
            self.positions.append([x, y + BLOCK])

    def draw(self):
        draw_block(self.display, self.color_head, self.positions[0])
        for position in self.positions[1:]:
            draw_block(self.display, self.color_body, position)


class Food:
    active = True

    def __init__(self, display):
        self.x = random.randint(0, 79) * BLOCK
        self.y = random.randint(0, 59) * BLOCK
        self.display = display

    def draw(self):
        pygame.draw.rect(self.display, PINK, [self.x, self.y, BLOCK, BLOCK])


game_over = False
player1 = Player(game_display, BLUE_HEAD, BLUE_BODY)
player1.positions = [[750, 550]]
player2 = Player(game_display, GREEN_HEAD, GREEN_BODY)
player2.positions = [[50, 50]]
foods = [Food(game_display) for _ in range(20)]

while not game_over:
    head_x1, head_y1 = player1.positions[0]
    head_x2, head_y2 = player2.positions[0]
    if head_x1 < 0 or head_x1 > 800 or head_y1 < 0 or head_y1 > 600:
        game_over = True
    if head_x2 < 0 or head_x2 > 800 or head_y2 < 0 or head_y2 > 600:
        game_over = True

    if len(player1.positions) > 1:
        if player2.positions[0] in player1.positions[1:]:
            game_over = True
        if player1.positions[0] in player1.positions[1:-1]:
            game_over = True

    if len(player2.positions) > 1:
        if player1.positions[0] in player2.positions[1:]:
            game_over = True
        if player2.positions[0] in player2.positions[1:-1]:
            game_over = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            break
        if event.type == pygame.KEYDOWN:
            if event.key in KEY_RIGHT:
                player1.direction = KEY_RIGHT[event.key]
            if event.key in KEY_LEFT:
                player2.direction = KEY_LEFT[event.key]

        player1.handle_event()
        player2.handle_event()

    player1.tick()
    player2.tick()
    game_display.fill(BLACK)
    player1.draw()
    player2.draw()

    for food in foods:
        if food.active:
            food.draw()

        if player1.positions[0] == [food.x, food.y]:
            player1.grow_body_right()
            food.active = False
            foods.append(Food(game_display))

        if player2.positions[0] == [food.x, food.y]:
            player2.grow_body_left()
            food.active = False
            foods.append(Food(game_display))

    pygame.display.update()
    clock.tick(10)
