import pygame as p
import random as r

class Player:
    def __init__(self, size, screen):
        self.size = size
        range_x, range_y = size
        self.x = r.randint(0, range_x/10-1)*10
        self.y = r.randint(0, range_y/10-1)*10
        self.dx = 0
        self.dy = 0
        self.screen = screen
        self.bodylist = list()
        
    def set_HeadColor(self, color):
        self.headColor = color

    def set_BodyColor(self, color):
        self.bodyColor = color

    def makeBody_Long(self, boost): # food를 먹었을 때, 길이 늘리기
        if not boost:
            self.bodylist.append([self.x-self.dx, self.y-self.dy])
        else:
            try:
                del self.bodylist[0]
                self.bodylist.append([self.x-2*self.dx, self.y-2*self.dy])
                self.bodylist.append([self.x-self.dx, self.y-self.dy])
            except:
                self.bodylist.append([self.x-self.dx, self.y-self.dy])
    def makeBody_Long2(self):
        try:
            del self.bodylist[0]
            self.bodylist.append([self.x-2*self.dx, self.y-2*self.dy])
            self.bodylist.append([self.x-self.dx, self.y-self.dy])
        except:
            self.bodylist.append([self.x-self.dx, self.y-self.dy])

    def bodyManager(self, boost): # body가 존재할 때, 길이 유지
        if len(self.bodylist)>0:
            if not boost:
                del self.bodylist[0]
                self.bodylist.append([self.x-self.dx, self.y-self.dy])
            else:
                del self.bodylist[0]
                try:
                    del self.bodylist[0]
                    self.bodylist.append([self.x-2*self.dx, self.y-2*self.dy])
                    self.bodylist.append([self.x-self.dx, self.y-self.dy])
                except:
                    self.bodylist.append([self.x-self.dx, self.y-self.dy])
                
    def event_Handling(self, event):
        if event.key == p.K_UP:
            self.dx = 0
            self.dy = -10
        elif event.key == p.K_DOWN:
            self.dx = 0
            self.dy = 10
        elif event.key == p.K_LEFT:
            self.dx = -10
            self.dy = 0
        elif event.key == p.K_RIGHT:
            self.dx = 10
            self.dy = 0

    def draw(self, color):
        p.draw.rect(self.screen, color, [self.x, self.y, 10, 10])

    def bodyDraw(self, color): # 몸 그리기
        for i in range(len(self.bodylist)):
            p.draw.rect(self.screen, color, [self.bodylist[i][0], self.bodylist[i][1], 10, 10])

    def pos_change(self, boost):
        self.x += self.dx
        self.y += self.dy
        if boost:
            self.x += self.dx
            self.y += self.dy

    def game_End(self):
        x_range, y_range = self.size
        if self.x <= -10:   
            return True
        if self.x >= x_range:
            return True
        if self.y <= -10:
            return True
        if self.y >= y_range:
            return True
        if [self.x, self.y] in self.bodylist:
            return True
        return False


class Player2:
    def __init__(self, size, screen):
        self.size = size
        range_x, range_y = size
        self.x = r.randint(0, range_x/10-1)*10
        self.y = r.randint(0, range_y/10-1)*10
        self.dx = 0
        self.dy = 0
        self.screen = screen
        self.bodylist = list()
        
    def set_HeadColor(self, color):
        self.headColor = color

    def set_BodyColor(self, color):
        self.bodyColor = color

    def makeBody_Long(self, boost): # food를 먹었을 때, 길이 늘리기
        if not boost:
            self.bodylist.append([self.x-self.dx, self.y-self.dy])
        else:
            try:
                del self.bodylist[0]
                self.bodylist.append([self.x-2*self.dx, self.y-2*self.dy])
                self.bodylist.append([self.x-self.dx, self.y-self.dy])
            except:
                self.bodylist.append([self.x-self.dx, self.y-self.dy])

    def makeBody_Long2(self):
        try:
            del self.bodylist[0]
            self.bodylist.append([self.x-2*self.dx, self.y-2*self.dy])
            self.bodylist.append([self.x-self.dx, self.y-self.dy])
        except:
            self.bodylist.append([self.x-self.dx, self.y-self.dy])

    def bodyManager(self, boost): # body가 존재할 때, 길이 유지
        if len(self.bodylist)>0:
            if not boost:
                del self.bodylist[0]
                self.bodylist.append([self.x-self.dx, self.y-self.dy])
            else:
                del self.bodylist[0]
                try:
                    del self.bodylist[0]
                    self.bodylist.append([self.x-2*self.dx, self.y-2*self.dy])
                    self.bodylist.append([self.x-self.dx, self.y-self.dy])
                except:
                    self.bodylist.append([self.x-self.dx, self.y-self.dy])
                
    def event_Handling(self, event):
        if event.key == ord('w'):
            self.dx = 0
            self.dy = -10
        elif event.key == ord('s'):
            self.dx = 0
            self.dy = 10
        elif event.key == ord('a'):
            self.dx = -10
            self.dy = 0
        elif event.key == ord('d'):
            self.dx = 10
            self.dy = 0

    def draw(self, color):
        p.draw.rect(self.screen, color, [self.x, self.y, 10, 10])

    def bodyDraw(self, color): # 몸 그리기
        for i in range(len(self.bodylist)):
            p.draw.rect(self.screen, color, [self.bodylist[i][0], self.bodylist[i][1], 10, 10])

    def pos_change(self, boost):
        self.x += self.dx
        self.y += self.dy
        if boost:
            self.x += self.dx
            self.y += self.dy

    def game_End(self):
        x_range, y_range = self.size
        if self.x <= -10:   
            return True
        if self.x >= x_range:
            return True
        if self.y <= -10:
            return True
        if self.y >= y_range:
            return True
        if [self.x, self.y] in self.bodylist:
            return True
        return False

