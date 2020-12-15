import pygame
from random import randint

class Snake:
	def __init__(self, x, y, bcolor, hcolor):
		self.x = x
		self.y = y
		self.bcolor = bcolor
		self.hcolor = hcolor
		self.dx, self.dy = 0, speed
		self.coords = [[x, y]]
		self.isSurvive = True
		self.isGrowth = False
		self.isBoost = False

	def move(self):
		if not self.isBoost:
			tmpx = self.coords[-1][0]
			tmpy = self.coords[-1][1]

			for i in range(len(self.coords))[::-1]:
				if i == 0:
					self.coords[i][0] += self.dx
					self.coords[i][1] += self.dy
				else:
					self.coords[i][0] = self.coords[i - 1][0]
					self.coords[i][1] = self.coords[i - 1][1]
		else:
			if len(self.coords) >= 2:
				tmpx = self.coords[-2][0]
				tmpy = self.coords[-2][1]
			else:
				tmpx = self.coords[0][0] + self.dx
				tmpy = self.coords[0][1] + self.dy

			for i in range(len(self.coords))[::-1]:
				if i == 0:
					self.coords[i][0] += self.dx * 2
					self.coords[i][1] += self.dy * 2
				elif i == 1:
					self.coords[i][0] = self.coords[0][0] + self.dx
					self.coords[i][1] = self.coords[0][1] + self.dy
				else:
					self.coords[i][0] = self.coords[i - 2][0]
					self.coords[i][1] = self.coords[i - 2][1]
		
		if self.isGrowth:
			self.coords.append([tmpx, tmpy])
			self.isGrowth = False


	def display(self):
		for i in range(len(self.coords)):
			if i == 0:
				pygame.draw.rect(game_display, self.hcolor, [self.coords[i][0], self.coords[i][1], size, size])
			else:
				pygame.draw.rect(game_display, self.bcolor, [self.coords[i][0], self.coords[i][1], size, size])

	def checkCollide(self, other = None):
		if self.coords[0][0] < 0 or self.coords[0][0] >= fieldWidth or self.coords[0][1] < 0 or self.coords[0][1] >= fieldHeight: #check collide to end of the map
			self.isSurvive = False

		for coord in self.coords[1:]:
			if self.coords[0][0] == coord[0] and self.coords[0][1] == coord[1]:
				self.isSurvive = False
				break
		if self.isBoost and len(self.coords) >= 2:
			for coord in self.coords[2:]:
				if self.coords[1][0] == coord[0] and self.coords[1][1] == coord[1]:
					self.isSurvive = False
					break

		if other != None:
			for oCoord in other.coords:
				if self.coords[0][0] == oCoord[0] and self.coords[0][1] == oCoord[1]:
					self.isSurvive = False
					break
			if self.isBoost and len(self.coords) >= 2:
				for oCoord in other.coords:
					if self.coords[1][0] == oCoord[0] and self.coords[1][1] == oCoord[1]:
						self.isSurvive = False
						break

	def checkGrowth(self):
		def regenerateFeed():
			isGenerated = False
			while not isGenerated:
				isAvailable = True
				randx = randint(0, fieldWidth / size) * size
				randy = randint(0, fieldHeight / size) * size

				for coord in feedCoords:
					if coord[0] == randx and coord[1] == randy:
						isAvailable = False
						break

				if isAvailable:
					feedCoords.append([randx, randy])
					isGenerated = True

		delIndexs = []
		for i in range(len(feedCoords)):
			if self.coords[0][0] == feedCoords[i][0] and self.coords[0][1] == feedCoords[i][1] or (self.isBoost and self.coords[0][0] - self.dx == feedCoords[i][0] and self.coords[0][1] - self.dy == feedCoords[i][1]):
				self.isGrowth = True
				delIndexs.append(i)

		for ind in delIndexs: #Delete eaten feeds and regeneration
			del feedCoords[ind]
			regenerateFeed()


def dispFeeds():
	fColor = (0, 255, 0)
	for coord in feedCoords:
		pygame.draw.rect(game_display, fColor, [coord[0], coord[1], size, size])

#===============initialize values==================

pygame.init()

isGameEnd = False
fieldWidth = 800
fieldHeight = 600
background = (0, 0, 0)
size = 10
speed = size

game_display = pygame.display.set_mode((fieldWidth, fieldHeight))
pygame.display.set_caption("snake game")
clock = pygame.time.Clock()

player1 = Snake(600, 300, (80, 80, 255), (150, 150, 255))
player2 = Snake(200, 300, (255, 80, 80), (255, 150, 150))

game_display.fill(background)
player1.display()

#===============initialize feeds==================

feedCoords = []
feedNum = 20
tmp = 0
while tmp < feedNum:
	isAvailable = True
	randx = randint(0, fieldWidth / size - 1) * size
	randy = randint(0, fieldHeight / size - 1) * size

	for coord in feedCoords:
		if coord[0] == randx and coord[1] == randy:
			isAvailable = False
			break

	if isAvailable:
		feedCoords.append([randx, randy])
		tmp += 1

#================main code======================

while not isGameEnd:
	if not player1.isSurvive or not player2.isSurvive:
		isGameEnd = True
		if player1.isSurvive:
			print("Player 1 Win!")
		elif player2.isSurvive:
			print("Player 2 Win!")
		else:
			print("Draw")

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isGameEnd = True
		
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				player1.dx = -speed
				player1.dy = 0
			elif event.key == pygame.K_RIGHT:
				player1.dx = speed
				player1.dy = 0
			elif event.key == pygame.K_UP:
				player1.dx = 0
				player1.dy = -speed
			elif event.key == pygame.K_DOWN:
				player1.dx = 0
				player1.dy = speed
			elif event.key == pygame.K_RSHIFT:
				player1.isBoost = True

			elif event.key == pygame.K_a:
				player2.dx = -speed
				player2.dy = 0
			elif event.key == pygame.K_d:
				player2.dx = speed
				player2.dy = 0
			elif event.key == pygame.K_w:
				player2.dx = 0
				player2.dy = -speed
			elif event.key == pygame.K_s:
				player2.dx = 0
				player2.dy = speed
			elif event.key == pygame.K_LSHIFT:
				player2.isBoost = True


		if event.type == pygame.KEYUP:
			if event.key == pygame.K_RSHIFT:
				player1.isBoost = False
			elif event.key == pygame.K_LSHIFT:
				player2.isBoost = False


	game_display.fill(background)
	dispFeeds()
	player1.checkCollide(player2)
	player2.checkCollide(player1)
	player1.checkGrowth()
	player2.checkGrowth()
	player1.move()
	player2.move()
	player1.display()
	player2.display()

	pygame.display.update()

	clock.tick(10) #fps