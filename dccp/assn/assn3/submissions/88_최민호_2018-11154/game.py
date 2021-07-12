from random import randint
from pygame import display, init, draw, event, time
from pygame.constants import KEYDOWN, K_DOWN, K_ESCAPE, K_LEFT, K_LSHIFT, K_RIGHT, K_RSHIFT, K_UP, K_a, K_d, K_g, K_i, K_j, K_k, K_l, K_s, K_w, QUIT
from pygame.display import update

# problems to solve:
'''
    1) select player number input (min: 1 max: 3)
    2) print_winner function > when two players coincidently die, only one loses
    3) can't do survival match for 3 players
    4) score board
'''

# color constants
BLACK = (0, 0, 0)
WHITE = (255,255,255)
RED = (255, 0, 0)
LIGHT_RED = (255, 100, 100)
GREEN = (0, 255, 0)
LIGHT_GREEN = (100, 255, 100)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)
YELLOW = (255, 255, 0)

# display constants
DISPLAY_X = 800
DISPLAY_Y = 600
DISPLAY_XY = (DISPLAY_X, DISPLAY_Y)
DISPLAY_COLOR = BLACK
GRID_SIZE = 10
RANGE_OF_LOCATION = (range(DISPLAY_X // GRID_SIZE), range(DISPLAY_Y // GRID_SIZE))

CAPTION = 'DCCP SNAKE GAME by MINHO'

# direction constants
class Direction:
    
    def __init__(self, name):
        
        self.name = name

STOP = Direction('STOP')
LEFT = Direction('LEFT')
RIGHT = Direction('RIGHT')
UP = Direction('UP')
DOWN = Direction('DOWN') 
OPPOSITE_DIRECTION = {LEFT: RIGHT, RIGHT: LEFT, UP: DOWN, DOWN: UP}

# extra commands
class ExtraCommand:

    def __init__(self, name):

        self.name = name

EXIT = ExtraCommand('EXIT')
PLAYER_BOOST = ExtraCommand('PLAYER BOOST')

# player constants
PLAYER_INITIAL_LENGTH = 5
PLAYER_SPEED = 1
PLAYER_BOOST_SPEED = 2

PLAYER_NUMBER = 2 #to make more players than 3, you must add the color and control for the new player

PLAYERS_COLOR = [RED, GREEN, BLUE]
PLAYERS_HEAD_COLOR = {RED: LIGHT_RED, GREEN: LIGHT_GREEN, BLUE: LIGHT_BLUE}
PLAYERS_CONTROL = {K_LEFT: (0, LEFT), K_RIGHT: (0, RIGHT), K_UP: (0, UP), K_DOWN: (0, DOWN), K_RSHIFT: (0, PLAYER_BOOST),
        K_a: (1, LEFT), K_d: (1, RIGHT), K_w: (1, UP), K_s: (1, DOWN), K_LSHIFT: (1, PLAYER_BOOST),  
            K_j: (2, LEFT), K_l: (2, RIGHT), K_i: (2, UP), K_k: (2, DOWN), K_g: (2, PLAYER_BOOST), # key: (player_number, direction or speed)
                K_ESCAPE: (-1, EXIT)} # key: (-1 = options, command)

#food constants
FOOD_NUMBER = 20
FOOD_COLOR = YELLOW

'''
def winner_print(players): 
    players_that_lost = []

    for player in players:
        if player.game_over == True:
            players_that_lost.append(player)

    players_that_won = players

    for player in players_that_lost:
        players_that_won.remove(player)

    for i, player in enumerate(players_that_won) :
        if i > 0:
            print('&', end = ' ')
        print('Player' + str(player.number), end = ' ')
    print('won the game')
    
    return players_that_won
'''

class DisplayObject:

    def __init__(self, initial_location: tuple, color, size: tuple = (1,1)):
        self.location = initial_location # (x,y)
        self.size = size # (w,h)
        self.color = color

    def draw_object(self, game_display, DisplayObject) :
        object_data = [*DisplayObject.location, *DisplayObject.size]
        draw.rect(game_display, DisplayObject.color, [ GRID_SIZE*e for e in object_data ])

class PlayerBody(DisplayObject):

    def __init__(self, initial_location: tuple, color):
        super().__init__(initial_location, color)
    
class Player:
    number_of_players = 0

    def __init__(self, initial_location: tuple, color, speed: int):

        Player.number_of_players += 1
        self.number = self.number_of_players
        self.length = PLAYER_INITIAL_LENGTH
        self.head_location = initial_location
        self.color = color
        self.speed = speed
        self.direction = STOP
        self.delta = {LEFT: (-1, 0), RIGHT: (1, 0), UP: (0, -1), DOWN: (0, 1)}
        player_initial_x, player_initial_y = initial_location
        self.game_over = False

        self.body = []
        for i in range(self.length):
            if i == 0:
                self.body.append(PlayerBody(initial_location = (player_initial_x, player_initial_y + i), color = PLAYERS_HEAD_COLOR[color]))
            else:
                self.body.append(PlayerBody(initial_location = (player_initial_x, player_initial_y + i), color = color))
    
    def direction_change(self, direction_or_speed):
        
        self.direction = direction_or_speed
        
    def speed_change(self, speed):
        
        self.speed = speed

    def eat(self):
        self.body.append(PlayerBody(self.body[-1].location, self.color)) # the created location, isn't actually so important
        self.length += 1
    
    def location_change(self):

        if self.direction != STOP:

            dx, dy = player.delta[player.direction]            
            new_head_location = (player.head_location[0] + dx, player.head_location[1] + dy)
            
            # unable backwarding
            if player.body[1].location == new_head_location:

                self.direction = OPPOSITE_DIRECTION[self.direction]
                dx, dy = self.delta[self.direction]            
                new_head_location = (self.head_location[0] + dx, self.head_location[1] + dy)
            
            self.head_location = new_head_location 
        
            if self.game_over == False:
                for i in range(self.length - 1, -1, -1):
                    if i == 0:
                        self.body[i].location = self.head_location
                    else:
                        self.body[i].location = self.body[i-1].location



class Food(DisplayObject):
    
    def __init__(self, initial_location: tuple, color):
        
        super().__init__(initial_location, color, (1, 1))
        self.color = color
    
    def eaten(self, display_objects):
        food_not_appended = True

        while food_not_appended: 
            
            food_x = randint(0, DISPLAY_X//GRID_SIZE - 1)
            food_y = randint(0, DISPLAY_Y//GRID_SIZE - 1)

            for food in display_objects:

                if (food_x, food_y) == food.location:
                    break
                    
                else:
                    self.location = (food_x, food_y)
                    food_not_appended = False

class Game:

    def __init__(self):

        init()
        self.clock = time.Clock()        
        self.game_over = False
        self.game_display = self.set_display(display_size = DISPLAY_XY, color = DISPLAY_COLOR, caption = CAPTION)
        
        # create objects
        self.display_objects = []
        self.players = self.create_players(player_number = PLAYER_NUMBER)
        self.foods = self.create_foods(food_number = FOOD_NUMBER)
         
        
    def set_display(self, display_size, color, caption):
    
        game_display = display.set_mode(display_size)
        game_display.fill(color)
        display.set_caption(caption)

        return game_display

    def create_players(self, player_number):
        
        players = []

        for i in range(player_number):
            player_initial_x = (player_number - i) * DISPLAY_X // GRID_SIZE // (PLAYER_NUMBER + 1) 
            player_initial_y = DISPLAY_Y // GRID_SIZE // 2
            players.append(Player(initial_location = (player_initial_x, player_initial_y), color = PLAYERS_COLOR[i], speed = PLAYER_SPEED))
        
        for player in players:
            self.display_objects += player.body

        return players

    def create_foods(self, food_number):
    
        foods = []
        
        for _ in range(food_number):
            
            food_not_appended = True
            
            while food_not_appended:
                food_x = randint(0, DISPLAY_X // GRID_SIZE - 1)
                food_y = randint(0, DISPLAY_Y // GRID_SIZE - 1)
                                
                for obj in self.display_objects:
                    if (food_x, food_y) == obj.location:
                        break

                else:
                    food = Food(initial_location = (food_x,food_y), color = FOOD_COLOR)
                    foods.append(food)
                    self.display_objects.append(food)
                    food_not_appended = False
        
        return foods

    def crash_check(self):

        for player in self.players:
                                                                            
            # check crushes
            players_body_location = [body.location for player in self.players for body in player.body]
            players_body_location.remove(player.head_location)

            # player crushes with itself, or the other player
            if player.head_location in players_body_location:
                player.game_over = True
                        
            # player crushes with the wall
            elif not player.head_location[0] in RANGE_OF_LOCATION[0] or not player.head_location[1] in RANGE_OF_LOCATION[1]:
                player.game_over = True

        if any([player.game_over for player in self.players]) :
            self.game_over = True

    def food_interaction(self) :
        
        foods_location = {food.location: food for food in self.foods}
            
        for player in self.players:

            if player.head_location in foods_location:
                
                food = foods_location[player.head_location]
                player.eat()
                food.eaten(self.display_objects)

    def update_display(self) :
        
        self.game_display.fill(DISPLAY_COLOR)

        display_objects = [body for player in self.players for body in player.body] + self.foods 
        
        for obj in display_objects:
            obj.draw_object(self.game_display, obj)

        update()


# start
snake_game = Game()

i = 0

while not snake_game.game_over:
    
    for e in event.get(): 
        
        if e.type == QUIT:
            snake_game.game_over = True
            break

        elif e.type == KEYDOWN:

            if e.key in PLAYERS_CONTROL:
                player_and_command = PLAYERS_CONTROL[e.key]

                if type(player_and_command[1]) == ExtraCommand :
                    
                    if player_and_command[1] == EXIT:
                        snake_game.game_over = True

                    elif player_and_command[1] == PLAYER_BOOST:
                        snake_game.players[player_and_command[0]].speed_change(PLAYER_BOOST_SPEED)

                elif type(player_and_command[1]) == Direction :
                    snake_game.players[player_and_command[0]].direction_change(player_and_command[1])
    
    for i in range(PLAYER_BOOST_SPEED):
        
        for player in snake_game.players:

            if player.speed >= i + 1:
                player.location_change()

        snake_game.food_interaction()
        snake_game.crash_check()

        if snake_game.game_over == False :
            snake_game.update_display()   
        
        else:
            break
    
    for player in snake_game.players:

        player.speed = PLAYER_SPEED
    
    snake_game.clock.tick(10)






