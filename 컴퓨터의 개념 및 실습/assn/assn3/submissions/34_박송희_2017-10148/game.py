import pygame
import random

WHITE = (255,255,255)
RED   = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE  = (  0,  0,255)
BLACK = (  0,  0,  0)
PINK  = (255,192,203)

class GridObject : 
    def __init__(self,x,y,game,color) :
        self.game = game 
        self.active = True
        self.color = color 
        self.x = x # grid column index
        self.y = y # grid row index
    
    def handle_event(self,event) :
        pass

    def handle_tick(self) :
        pass

    def draw(self) :
        block_size = self.game.block_size
        pygame.draw.rect( self.game.display, self.color, \
            [self.x*block_size, self.y*block_size, block_size, block_size] )


class Player(GridObject) :
    
    def __init__(self,x,y,game) :
        self.game = game
        self.x = [x]
        self.y = [y]
        self.dx = 0
        self.dy = 0
        self.active = True
        self.boost_active = False

    def set_color(self) :
        pass

    def set_keyboard(self) :
        pass

    # event, self state update
    def handle_event(self, event) :

        if event.type == pygame.KEYDOWN :
            
            # boost
            shift = pygame.key.get_pressed()
            if shift[self.boost] :
                self.boost_active = True
                move = 2
            else :
                self.boost_active = False
                move = 1

            # handle
            if event.key == self.left :
                self.direction = 'left'
                self.dx = -move
                self.dy = 0
            elif event.key == self.right :
                self.direction = 'right'
                self.dx = move
                self.dy = 0
            elif event.key == self.up :
                self.direction = 'up'
                self.dx = 0
                self.dy = -move
            elif event.key == self.down :
                self.direction = 'down'
                self.dx = 0
                self.dy = +move
    
    # tick, self state update
    def handle_tick(self) :

        # x[1]~x[n]까지 x[0]~x[n-1] 위치로 이동
        for i in range(len(self.x)-1,0,-1) :
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # head 위치 이동
        self.x[0] += self.dx
        self.y[0] += self.dy

    # game over
    def display_out(self) :
        if  self.x[0] < 0 or self.game.n_cols < self.x[0] or \
            self.y[0] < 0 or self.game.n_rows < self.y[0] :
            return True
        return False

    def self_collide(self) :
        for i in range(1,len(self.x)) :
            if self.x[0] == self.x[i] and self.y[0] == self.y[i] :
                return True
        return False

    # snake body append
    def grow(self) :
        if self.direction == 'left' :
            self.x.insert(0,self.x[0]-1)
            self.y.insert(0,self.y[0])
        elif self.direction == 'right' :
            self.x.insert(0,self.x[0]+1)
            self.y.insert(0,self.y[0])
        elif self.direction == 'up' :
            self.x.insert(0,self.x[0])
            self.y.insert(0,self.y[0]-1)
        elif self.direction == 'down' :
            self.x.insert(0,self.x[0])
            self.y.insert(0,self.y[0]+1)

    # color : head = white, body = red
    def draw(self) :
        block_size = self.game.block_size
        # head drawing
        pygame.draw.rect( self.game.display, self.head_color, \
            [self.x[0]*block_size, self.y[0]*block_size, block_size, block_size] )
        # body drawing
        for i in range(1,len(self.x)) :
            pygame.draw.rect( self.game.display, self.body_color, \
                [self.x[i]*block_size, self.y[i]*block_size, block_size, block_size] )


class Player1(Player) :
    head_color = RED
    body_color = PINK

    boost = pygame.K_LSHIFT
    left  = pygame.K_a
    right = pygame.K_d
    up    = pygame.K_w
    down  = pygame.K_s

    def __init__(self,x,y,game) :
        super().__init__(x,y,game)


class Player2(Player) :
    head_color = BLUE
    body_color = WHITE

    boost = pygame.K_RSHIFT
    left  = pygame.K_LEFT
    right = pygame.K_RIGHT
    up    = pygame.K_UP
    down  = pygame.K_DOWN

    def __init__(self,x,y,game) :
        super().__init__(x,y,game)

    


class Food(GridObject) :
    color = GREEN
    def __init__(self, game) :
        x = random.randint(0, game.n_cols-1)
        y = random.randint(0, game.n_rows-1) 
        super().__init__(x,y,game,self.color)
        

class Game :

    block_size = 10
    def __init__(self, n_rows=60, n_cols=80) :
        
        self.n_rows = n_rows
        self.n_cols = n_cols

        pygame.init()
        pygame.display.set_caption('Snake Game')

        self.display = pygame.display.set_mode( (n_cols*self.block_size, n_rows*self.block_size) )     
        self.clock = pygame.time.Clock()
        self.game_over = 0

        self.objects = []

    def active_objects(self) :
        for obj in self.objects :
            if obj.active :
                yield obj

    def collide(self, obj1, obj2) :
        coor1 = [ (obj1.x[i],obj1.y[i]) for i in range(len(obj1.x)) ]
        coor2 = [ (obj2.x[i],obj2.y[i]) for i in range(len(obj2.x)) ]
        for i in range(len(obj1.x)) :
            if coor1[i] in coor2 :
                return True
        return False

    def eating(self, player, food) :

        if player.boost_active :
            if player.direction == 'left' :
                if (player.x[0]==food.x or player.x[0]+1==food.x) and player.y[0]==food.y :
                    food.active = False
                    self.objects.append( Food(self) )
                    player.grow() 
            elif player.direction == 'right' :
                if (player.x[0]==food.x or player.x[0]-1==food.x) and player.y[0]==food.y :
                    food.active = False
                    self.objects.append( Food(self) )
                    player.grow() 
            elif player.direction == 'up' :
                if player.x[0]==food.x and (player.y[0]==food.y or player.y[0]==food.y+1) :
                    food.active = False
                    self.objects.append( Food(self) )
                    player.grow() 
            elif player.direction == 'down' :
                if player.x[0]==food.x and (player.y[0]==food.y or player.y[0]==food.y-1) :
                    food.active = False
                    self.objects.append( Food(self) )
                    player.grow() 
                        
        else :
            if food.x == player.x[0] and food.y == player.y[0] :
                food.active = False
                self.objects.append( Food(self) )
                player.grow()


    def play(self, n_foods=20) :
        
        self.objects = [
            Player1(30,30,self),
            Player2(50,30,self),
            *[ Food(self) for _ in range(n_foods) ]
        ]

        while not self.game_over :

            #keyboard input
            for event in pygame.event.get() :

                # game over
                if event.type == pygame.QUIT :
                    self.game_over = 1
                    break

                # handle event
                for obj in self.active_objects() :
                    obj.handle_event(event)
            
            # player move
            for obj in self.active_objects() :
                obj.handle_tick()
            
            # eating food 
            for obj1 in self.objects :
                for obj2 in self.objects :
                    if isinstance(obj1,Player) and isinstance(obj2,Food) :
                        if obj2.active :
                            self.eating(obj1,obj2)
                
            # draw
            self.display.fill(BLACK)
            for obj in self.active_objects() :
                obj.draw()

            # display update
            pygame.display.update()
            self.clock.tick(10)

            # game over 
            for obj1 in self.objects :
                if self.game_over :
                    break
                if isinstance(obj1,Player) :
                    # when player goes out of the screen
                    self.game_over += obj1.display_out()

            for obj1 in self.objects :
                if self.game_over :
                    break
                if isinstance(obj1,Player) :
                    # when player collides.
                    self.game_over += obj1.self_collide()

            for obj1 in self.objects :     
                for obj2 in self.objects :
                    if self.game_over :
                        break
                    if isinstance(obj1,Player) and isinstance(obj2,Player) :
                        if obj1 != obj2 :
                            self.game_over += self.collide(obj1,obj2)

            if self.game_over :
                break
            



if __name__ == '__main__' :
    Game(n_rows=60,n_cols=80).play(n_foods=20)
    