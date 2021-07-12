import pygame
import random
pygame.init()

class SnakeGame:
    colorlist={'white':(255,255,255),'black':(0,0,0),'red':(255,0,0),'green':(0,255,0),'blue':(0,0,255), 'yellow':(255,255,0), 'cyan':(0,255,255),'mazenta':(255,0,255),'pink':(255,160,190),'skyblue':(160,190,255)}
    def __init__(self,column,row,block_size,speed):
        self.row=row
        self.column=column
        self.block_size=block_size
        self.game_display=pygame.display.set_mode((block_size*column,block_size*row))
        self.game_over=False
        self.clock=pygame.time.Clock()
        self.speed=speed
    pygame.display.set_caption('Snake Game (2019-14221 문민지)')
    def play(self,num_food):
        Player1=Player(self,self.column-self.column//4,self.row//2,'pink','red')
        Player2=Player(self,self.column//4,self.row//2,'skyblue','blue')
        Player2.key_up=pygame.K_w
        Player2.key_down=pygame.K_s
        Player2.key_left=pygame.K_a
        Player2.key_right=pygame.K_d
        Player2.key_boost=pygame.K_LSHIFT
        Foods=[]
        for _ in range(num_food):
            Foods.append(Food(self,'green',Player1.body+Player2.body+[(food.x,food.y) for food in Foods]))

        while not self.game_over:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.game_over=True
                    break
                Player1.action(event)
                Player2.action(event)
            Player1.Boost()
            Player2.Boost()

            #move snakes' heads
            Player1.head()
            Player2.head()

            #lengthen the body of snakes if they eat
            for player in [Player1,Player2]:
                for food in Foods:
                    if food.x==player.x and food.y==player.y:
                        player.eat+=1
                        food.state=False
                    if player.boost:
                        if food.x==player.x-player.dx and food.y==player.y-player.dy:
                            player.eat+=1
                            food.state=False
                
            Player1.body_modify()
            Player2.body_modify() 

            #maintain the number of foods
            newFoods=[]
            for food in Foods:
                if food.state:
                    newFoods.append(food)  
                else:
                    newFoods.append(Food(self,'green',Player1.body+Player2.body+[(food.x,food.y) for food in Foods]))       
            Foods=newFoods

            #game over condition
            if not(0<=Player1.x<=self.column-1 and 0<=Player2.x<=self.column-1 and 0<=Player1.y<=self.row-1 and 0<=Player2.y<=self.row-1):
                self.game_over=True
            
            for player1 in [Player1,Player2]:
                for player2 in [Player1,Player2]:
                    if any(player2.body[-1]==part for part in player1.body[:len(player1.body)-1]):
                        self.game_over=True
                        break
                    if player1!=player2 and player2.boost and any(player2.pastbody[-2]==part for part in player1.body):
                        self.game_over=True
                        break 
                if self.game_over:
                    break
 
            if Player1.x==Player2.x and Player1.y==Player2.y:
                self.game_over=True

            for i in [Player1,Player2]:
                if len(i.body)==2:
                    if i.boost and i.pastbody[0]==i.body[0]:
                        self.game_over=True
                        break
                    elif not i.boost and i.pastbody[0]==i.body[1]:
                        self.game_over=True
                        break
            
           
            self.game_display.fill(self.colorlist['black'])

            obj=[Player1,Player2,*Foods]
            for i in obj:
                i.draw()
            Player1.score(1)
            Player2.score(2)

            Player1.eat=0
            Player2.eat=0
                      
            pygame.display.update()
            self.clock.tick(self.speed)


    
class GameObjects:
    def __init__(self,game,x,y,color1,color2='black'):
        self.game=game
        self.x=x
        self.y=y   
        self.game_display=game.game_display
        self.block_size=game.block_size
        self.color1=game.colorlist[color1]
        self.color2=game.colorlist[color2]
        self.body=[(x,y)]
        self.state=True

    def draw(self):
        for i in range(len(self.body)):
            if i==len(self.body)-1:
                pygame.draw.rect(self.game_display,self.color1,[self.x*self.block_size,self.y*self.block_size,self.block_size,self.block_size])
            else:
                pygame.draw.rect(self.game_display,self.color2,[self.body[i][0]*self.block_size,self.body[i][1]*self.block_size,self.block_size,self.block_size])
       
class Player(GameObjects):
    def __init__(self,game,x,y,color1,color2):
        super().__init__(game,x,y,color1,color2)
        self.dx=0
        self.dy=0
        self.key_up=pygame.K_UP
        self.key_down=pygame.K_DOWN
        self.key_left=pygame.K_LEFT
        self.key_right=pygame.K_RIGHT
        self.key_boost=pygame.K_RSHIFT
        self.eat=0
        self.boost=False

    def action(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key==self.key_down:
                self.dx=0
                self.dy=1
            elif event.key==self.key_up:
                self.dx=0
                self.dy=-1
            elif event.key==self.key_left:
                self.dx=-1
                self.dy=0
            elif event.key==self.key_right:
                self.dx=1
                self.dy=0

    def Boost(self):
        key=pygame.key.get_pressed()
        if key[self.key_boost]:
            self.boost=True
        else:
            self.boost=False
               
    def head(self):
        if self.boost:
            self.x+=self.dx*2
            self.y+=self.dy*2
        else:           
            self.x+=self.dx
            self.y+=self.dy

    def body_modify(self):    
        if self.boost:
            self.body.append((self.x-self.dx,self.y-self.dy))
            self.body.append((self.x,self.y))
            self.pastbody=self.body[:]
            if self.eat==0:
                self.body=self.body[2:]
            elif self.eat==1:
                self.body=self.body[1:]
            
        else:    
            self.body.append((self.x,self.y))
            self.pastbody=self.body[:]
            if not self.eat:
                self.body=self.body[1:]
        
    def score(self,order):
        score='Player%d: %d' % (order,len(self.body)-1)
        font=pygame.font.Font(None, 20)
        text=font.render(score, True, self.color1)
        text_pos=text.get_rect()
        text_pos.center=(self.game.column*self.block_size-45,20*order-5)
        self.game_display.blit(text,text_pos) 

class Food(GameObjects):
    def __init__(self,game,color,points):
        while True:
            x=random.randint(0,game.column-1)
            if all(x!=other for other in list(zip(points))[0]):
                self.x=x
                break
        while True:
            y=random.randint(0,game.row-1)
            if all(y!=other for other in list(zip(points))[1]):
                self.y=y
                break
        super().__init__(game,self.x,self.y,color)


if __name__ == "__main__":
    SnakeGame(80,60,10,10).play(20)

