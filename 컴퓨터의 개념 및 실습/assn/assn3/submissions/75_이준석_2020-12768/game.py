import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (205, 12, 34)
PINK = (219, 68, 85)
GREEN = (0, 255, 0)
BLUE = (22, 141, 210)
SKYBLUE = (91, 175, 225)


pygame.init()

game_display = pygame.display.set_mode((800, 600))
pygame.display.set_caption('DCCP Snake Game')
clock = pygame.time.Clock()


class Player:
	dx = 0; dy = 0
	length = 1

	def __init__(self, display, pid, x, y, colors):
		self.display = display
		self.pid = pid
		self.x = x; self.y = y
		self.body = [(x, y)]
		self.color1, self.color2 = colors

	def handle_event(self, event):
		if event.type == pygame.KEYDOWN:
			if (self.pid == 2 and event.key == pygame.K_LEFT) or (self.pid == 1 and event.key == pygame.K_a):
				if self.length > 1 and self.dx == 10:
					return 'wrongDirection'
				else:
					self.dx = -10; self.dy = 0
			elif (self.pid == 2 and event.key == pygame.K_RIGHT) or (self.pid == 1 and event.key == pygame.K_d):
				if self.length > 1 and self.dx == -10:
					return 'wrongDirection'
				else:
					self.dx = 10; self.dy = 0
			elif (self.pid == 2 and event.key == pygame.K_UP) or (self.pid == 1 and event.key == pygame.K_w):
				if self.length > 1 and self.dy == 10:
					return 'wrongDirection'
				else:
					self.dx = 0; self.dy = -10
			elif (self.pid == 2 and event.key == pygame.K_DOWN) or (self.pid == 1 and event.key == pygame.K_s):
				if self.length > 1 and self.dy == -10:
					return 'wrongDirection'
				else:
					self.dx = 0; self.dy = 10

	def tick(self, other, boost):
		head = self.body[0]
		next_head = (head[0]+self.dx*(boost+1), head[1]+self.dy*(boost+1))
		self.x, self.y = next_head

		rtn = 0
		if (self.dx != 0 or self.dy != 0) and (next_head in self.body):
			rtn = 'overlapped'
		elif next_head in other.body:
			rtn = 'overlapped'

		self.body.insert(0, next_head)

		if self.length > 1 and boost == 1:
			self.body.insert(1, (self.x-self.dx, self.y-self.dy))

		while len(self.body) > self.length:
			self.body.pop()

		self.draw()
		return rtn

	def draw(self):
		for i, (x, y) in enumerate(self.body):
			if i == 0:
				pygame.draw.rect(self.display, self.color1, [x, y, 10, 10])
			else:
				pygame.draw.rect(self.display, self.color2, [x, y, 10, 10])


class Food:
	def __init__(self, display):
		self.display = display
		self.generate()

	def generate(self):
		self.x = random.randint(0, 79)*10
		self.y = random.randint(0, 59)*10

		pos = (self.x, self.y)
		if pos in player1.body or pos in player2.body:
			self.generate()

	def draw(self):
		pygame.draw.rect(self.display, GREEN, [self.x, self.y, 10, 10])

player1 = Player(game_display, 1, 200, 300, (RED, PINK))
player2 = Player(game_display, 2, 600, 300, (BLUE, SKYBLUE))
foods = [Food(game_display) for i in range(20)]


game_over = False

def game(player, other, boost):
	if player.tick(other, boost) == 'overlapped':
		global game_over; game_over = True

	if player.x < 0 or player.x > 790 or player.y < 0 or player.y > 590:
		game_over =True

	for food in foods:
		if (player.x == food.x and player.y == food.y) or \
			(player.length > 1 and (player.x-player.dx) == food.x and (player.y-player.dy) == food.y):
			player.length += 1
			food.generate()

		food.draw()

while not game_over:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game_over = True
			break
		player1.handle_event(event); player2.handle_event(event)

	boost_1 = 0; boost_2 = 0
	keys = pygame.key.get_pressed()
	if keys[pygame.K_LSHIFT]:
		boost_1 = 1
		if keys[pygame.K_RSHIFT]:
			boost_2 = 1
	elif keys[pygame.K_RSHIFT]:
		boost_2 = 1

	
	game_display.fill(BLACK)
	game(player1, player2, boost_1)
	game(player2, player1, boost_2)
	pygame.display.update()

	clock.tick(10)

