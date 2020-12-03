import pygame
import random

pygame.init()

size = [800,600] # 창 크기 설정
block = 10 # 타일의 크기 
dp = pygame.display.set_mode(size) # 창 변수 설정 
pygame.display.set_caption('Snake game') # 창의 이름 설정
clock = pygame.time.Clock() # 게임 루프 주기 설정(초당 화면 출력 횟수)

white = (255,255,255) # 흰색의 RGB값
black = (0,0,0) # 검은색의 RGB값
red = (255,0,0) # 빨간색의 RGB값
green = (0,255,0) # 초록색의 RGB값
blue = (0,0,255) # 파란색의 RGB값
gray = (128,128,128) # 회색의 RGB값


class Player1: # 1P 클래스
    def __init__(self, x,y,dx,dy,display, color): # 네모가 생성되는 위치, 네모의 이동 간격, 색깔 등을 정의
        self.x = x # x좌표
        self.y = y # y좌표
        self.dx = dx # x축 이동간격
        self.dy = dy # y축 이동간격
        self.display = display # 게임 디스플레이 
        self.color = color # 도형의 색깔 

    def handle(self,event): # 이벤트에 따라 1P 작동 키 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: # 왼쪽 화살표 누르면 왼쪽으로 이동 
                self.dx = -block
                self.dy = 0
            elif event.key == pygame.K_RIGHT: # 오른쪽 화살표 누르면 왼쪽으로 이동 
                self.dx = block
                self.dy = 0
            elif event.key == pygame.K_UP: # 위쪽 화살표 누르면 왼쪽으로 이동 
                self.dy = -block
                self.dx = 0
            elif event.key == pygame.K_DOWN: # 아래쪽 화살표 누르면 왼쪽으로 이동 
                self.dy = block
                self.dx = 0
           
    def tick(self,key): # 이동 함수 + key를 누를 경우 부스트 기능 
        k = pygame.key.get_pressed()
        if k[key]: # key가 눌려져 있다면 속도 2배 
            self.x += 2*self.dx
            self.y += 2*self.dy
        else:
            self.x += self.dx # 안 눌러졌다면 속도 1배 
            self.y += self.dy
 
    def draw(self): # 네모를 화면에 그려주는 함수 
        pygame.draw.rect(self.display ,self.color,[self.x,self.y,block,block])

    def out(self): # 플레이어가 창의 경계 좌표 밖으로 나가면 게임 종료(머리가 완전히 나가야 종료)
        if self.x<-10 or self.x>800:
            return True
        if self.y<-10 or self.y>600:
            return True
    def crush(self,other): # 다른 것과 충돌하는 경우의 함수
        if isinstance(other,Player1): # 충돌 대상이 플레이어의 인스턴스라면 
            if self.x == other.x and self.y == other.y: # 충돌 시 좌표가 같다. 
                return True

class Player2(Player1): # 2P를 1P의 자식 클래스로 설정 
    def handle(self,event): # 이벤트에 따른 2P 조종 방식
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: # a 누르면 왼쪽으로 이동
                self.dx = -block
                self.dy = 0
            elif event.key == pygame.K_d: # d 누르면 오른쪽으로 이동
                self.dx = block
                self.dy = 0
            elif event.key == pygame.K_w: # w 누르면 위쪽으로 이동
                self.dy = -block
                self.dx = 0
            elif event.key == pygame.K_s: # s 누르면 아래쪽으로 이동 
                self.dy = block
                self.dx = 0
    
class Food: # 먹이 클래스
    active = True # 먹히지 않았다면 True 
    def __init__(self,display): 
        self.x = random.randint(0,((size[0]/block)-1)) * block # x, y는 격자 내 크기 10인 block 중에서 랜덤으로 설정 
        self.y = random.randint(0,(size[1]/block)-1) * block
        self.display = display
    def draw(self):
        pygame.draw.rect(self.display,green,[self.x,self.y,block,block])


game_over = False # 게임 종료 변수 (True값이면 게임 종료)
   
snake1 = [Player1(20,30,0,0,dp,white)] # 1P인 뱀의 몸통 리스트(현재 머리 뿐)- 1P는 머리 흰색, 몸통 빨간색
snake2 = [Player2(60,30,0,0,dp,gray)] # 2P인 뱀의 몸통 리스트(현재 머리 뿐)- 2P는 머리 회색, 몸통 파란색
foods = [Food(dp) for i in range(20)] # 먹이 목록 설정 

while not game_over: # 게임 루프
    dp.fill(black) # 화면을 검은색으로 채우기
    head1 = snake1[0] # snake1의 첫째가 머리
    head2 = snake2[0] # snake2의 첫째가 머리 
    clock.tick(10) # FPS 설정 = 초당 10프레임 
    for event in pygame.event.get(): # 게임에서의 이벤트 추출
        print(event)
        if event.type == pygame.QUIT: # 창 닫는 이벤트인 quit으로 게임 종료 
            game_over = True 
            break
        head1.handle(event) # 1P 방향키 조작
        head2.handle(event) # 2P 방향키 조작

 
    head1.tick(pygame.KMOD_RSHIFT) # fps에 따른 1p 머리의 이동 표현. Right Shift 키를 누르면 부스터 가동 
    if len(snake1)>1:# 뱀의 길이가 2 이상이라면, 마지막 꼬리를 지우고 머리 뒷쪽에 새로운 몸통을 추가하는 방식으로 이동
        second = Player1(head1.x-head1.dx,head1.y-head1.dy,head1.dx,head1.dy,dp,red) 
        snake2.insert(1,second) # 머리 바로 뒤에 삽입
        del snake2[-1] # 꼬리 삭제

    head2.tick(pygame.KMOD_LSHIFT) # fps에 따른 2p 머리의 이동 표현. Left Shift 키를 누르면 부스터 가동 
    if len(snake2) >1:# 뱀의 길이가 2 이상이라면, 마지막 꼬리를 지우고 머리 뒷쪽에 새로운 몸통을 추가하는 방식으로 이동
        second = Player2(head2.x-head2.dx,head2.y-head2.dy,head2.dx,head2.dy,dp,blue) # 추가되는 몸통
        snake2.insert(1,second) # 머리 바로 뒤에 삽입
        del snake2[-1] # 꼬리 삭제 

    for x in snake1:
        x.draw() # 1p 뱀 그리기 
    
    for y in snake2:
        y.draw() # 2p 뱀 그리기 

    for i,food in enumerate(foods): # 먹이 목록 중에서(enumerate한 이유는 새 먹이를 먹힌 먹이의 index로 추가하기 위해서입니다. 이래야 먹이가 깜빡거리며 생기지 않는 것 같습니다.)
        if food.active: # 먹이가 안 먹혔다면 
            food.draw() # 먹이 그리기
        for body in snake1:
            if body.x == food.x and body.y== food.y: # 1P의 머리를 포함한 몸통의 좌표가 먹이의 좌표가 같다면(만일 먹이가 몸 속에 생기는 경우 포함)
                food.active = False # 먹이가 먹힌 상태
                foods.pop(i) # i번째 food 제거 
                new = Food(dp) # 새 먹이 인스턴스 생성
                foods.insert(i,new) # 먹이 목록 i 자리에 추가        
                nexthead = Player1(head1.x-head1.dx,head1.y-head1.dy,head1.dx,head1.dy,dp,red) # 기존 머리 바로 뒤에 몸통이 추가됨. 
                snake1.insert(1,nexthead) # snake의 첫째 원소가 머리이므로 0번째에 삽입
        for body in snake2:
            if body.x == food.x and body.y== food.y: # 2P의 머리를 포함한 몸통의 좌표가 먹이의 좌표가 같다면(만일 먹이가 몸 속에 생기는 경우 포함)
                food.active = False # 먹이가 먹힌 상태 
                foods.pop(i) # i번째 food 제거  
                new = Food(dp) # 새 먹이 인스턴스 생성
                foods.insert(i,new) # 먹이 목록 i 자리에 추가
                nexthead = Player2(head2.x-head2.dx,head2.y-head2.dy,head2.dx,head2.dy,dp,blue) # 기존 머리 바로 뒤에 몸통이 추가됨.
                snake2.insert(1,nexthead) # snake의 첫째 원소가 머리이므로 0번째에 삽입
        
    # 게임 종료 경우 
    if head1.out() or head2.out(): # 두 뱀의 머리가 화면 밖으로 나가면 게임 종료 
        game_over = True
        break
        
    for i in range(1,len(snake1)): # 1p의 머리가 몸통과 닿거나, 몸통 쪽으로 이동하려하면 게임 종료
        if snake1[0].x == snake1[i].x and snake1[0].y == snake1[i].y: # 머리와 몸통의 위치 자표가 동일하다면 
            game_over = True
            break
    for i in range(1,len(snake2)): # 2P의 머리가 몸통과 닿거나, 몸통 쪽으로 이동하려하면 게임 종료
        if head2.x == snake2[i].x and head2.y == snake2[i].y: # 머리와 몸통의 위치 자표가 동일하다면 
            game_over = True
            break

    for x in snake1: #1p의 몸통 목록 
        for y in snake2:#2p의 몸통 목록 
            if y.crush(x): # 1p와 2p의 몸이 충돌한다면 게임 종료 
                game_over = True
                break
        
    pygame.display.update() # 게임 상태 업데이트
   
    

        
        


