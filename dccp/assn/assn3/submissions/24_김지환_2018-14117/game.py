import pygame, random

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
MAGENTA=(255,0,255)
YELLOW=(255,255,0)
CYAN=(0,255,255)

pygame.init()
game_display=pygame.display.set_mode([800,600])
pygame.display.set_caption("Snake game by KimJihwan")

game_over=False

class Player:
    def __init__(self, x, y, hcolor, tcolor):
        self.x=x
        self.y=y
        self.hcolor=hcolor
        self.tcolor=tcolor
        self.dx=0
        self.dy=0
        self.legacy=[]
class Food:
    def __init__(self):
        self.x=random.randint(0,79)*10
        self.y=random.randint(0,59)*10
foods=[]
for i in range(20):
    foods.append(Food())

game_display.fill((255,255,255))
pygame.display.update()
clock = pygame.time.Clock()

p1=Player(50,200,CYAN,BLUE)
p2=Player(650,200,MAGENTA,RED)

while not game_over:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_over=True
            break
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                p1.dx=-10
                p1.dy=0
            elif event.key==pygame.K_RIGHT:
                p1.dx=10
                p1.dy=0
            elif event.key==pygame.K_UP:
                p1.dx=0
                p1.dy=-10
            elif event.key==pygame.K_DOWN:
                p1.dx=0
                p1.dy=10
            elif event.key==pygame.K_RSHIFT:
                p1.dx*=2
                p1.dy*=2
            elif event.key==pygame.K_a:
                p2.dx=-10
                p2.dy=0
            elif event.key==pygame.K_d:
                p2.dx=10
                p2.dy=0
            elif event.key==pygame.K_w:
                p2.dx=0
                p2.dy=-10
            elif event.key==pygame.K_s:
                p2.dx=0
                p2.dy=10
            elif event.key==pygame.K_LSHIFT:
                p2.dx*=2
                p2.dy*=2
        elif event.type==pygame.KEYUP:
            if event.key==pygame.K_RSHIFT:
                p1.dx/=2
                p1.dy/=2
            elif event.key==pygame.K_LSHIFT:
                p2.dx/=2
                p2.dy/=2
    p1.legacy.append([p1.x, p1.y])
    p2.legacy.append([p2.x, p2.y])
    p1.x+=p1.dx
    p1.y+=p1.dy
    p2.x+=p2.dx
    p2.y+=p2.dy
    for p in (p1, p2):   
        ate=False
        for f in foods:
            if p.x==f.x and p.y==f.y:
                foods.remove(f)
                foods.append(Food())
                ate=True
        if ate==False:
            p.legacy.remove(p.legacy[0])

    game_display.fill(BLACK)
    for f in foods:
        pygame.draw.rect(game_display, GREEN, [f.x,f.y,10,10])
    for p in p1,p2:
        for x,y in p.legacy:
            pygame.draw.rect(game_display, p.tcolor, [x,y,10,10])
        pygame.draw.rect(game_display, p.hcolor, [p.x,p.y,10,10])
    
    for p in p1,p2:
        if p.x<0 or p.y<0 or p.x>800 or p.y>600:
            game_over=True
        for x,y in p1.legacy:
            if x==p.x and y==p.y:
                game_over=True
        for x,y in p2.legacy:
            if x==p.x and y==p.y:
                game_over=True

    pygame.display.update()
    clock.tick(10)