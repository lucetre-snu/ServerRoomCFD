import pygame
from random import randrange

# creating pygame windows
pygame.init()
gameScreen = pygame.display.set_mode((800,450))
pygame.display.set_caption("DCCP Snake Game")

# initialize game setting
clock = pygame.time.Clock()
clock.tick(8)
## create movable snake
class Snake():
    def __init__(self, color: list, loc: list, length=1, way = 0, boost = False):
        self.color = color # [headcolor, bodycolor]
        self.loc = loc # All passed locations so far. loc[0] tuple means current head location.
        self.length = length # length of snake
        self.way = way # direction of head. if way==0(initial state): snake doesn't move.
        self.boost = boost
snake1 = Snake([(255,200,200),(255,0,0)], [(100,220)])
snake2 = Snake([(200,200,255),(0,0,255)], [(690,220)])
## create eatable prey
prey = [] # location storage of prey
def preyGen(): # generate the number of prey up to 20.
    while len(prey) < 20:
        x, y = randrange(0,80), randrange(0,45)
        existing = prey + snake1.loc[:snake1.length] + snake2.loc[:snake2.length]
        if (x*10,y*10) not in existing: prey.append((x*10,y*10))
preyGen()

# gameplay methods
## display previous(or initial) state
def draw_body(t: Snake):
    pygame.draw.rect(gameScreen, t.color[0], pygame.Rect(t.loc[0], (10,10)))
    for i in range(1, t.length): pygame.draw.rect(gameScreen, t.color[1], pygame.Rect(t.loc[i], (10,10)))
def draw_prey(prey: list):
    for i in range(len(prey)): pygame.draw.rect(gameScreen, (0,255,0), pygame.Rect(prey[i], (10,10)))

## quit cases
def isOverlap():
    # check if two snakes are overlapped or out of area
    ## this method only works on snake1 and snake2 ##
    global game_over
    overlapped = snake1.loc[1:snake1.length] + snake2.loc[1:snake2.length]
    if snake1.loc[0] in overlapped + [snake2.loc[0]] or snake2.loc[0] in overlapped + [snake1.loc[0]]: game_over = True
    if snake1.loc[0][0] < 0 or snake1.loc[0][0] > 790 or snake1.loc[0][1] < 0 or snake1.loc[0][1] > 440 or snake2.loc[0][0] < 0 or snake2.loc[0][0] > 790 or snake2.loc[0][1] < 0 or snake2.loc[0][1] > 440: game_over = True

## movements
### snake movements
def snake_move(s: Snake):
    newloc = list(s.loc[0])
    if s.way == "UP": newloc[1] -= 10
    elif s.way == "LEFT": newloc[0] -= 10
    elif s.way == "DOWN": newloc[1] += 10
    elif s.way == "RIGHT": newloc[0] += 10
    s.loc.insert(0, tuple(newloc))
### prey updating
def preyUpdate(ss: Snake):
    if ss.loc[0] in prey:
        prey.pop(prey.index(ss.loc[0]))
        ss.length += 1
        preyGen()
### overall movement control
def movement(sss: Snake):
    for _ in range(int(sss.boost) + 1): # True: ×2, False: ×1
        snake_move(sss); isOverlap(); preyUpdate(sss)

## event control
def event_control(events: list):
    for event in events:
        # key > snake movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:         snake1.way = "UP"
            elif event.key == pygame.K_a:       snake1.way = "LEFT"
            elif event.key == pygame.K_s:       snake1.way = "DOWN"
            elif event.key == pygame.K_d:       snake1.way = "RIGHT"
            elif event.key == pygame.K_UP:      snake2.way = "UP"
            elif event.key == pygame.K_LEFT:    snake2.way = "LEFT"
            elif event.key == pygame.K_DOWN:    snake2.way = "DOWN"
            elif event.key == pygame.K_RIGHT:   snake2.way = "RIGHT"
            elif event.key == pygame.K_LSHIFT:  snake1.boost = True
            elif event.key == pygame.K_RSHIFT:  snake2.boost = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:    snake1.boost = False
            elif event.key == pygame.K_RSHIFT:  snake2.boost = False
        elif event.type == pygame.QUIT: game_over = True


# start game
game_over = False
while not game_over:
    # movements
    movement(snake1); movement(snake2)
    # key event control
    event_control(pygame.event.get())
    # display draw
    gameScreen.fill((0,0,0))
    draw_body(snake1); draw_body(snake2)
    draw_prey(prey)
    pygame.display.flip() # practical update code
    # game delay
    pygame.time.delay(125)

# end game
pygame.quit()