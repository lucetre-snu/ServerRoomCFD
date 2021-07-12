import pygame
import random

pygame.init()

game_display = pygame.display.set_mode((800,600))
pygame.display.set_caption('DCCP Snake Game')
clock = pygame.time.Clock()



#game_display.fill((255,255,255))
#pygame.draw.rect(game_display, (0,0,0), [400,300,20,10])    #x, y, w h

pygame.display.update()                 #화면 흰색으로 바꾸기+알파
#위는 디스플레이에 어떤 이벤트가 일어날때마다 실행.

class Player:
    dx=0
    dy=0
    point=1
    
    internal_clock=10
    boost=False

    def __init__(self,display,x,y,color,bodycolor,typeofp):
        self.display = display
        self.x=x
        self.y=y
        self.color=color
        self.bodycolor=bodycolor
        self.typeofp=typeofp

    def handle_event1(self,event):
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.dx = -10
                self.dy=0

            elif event.key == pygame.K_RIGHT:
                self.dx = 10
                self.dy=0

            elif event.key == pygame.K_UP:
                self.dy = -10
                self.dx=0
            
            elif event.key == pygame.K_DOWN:
                self.dy = 10    
                self.dx=0


    def handle_event2(self,event):
        if event.type==pygame.KEYDOWN:
            if event.key == 97:
                self.dx = -10
                self.dy=0

            elif event.key == 100:
                self.dx = 10
                self.dy=0

            elif event.key == 119:
                self.dy = -10
                self.dx=0
            
            elif event.key == 115:
                self.dy = 10    
                self.dx=0


    def Rshift(self,event):
        
        if event.type==pygame.KEYDOWN and event.key==1073742053:        #매번 연산을 하지만, 특정 이벤트에서만 변화가 일어난다. 그리고 return function을 쓰면 함숫값이 none으로 출력되는 문제가 있으므로 이렇게 한다. 
            self.boost=True

        if event.type==pygame.KEYUP and event.key==1073742053:
            self.boost=False


    def Lshift(self,event):
        
        if event.type==pygame.KEYDOWN and event.key==1073742049:        #매번 연산을 하지만, 특정 이벤트에서만 변화가 일어난다. 그리고 return function을 쓰면 함숫값이 none으로 출력되는 문제가 있으므로 이렇게 한다. 
            self.boost=True

        if event.type==pygame.KEYUP and event.key==1073742049:
            self.boost=False        


    def handle_tick(self):
        self.x += self.dx
        self.y += self.dy


    def draw(self):
        pygame.draw.rect(self.display, self.color, [self.x, self.y,10,10])    
    
    
    pass


class Food:
    active = True
    def __init__(self,display):
        self.x = random.randint(0,79) * 10
        self.y = random.randint(0,59) * 10
        self.display=display
    
    def draw(self):
        pygame.draw.rect(self.display, 'green', [food.x, food.y, 10, 10])
    pass

class Body:
    
    def __init__(self, display,x,y,color):     #player의 이전 행동을 copy하는 것. body.player_copy.dx같은걸 모두 사용가능.      
        self.display=display
        self.x=x
        self.y=y
        self.color=color

    def draw(self):
        pygame.draw.rect(self.display, self.color, [self.x, self.y, 10, 10])
    
    pass
    
    pass
game_over = False


player1 = Player(game_display,600,300,'white','blue',1)
player2 = Player(game_display,200,300,'red','yellow',2)
foods=[Food(game_display) for _ in range(20)]
bodys1=[]           #head의 자리를 포함하고 있는 것. 일관성을 위해서 필요.
bodys2=[]

while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            break                       # X누르면 나가지기.'
        
        player1.Rshift(event)
        player1.handle_event1(event)
        
        player2.Lshift(event)
        player2.handle_event2(event)    
            
            
    for player in (player1,player2):
        if player.x<0 or player.x>790 or player.y<0 or player.y>590:
            game_over=True
        
        
        player.handle_tick()

            
        #x 갱신하기. 갱신 전에 draw self가 나와야될 것 같아.   
    n1=player1.point
    n2=player2.point

    bodys1.append(Body(game_display,  player1.x,  player1.y,  player1.bodycolor))
    if len(bodys1)>(player1.point+2):
        bodys1=bodys1[-n1-3:]
    
    bodys2.append(Body(game_display,  player2.x,  player2.y,  player2.bodycolor))
    if len(bodys2)>(player2.point+2):
        bodys2=bodys2[-n2-3:]
        

        
    game_display.fill('black')


    for food in foods:
        if food.active:
            food.draw()
        for player in (player1,player2):

            if player.x==food.x and player.y==food.y:
                player.point +=1
            

                foods.remove(food)
                new_food=Food(game_display)
                foods.append(new_food)

        
    for body in bodys1[-n1:-1]:
        body.draw()

        
    for body in bodys2[-n2:-1]:
        body.draw()

    for body in bodys1[-n1:-1]+bodys2[-n2:-1]:
        for player in (player1, player2):
            if player.x==body.x and player.y==body.y:
                game_over=True
                break
        

             


    player1.draw()
    player2.draw()

    pygame.display.update()
    if player1.x==player2.x and player1.y==player2.y:
        game_over=True 
        break 
    if len(bodys1)>1 and len(bodys2)>1:
        if player2.x==bodys1[-2].x and player2.y==bodys1[-2].y and player1.x==bodys2[-2].x and player1.y==bodys2[-1].y:
            game_over=True
            break
        
            
        
    if player1.boost:
        for event in pygame.event.get():                # X누르면 나가지기.'
            player1.handle_event1(event)
        
        player1.handle_tick()
        
        bodys1.append(Body(game_display,player1.x,player1.y,player1.bodycolor))

    #최적화 필요, 최신인 애들만 남기고 뒤에꺼는 자르기. 무난하게 데이터를 유지하려면 point가 2점이면 head와 1초전 head를 보유하고 있어야 하므로, 무난하게 n+2개정도 남기기로 하자.
        if len(bodys1)>(player1.point+2):
            bodys1=bodys1[-n1-3:]


        

        game_display.fill('black')

        #for body in bodys:
        #    body.draw()

        for food in foods:
            if food.active:
                food.draw()

            if player1.x==food.x and player1.y==food.y:
                player1.point +=1
                

                foods.remove(food)
                new_food=Food(game_display)
                foods.append(new_food)

        n=player1.point
        for body in bodys1[-n1:-1]:
            body.draw()
                

        for body in bodys1[-n1:-1]+bodys2[-n2:-1]:
            for player in (player1, player2):
                if player.x==body.x and player.y==body.y:
                    game_over=True
                    break 

        if player1.x==player2.x and player1.y==player2.y:
            game_over=True    
            break    

    if player2.boost:
        for event in pygame.event.get():                # X누르면 나가지기.'
            player2.handle_event2(event)
        
        player2.handle_tick()
        
        bodys2.append(Body(game_display,player2.x,player2.y,player2.bodycolor))

    #최적화 필요, 최신인 애들만 남기고 뒤에꺼는 자르기. 무난하게 데이터를 유지하려면 point가 2점이면 head와 1초전 head를 보유하고 있어야 하므로, 무난하게 n+2개정도 남기기로 하자.
        if len(bodys2)>(player2.point+2):
            bodys2=bodys2[-n2-3:]


        

        game_display.fill('black')

        #for body in bodys:
        #    body.draw()

        for food in foods:
            if food.active:
                food.draw()

            if player2.x==food.x and player2.y==food.y:
                player2.point +=1
                

                foods.remove(food)
                new_food=Food(game_display)
                foods.append(new_food)

        
        for body in bodys2[-n2:-1]:
            body.draw()
                

        for body in bodys1[-n1:-1]+bodys2[-n2:-1]:
            for player in (player1, player2):
                if player.x==body.x and player.y==body.y:
                    game_over=True
                    break 

        if player1.x==player2.x and player1.y==player2.y:
            game_over=True
            break

    clock.tick(player1.internal_clock)  #fps임.