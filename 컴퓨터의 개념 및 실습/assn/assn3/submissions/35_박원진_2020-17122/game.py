import random
import pygame

WHITE=(255, 255, 255)
BLACK=(0, 0, 0)
RED=(255, 0 ,0)
GREEN=(0, 255, 0)
BLUE=(0, 0, 255)
Yellow=(255, 255, 0)

space_width=800
space_height=600
body_len1=1
body_len2=1

game_display=pygame.display.set_mode((space_width, space_height))
pygame.display.set_caption('Snake Game')
clock=pygame.time.Clock()

class Control_key():
    def __init__(self, up, down, left, right, boost):
        self.up=up
        self.down=down
        self.left=left
        self.right=right
        self.boost=boost

class Player():
    dx=0
    dy=0
    box_len=10
    def __init__(self, display, position, color, control):
        self.display=display
        self.position_list=[]
        self.test_dx=0
        self.test_dy=0
        self.x=position[0]
        self.y=position[1]
        self.color=color
        self.control=control
    def choose_boost(self, event):
        if event.type==pygame.KEYDOWN:
            if event.key==self.control.boost:
                return True
        elif event.type==pygame.KEYUP and event.key==self.control.boost:
            return False
    def handle_event(self, event):
        if event.type==pygame.KEYDOWN:
            if event.key==self.control.left:
                self.dx=-self.box_len
                self.dy=0
                if self.test_dx>0:
                    return True
            elif event.key==self.control.right:
                self.dx=+self.box_len
                self.dy=0
                if self.test_dx<0:
                    return True
            elif event.key==self.control.up:
                self.dy=-self.box_len
                self.dx=0
                if self.test_dy>0:
                    return True
            elif event.key==self.control.down:
                self.dy=+self.box_len
                self.dx=0
                if self.test_dy<0:
                    return True
    def tick(self):
        self.x+=self.dx
        self.y+=self.dy
    def draw(self):
        pygame.draw.rect(self.display, self.color, [self.x, self.y, self.box_len, self.box_len])
    def save_position(self, n):
        self.position_list.append((self.x, self.y))
        del self.position_list[:-n]
    def save_test(self, event):
        if event.type==pygame.KEYDOWN:
            self.test_dx=self.dx
            self.test_dy=self.dy

class Snake_Body():
    box_len=10
    def __init__(self, display, color):
        self.display=display
        self.x=0
        self.y=0
        self.color=color
    def draw(self):
        pygame.draw.rect(self.display, self.color, [self.x, self.y, self.box_len, self.box_len])

class Food:
    active=True
    def __init__(self, display):
        self.x=self.x=random.randint(0, 79)*10
        self.y=self.y=random.randint(0, 59)*10
        self.display=display
        self.box_len=10
    def draw(self):
        pygame.draw.rect(self.display, GREEN, [self.x, self.y, self.box_len, self.box_len])
    def check_meet(self,x,y):
        if self.x==x and self.y==y:
            return True
        else:
            return False
    def food_replace(self):
        self.x=random.randint(0, 79)*10
        self.y=random.randint(0, 59)*10
    def check_food(self, x, y):
        if self.x==x and self.y==y:
            return True
        else:
            return False

game_over=False

arrow=Control_key(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RSHIFT)
wasd=Control_key(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LSHIFT)

player1=Player(game_display,(600,300),WHITE,arrow)
player2=Player(game_display,(200,300),BLUE,wasd)

foods=[Food(game_display) for _ in range(20)]
for i in foods:
    check=True
    while check:
        a=i.check_food(player1.x, player1.y)
        b=i.check_food(player2.x, player2.y)
        if a==False and b==False:
            check=False
        else:
            i.food_replace()
       
while not game_over:
    a=False
    b=False
    for event in pygame.event.get():
        if event.type==pygame.QUIT:   
            game_over=True
            break
        #방향을 정반대로 바꿀 때 게임 오버(몸통과 만남)
        opposite1=player1.handle_event(event)
        if body_len1>1:
            if opposite1:
                game_over=True
                a=True
                break
        player1.save_test(event)
        check_tick1=player1.choose_boost(event)

        opposite2=player2.handle_event(event)
        if body_len2>1:
            if opposite2:
                game_over=True
                b=True
                break
        player2.save_test(event)
        check_tick2=player2.choose_boost(event)
    
    if a==True or b==True:
        break

    food_position_list=[]
    for food in foods:
        food_position_list.append((food.x, food.y))

    game_display.fill(BLACK)

    player1.tick()
    player1.save_position(body_len1)
    for food in foods:
        if food.active:     
            food.draw()

        if player1.x==food.x and player1.y==food.y:
            food.active=False
            foods.remove(food)
            #food를 새롭게 추가
            other_food1=Food(game_display) 
            foods.append(other_food1)
            #새로운 먹이가 기존의 먹이 및 뱀과 만나지 않게 하기
            TOFTOF1=True
            while TOFTOF1:
                TOFlist1=[]
                other_food1.food_replace()
                for i in player1.position_list:
                    TOF1=other_food1.check_food(i[0], i[1])
                    TOFlist1.append(TOF1)
                for i in food_position_list:
                    TOF1=other_food1.check_food(i[0], i[1])
                    TOFlist1.append(TOF1)
                if True not in TOFlist1:
                    TOFTOF1=False
            #몸통을 새롭게 추가
            body_len1+=1
    if check_tick1:
        player1.tick()
        player1.save_position(body_len1)
        for food in foods:
            if food.active:     
                food.draw()

            if player1.x==food.x and player1.y==food.y:
                food.active=False
                foods.remove(food)
                #food를 새롭게 추가
                other_food1=Food(game_display) 
                foods.append(other_food1)
                #새로운 먹이가 기존의 먹이 및 뱀과 만나지 않게 하기
                TOFTOF1=True
                while TOFTOF1:
                    TOFlist1=[]
                    other_food1.food_replace()
                    for i in player1.position_list:
                        TOF1=other_food1.check_food(i[0], i[1])
                        TOFlist1.append(TOF1)
                    for i in food_position_list:
                        TOF1=other_food1.check_food(i[0], i[1])
                        TOFlist1.append(TOF1)
                    if True not in TOFlist1:
                        TOFTOF1=False
                #몸통을 새롭게 추가
                body_len1+=1

    player2.tick()
    player2.save_position(body_len2)
    for food in foods:
        if food.active:     
            food.draw()

        if player2.x==food.x and player2.y==food.y:
            food.active=False
            foods.remove(food)
            #food를 새롭게 추가
            other_food2=Food(game_display) 
            foods.append(other_food2)
            #새로운 먹이가 기존의 먹이 및 뱀과 만나지 않게 하기
            TOFTOF2=True
            while TOFTOF2:
                TOFlist2=[]
                other_food2.food_replace()
                for i in player2.position_list:
                    TOF2=other_food2.check_food(i[0], i[1])
                    TOFlist2.append(TOF2)
                for i in food_position_list:
                    TOF2=other_food2.check_food(i[0], i[1])
                    TOFlist2.append(TOF2)
                if True not in TOFlist2:
                    TOFTOF2=False
            #몸통을 새롭게 추가
            body_len2+=1
    if check_tick2:
        player2.tick()
        player2.save_position(body_len2)
        for food in foods:
            if food.active:     
                food.draw()

            if player2.x==food.x and player2.y==food.y:
                food.active=False
                foods.remove(food)
                #food를 새롭게 추가
                other_food2=Food(game_display) 
                foods.append(other_food2)
                #새로운 먹이가 기존의 먹이 및 뱀과 만나지 않게 하기
                TOFTOF2=True
                while TOFTOF2:
                    TOFlist2=[]
                    other_food2.food_replace()
                    for i in player2.position_list:
                        TOF2=other_food2.check_food(i[0], i[1])
                        TOFlist2.append(TOF2)
                    for i in food_position_list:
                        TOF2=other_food2.check_food(i[0], i[1])
                        TOFlist2.append(TOF2)
                    if True not in TOFlist2:
                        TOFTOF2=False
                #몸통을 새롭게 추가
                body_len2+=1
         
    player1.draw()
    player2.draw()

    #몸통을 새롭게 추가 
    try:
        body_list1=[]
        for i in player1.position_list[-2:-(body_len1+1):-1]:
            body1=Snake_Body(game_display, RED)
            body1.x=i[0]
            body1.y=i[1]
            body1.draw()
            body_list1.append(body1)
    except(IndexError):
        pass

    try:
        body_list2=[]
        for i in player2.position_list[-2:-(body_len2+1):-1]:
            body2=Snake_Body(game_display, Yellow)
            body2.x=i[0]
            body2.y=i[1]
            body2.draw()
            body_list2.append(body2)
    except(IndexError):
        pass

    pygame.display.update()

    #먹이를 다 먹으면 게임 오버 
    if not bool(foods):
        game_over=True
    
    #바깥에 나가면 게임 오버 
    out_of_space=False 
    if player1.x<0 or player1.x>=space_width or player1.y<0 or player1.y>=space_height:
        out_of_space=True
    if player2.x<0 or player2.x>=space_width or player2.y<0 or player2.y>=space_height:
        out_of_space=True
    if out_of_space:
        game_over=True
    
    #몸통과 만나면 게임 오버
    meet_body=False
    for i in body_list1:
        if i.x==player1.x and i.y==player1.y:
            meet_body=True
        if i.x==player2.x and i.y==player2.y:
            meet_body=True
    for i in body_list2:
        if i.x==player2.x and i.y==player2.y:
            meet_body=True
        if i.x==player1.x and i.y==player1.y:
            meet_body=True
    if player1.x==player2.x and player1.y==player2.y:
        meet_body=True
    if meet_body:
        game_over=True
    
    clock.tick(10)