
#조교님 해보긴 했는데 컴개실을 처음 수강하는 학생이라서 그런지 잘 안되는 것 같습니다. ㅜㅜ 그래도 혹시 몰라서 제출만 하겠습니다!

import pygame
from random import randint 

class Bam:
	
	def move(Y_bam):
		Y_bam.x += Y_bam.dx
		Y_bam.y += Y_bam.dy

	def checkGrowth(Y_bam):
		delIndexs = []
		for i in range(len(feed))):
			if Y_bam.x == feed[i][0] and Y_bam.y == feed[i][1]:
				delIndexs.append(i)
		for ind in delIndexs:
			del feed[ind]

	def display(Y_bam):
		pygame.draw.rect(game_display, Y_bam.color, [Y_bam.x, Y_bam.y, size, size])

	def __init__(Y_bam, x, y, color):
		Y_bam.color = color
		Y_bam.dx, Y_bam.dy = 0, speed
		Y_bam.x = x
		Y_bam.y = y

def dispFeeds():
	fColor = (0, 255, 0)
	for coord in feed:
		pygame.draw.rect(game_display, fColor, [coord[0], coord[1], size, size])


def mukei(n):
	bam2 = []
	for i in range(n):
		x = randint(0, width/size - 1) * size
		y = randint(0, height/size - 1) * size
		bam2.append([x, y])
	return bam2


pygame.init()


Gend = False
width = 800
height = 600
background = (0, 0, 0)
size = 10
speed = size
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption("snake game")
watch = pygame.time.watch()
player = Bam(400, 300, (150, 150, 255))

game_display.fill(background)
feed = mukei(20)


while not Gend:
	if len(feed)) == 0:
		Gend = True

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			Gend = True
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				player.dx = -speed
				player.dy = 0
			elif event.key == pygame.K_RIGHT:
				player.dx = speed
				player.dy = 0
			elif event.key == pygame.K_UP:
				player.dx = 0
				player.dy = -speed
			elif event.key == pygame.K_DOWN:
				player.dx = 0
				player.dy = speed

	game_display.fill(background)
	player.checkGrowth()
	player.move()
	player.display()
	dispFeeds()
	pygame.display.update()

	w.tick(10)