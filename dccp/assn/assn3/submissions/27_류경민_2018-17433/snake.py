from utils import * 

class Snake:    
    def __init__(self,x,y, game, headcolor, bodycolor, leftkey, rightkey, upkey, downkey, boostkey):
        self.dx = 0
        self.dy = 0
        self.head = GridObject(x, y, game, headcolor)
        self.game = game  
        self.headcolor = headcolor
        self.bodycolor = bodycolor
        self.leftkey = leftkey
        self.rightkey = rightkey
        self.upkey = upkey
        self.downkey = downkey
        self.boostkey = boostkey
        self.snake_list=[]
        self.if_touched = False

        self.active = True
        self.dummy = None
        self.speed = 1


    def out_of_screen(self):
        if self.head.x > self.game.n_cols or self.head.y > self.game.n_rows:
            return True
        elif self.head.x < 0 or self.head.y < 0:
            return True

        else:
            return False    

    def handle_event(self,event):
        # change speed
        if event.type == pygame.KEYDOWN:
            if event.key == self.boostkey:
                self.speed = 2
        if event.type == pygame.KEYUP:
            if event.key == self.boostkey:
                self.speed = 1         
        if event.type == pygame.KEYDOWN:            
            if event.key == self.leftkey:
                self.dx = -1
                self.dy = 0 
            elif event.key == self.rightkey:
                self.dx = 1 
                self.dy = 0
            elif event.key == self.upkey:
                self.dx = 0
                self.dy = -1 
            elif event.key == self.downkey:
                self.dx = 0
                self.dy = 1 

    def tick(self):
        for i in reversed(range(len(self.snake_list))):
            if i == 0:
                self.snake_list[0].x = self.head.x
                self.snake_list[0].y = self.head.y
            else:
                self.snake_list[i].x = self.snake_list[i-1].x
                self.snake_list[i].y = self.snake_list[i-1].y

        self.head.x += self.dx * self.speed
        self.head.y += self.dy *self.speed

        if self.dummy != None: 
            self.snake_list.append(self.dummy)
            self.dummy = None

    def interact(self, other):
        if isinstance(other, Food):
            if self.head.x == other.x and self.head.y == other.y: 

                if self.snake_list == []:
                    self.dummy = GridObject(self.head.x, self.head.y, self.game, self.bodycolor)
                else: 
                    self.dummy = GridObject(self.snake_list[-1].x, self.snake_list[-1].y, self.game, self.bodycolor)  

        if isinstance(other, Snake):
            for i in range(len(other.snake_list)):
                if self.head.x == other.snake_list[i].x and self.head.y == other.snake_list[i].y: 
                    print("CRASH")
                    self.if_touched = True

            if other != self:
                if self.head.x == other.head.x and self.head.y == other.head.y: 
                    self.if_touched = True

    def draw(self):
        self.head.draw()
        for body in self.snake_list:
            body.draw()

