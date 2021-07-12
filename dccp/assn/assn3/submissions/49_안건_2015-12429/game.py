import pygame
import random
from food import Food
from player import Player

pygame.init()

game_display = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

game_over = False
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
p1_headcolor = (0, 163, 210)
p1_bodycolor = (0, 103, 114)
p2_headcolor = (255, 215, 0)
p2_bodycolor = (154, 120, 0)
food_tray = [Food(game_display) for _ in range(20)]
player_tray = [Player(600, 300, 0, 0, p1_headcolor, p1_bodycolor, game_display, pygame.KMOD_RSHIFT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN), \
               Player(200, 300, 0, 0, p2_headcolor, p2_bodycolor, game_display, pygame.KMOD_LSHIFT, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)]
obj_tray = food_tray + player_tray

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True; break
        # 각 player 안에 event 넣어주기
        for player in player_tray:
            player.handle_event(event)

    for player in player_tray:
        player.move()
    
    body_tray = [body for player in player_tray for body in player.body]
    
    # 각 요소들 사이 상호작용 하기
    for player in player_tray:
        for food in food_tray:
            player.interact(food)
        for body in body_tray:
            player.interact(body)
        for playerr in player_tray:
            player.interact(playerr)
    
    for player in player_tray:
        if player.game_over:
            game_over = True

    # 화면 밖으로 나가는 경우 체크
    for player in player_tray:
        if player.x < 0 or player.x >=800 or player.y < 0 or player.y >= 600:
            game_over = True
    
    game_display.fill(BLACK)
    # 화면에 그리기
    for obj in obj_tray:
        obj.draw()

    # 몸통 movecopy
    for player in player_tray:
        player.body_movecopy()

    # 화면 업데이트
    pygame.display.update()
    clock.tick(7)
