import pygame as p
import random as r

#Color Pallete
WHITE=(255,255,255)
BLACK=(0,0,0) #BG
RED=(255,0,0) #P-1
RED_PASTEL=(255,150,150) #P-1 Head
GREEN=(0,255,0) # Food
BLUE=(0,0,255) #P-2
BLUE_PASTEL=(150,150,255)

class SnakeGame:

    #0.Setting Variables
    game_over = False
    game_frame = 10
    game_display_unit=10
    game_display_x = game_display_unit*80
    game_display_y = game_display_unit*60

    def __init__(self,title):

        #1.Initial Setting
        p.init()
        self.display = p.display.set_mode((self.game_display_x,self.game_display_y))
        p.display.set_caption(title)
        clock = p.time.Clock()
        self.display.fill(BLACK)

        #1-1.Generate Snakes
        player1=Snake(self.game_display_x/self.game_display_unit/2+10,self.game_display_y/2/self.game_display_unit,RED,RED_PASTEL)
        player2=Snake(self.game_display_x/self.game_display_unit/2-10,self.game_display_y/2/self.game_display_unit,BLUE,BLUE_PASTEL)

        #1-2.Generate Foods
        foods=[]
        for i in range(Food.count):
            foods.append(Food())
        #2.Game Loop
        while not(self.game_over):
            #1)입력 처리
            for event in p.event.get():
                #종료 처리
                if event.type == p.QUIT:
                    self.game_over = True
                    break

                #Player1 움직임 입력
                if event.type == p.KEYDOWN:
                    if event.key == p.K_LEFT:
                        if player1.length == 2 and player1.state == 'RIGHT':
                            self.game_over = True
                            break
                        player1.desinate('LEFT')
                    elif event.key == p.K_RIGHT:
                        if player1.length == 2 and player1.state == 'LEFT':
                            self.game_over = True
                            break
                        player1.desinate('RIGHT')
                    elif event.key == p.K_UP:
                        if player1.length == 2 and player1.state == 'DOWN':
                            self.game_over = True
                            break
                        player1.desinate('UP')
                    elif event.key == p.K_DOWN:
                        if player1.length == 2 and player1.state == 'UP':
                            self.game_over = True
                            break
                        player1.desinate('DOWN')

                #Player1 부스트 입력
                    if event.key == p.K_RSHIFT:
                        player1.boost_speed()
                if event.type == p.KEYUP:
                    if event.key == p.K_RSHIFT:
                        player1.restore_speed()

                    break
                
                #Player2 움직임 입력
                if event.type == p.KEYDOWN:
                    if event.key == p.K_a:
                        if player2.length == 2 and player2.state == 'RIGHT':
                            self.game_over = True
                            break
                        player2.desinate('LEFT')
                    elif event.key == p.K_d:
                        if player2.length == 2 and player2.state == 'LEFT':
                            self.game_over = True
                            break
                        player2.desinate('RIGHT')
                    elif event.key == p.K_w:
                        if player2.length == 2 and player2.state == 'DOWN':
                            self.game_over = True
                            break
                        player2.desinate('UP')
                    elif event.key == p.K_s:
                        if player2.length == 2 and player2.state == 'UP':
                            self.game_over = True
                            break
                        player2.desinate('DOWN')
                #Player2 부스트 입력
                    if event.key == p.K_LSHIFT:
                        player2.boost_speed()
                if event.type == p.KEYUP:
                    if event.key == p.K_LSHIFT:
                        player2.restore_speed()
                if player2.length == 2 and player2.body_cordinate[1] == player2.cordinate:
                    self.game_over = True
                    break

            # 부스트 회수
            for i in [player1,player2]:
                if i.dx == i.speed or i.dy == i.speed:
                    i.boost_activated = False
            #2)게임 상태 업데이트
            #먹기 Event

            for i in [player1,player2]:
                if i.boost_activated == False:
                    if (i.x,i.y) in Food.cordinates:
                        j=Food.cordinates.index((i.x,i.y))
                        foods[j].ate(j,i)
                        foods.remove(foods[j])
                        foods.insert(j,Food())
                        Food.cordinates.remove(Food.cordinates[-1])
                        Food.cordinates.insert(j,(foods[j].x,foods[j].y))
                else:
                    if (i.x,i.y) in Food.cordinates:
                        j=Food.cordinates.index((i.x,i.y))
                        foods[j].ate(j,i)
                        foods.remove(foods[j])
                        foods.insert(j,Food())
                        Food.cordinates.remove(Food.cordinates[-1])
                        Food.cordinates.insert(j,(foods[j].x,foods[j].y))
                    elif (i.x-i.des_x,i.y-i.des_y) in Food.cordinates:
                        j=Food.cordinates.index((i.x-i.des_x,i.y-i.des_y))
                        foods[j].ate(j,i)
                        foods.remove(foods[j])
                        foods.insert(j,Food())
                        Food.cordinates.remove(Food.cordinates[-1])
                        Food.cordinates.insert(j,(foods[j].x,foods[j].y))


            #장외 Event
            for i in [player1,player2]:
                if i.IsOut():
                    self.game_over = True
                    break
            #움직이기 Event
            player1.move()
            player2.move()
            player1.tracking()
            player2.tracking()
            player1.enlong()
            player2.enlong()

            #충돌
            for i in player1.body_cordinate:
                for j in player2.body_cordinate:
                    if i==j:
                        self.game_over = True
                        break
            #자기 충돌
            for i in [player1,player2]:
                if i.selfcrash():
                    self.game_over = True
                    break
                    

            #3)게임 상태 그리기
            self.display.fill(BLACK)
            for i in player1.body:
                i.draw(self)
            for j in player2.body:
                j.draw(self)
            player1.draw(self)
            player2.draw(self)
            for i in range(Food.count):
                foods[i].draw(self)
            p.display.update()
            clock.tick(self.game_frame)

class GridObject:
    def __init__(self,x,y,color=WHITE):
        self.size=SnakeGame.game_display_unit
        self.x = x 
        self.y = y
        self.color = color
        self.cordinate = (self.x , self.y) 
    def draw(self,game):
        p.draw.rect(game.display,self.color,[self.x * self.size,self.y * self.size,self.size,self.size])
class Snake(GridObject):
    def __init__(self,x,y,body_color,color=WHITE):
        GridObject.__init__(self,x,y,color)
        self.body_color=body_color
        self.dx = 0
        self.dy = 0
        self.speed = 1
        self.boosting = 2
        self.length = 1
        self.track=[]
        self.body=[]
        self.boost_activated = False
        self.state='PAUSE'
    def enlong(self):
        self.body.clear()
        self.body_cordinate=[]
        for i in self.track:
            self.body.append(Body(i[0],i[1],self,self.body_color))
            self.body_cordinate.append((i[0],i[1]))
    def boost_speed(self):
        if self.dx != 0:
            self.des_x=self.dx/abs(self.dx)
        else:
            self.des_x=0
        if self.dy != 0:
            self.des_y=self.dy/abs(self.dy)
        else:
            self.des_y=0
        self.boost_activated = True
        self.dx = self.speed * self.boosting * self.des_x
        self.dy = self.speed * self.boosting * self.des_y
    def restore_speed(self):
        if self.dx != 0:
            self.des_x=self.dx/abs(self.dx)
        else:
            self.des_x=0
        if self.dy != 0:
            self.des_y=self.dy/abs(self.dy)
        else:
            self.des_y=0
        self.dx = self.speed * self.des_x
        self.dy = self.speed * self.des_y
        self.boost_activated=False
    def tracking(self):
        if self.boost_activated:
            if self.state == 'LEFT':
                self.track.append((self.x+1,self.y))
            elif self.state == 'RIGHT':
                self.track.append((self.x-1,self.y))
            elif self.state == 'UP':
                self.track.append((self.x,self.y+1))
            elif self.state == 'DOWN':
                self.track.append((self.x,self.y-1))
            for i in self.track:
                if self.track.count(i) == 2:
                    self.track.remove(i)
        self.track.append((self.x,self.y))
        self.track=self.track[len(self.track)-self.length:]
    def desinate(self,key):
        if key == 'DOWN':
            self.dx = 0
            self.dy = self.speed
            self.state='DOWN'
        elif key == 'UP':
            self.dx = 0
            self.dy = -self.speed
            self.state='UP'
        elif key == 'LEFT':
            self.dx = -self.speed
            self.dy = 0
            self.state='LEFT'
        elif key == 'RIGHT':
            self.dx = self.speed
            self.dy = 0
            self.state='RIGHT'
        if self.dx != 0:
            self.des_x=self.dx/abs(self.dx)
        else:
            self.des_x=0
        if self.dy != 0:
            self.des_y=self.dy/abs(self.dy)
        else:
            self.des_y=0
    def move(self):
        self.x += self.dx
        self.y += self.dy
    def IsOut(self):
        if self.x >= SnakeGame.game_display_x/SnakeGame.game_display_unit or self.y >= SnakeGame.game_display_y/SnakeGame.game_display_unit:
            return True
        elif self.x < 0 or self.y < 0:
            return True
        else:
            return False
    def selfcrash(self):

        for i in self.body_cordinate:
            if self.track.count(i) >= 2:
                return True
            else:
                return False
class Body(GridObject):
    def __init__(self,x,y,p:Snake,c):
        self.snake=p
        GridObject.__init__(self,x,y,c)
class Food(GridObject):
    count=20
    cordinates=[]
    def __init__(self):
        GridObject.__init__(self,r.randint(1,SnakeGame.game_display_x/SnakeGame.game_display_unit-1),\
            r.randint(1,SnakeGame.game_display_y/SnakeGame.game_display_unit-1),GREEN)
        while Food.cordinates.count((self.x,self.y)) == 1:
            self.x=r.randint(1,SnakeGame.game_display_x/SnakeGame.game_display_unit-1)
            self.y=r.randint(1,SnakeGame.game_display_y/SnakeGame.game_display_unit-1)
        Food.cordinates.append((self.x,self.y))
    def ate(self,index,player:Snake):
        Food.cordinates.remove((self.x,self.y))
        player.length += 1

#Execute Game
SnakeGame('Snake Game 2020')