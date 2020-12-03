import pygame
from pygame import QUIT as QUIT
import random
import types

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (40, 116, 166)
LIGHT_BLUE = (174, 214, 241)
RED = (176, 58, 46)
LIGHT_RED = (245, 183, 177)
GREEN = (0, 255, 0)
RIGHT = 'right'
LEFT = 'left'

class GridObject:
	def __init__(self, x, y, game, color):
		self.game = game
		self.active = True
		self.color = color
		self.x = x   # grid column index
		self.y = y   # grid row index

	def handle_event(self, event):
		pass

	def tick(self, right_shift, left_shift):
		pass
	def interact(self, other):
		pass

	def draw(self):
		block_size = self.game.block_size
		pygame.draw.rect(self.game.display, self.color, [self.x * block_size, self.y * block_size, block_size, block_size])

class Player(GridObject):
	dx = 0
	dy = 0

	def __init__(self, x, y, game, player_id = RIGHT, k_left = pygame.K_LEFT, k_right = pygame.K_RIGHT, k_up = pygame.K_UP, k_down =  pygame.K_DOWN, color = RED, tail_color = LIGHT_RED):
		super().__init__(x, y, game, color)
		self.tail = []
		self.tail_color = tail_color
		self.player_id = player_id
		self.turn = False
		self.k_left = k_left
		self.k_right = k_right
		self.k_up = k_up
		self.k_down = k_down

	def handle_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == self.k_left:
				if self.dx != 1:
					self.dx = -1
					self.dy = 0
			elif event.key == self.k_right:
				if self.dx != -1:
					self.dx = 1
					self.dy = 0
			elif event.key == self.k_up:
				if self.dy != 1:
					self.dy = -1
					self.dx = 0
			elif event.key == self.k_down:
				if self.dy != -1:
					self.dy = 1
					self.dx = 0
			
	def tick(self, right_shift = False, left_shift = False):
		if not ((self.player_id == RIGHT and right_shift) or (self.player_id == LEFT and left_shift) or (not right_shift and not left_shift)):
			self.turn = not self.turn
			if not self.turn:
				return
		if self.tail:
			inactive_obj = self.tail.pop()
			inactive_obj.active = False
			self.tail.insert(0, Tail(self.x, self.y, self.game, color = self.tail_color))
		self.x += self.dx
		self.y += self.dy

	def interact(self, other, game_over = False):
		if isinstance(other, Food):
			if self.x == other.x and self.y == other.y:
				other.active = False
				self.tail.insert(0, Tail(self.x, self.y, self.game, color = self.tail_color))
				self.x += self.dx
				self.y += self.dy
				return True
		elif game_over:
			if self.x == other.x and self.y == other.y:
				return True

		return False 	

class Tail(GridObject):
	def __init__(self, x, y, game, color = LIGHT_RED):
		super().__init__(x, y, game, color)
	def interact(self, other, game_over = False):
		if game_over and isinstance(other, Player):
			if self.x == other.x and self.y == other.y:
				return True
		else:
			return False

class Food(GridObject):
	color = GREEN
	def __init__(self, game):
		x = random.randint(0, game.n_cols - 1)
		y = random.randint(0, game.n_rows - 1)
		super().__init__(x, y, game, self.color)	
	def interact(self, other, new_food = False):
		if new_food:
			if self.x == other.x and self.y == other.y:
				return True
		else:
			return False

class Game:
	block_size = 10
	clock_speed = 10

	def __init__(self, n_cols, n_rows):
		pygame.init()
		pygame.display.set_caption('DCCP Snake Game')
		self.display = pygame.display.set_mode((n_cols * self.block_size, n_rows * self.block_size))
		self.n_rows = n_rows
		self.n_cols = n_cols
		self.clock = pygame.time.Clock()
		self.game_over = False

	def active_objects(self):
		for obj in self.objects:
			if obj.active:
				yield obj

	def play(self, n_foods = 20):
		self.objects = [
			Player(40, 50, self, player_id = RIGHT, k_left = pygame.K_LEFT, k_right = pygame.K_RIGHT, k_up = pygame.K_UP, k_down = pygame.K_DOWN, color = RED, tail_color = LIGHT_RED), 
			Player(20, 30, self, player_id = LEFT, k_left = pygame.K_a, k_right = pygame.K_d, k_up = pygame.K_w, k_down = pygame.K_s,color = BLUE, tail_color = LIGHT_BLUE),
			*[Food(self) for _ in range(n_foods)]
		]
		
		while not self.game_over:
			for event in pygame.event.get():
				if event.type == QUIT:
					self.game_over = True
					break		
				# Handle Events
				for obj in self.active_objects():
					obj.handle_event(event)

			# Handle Clock Speed		
			all_keys = pygame.key.get_pressed()
			right_shift = all_keys[pygame.K_RSHIFT]
			left_shift = all_keys[pygame.K_LSHIFT]

			if right_shift or left_shift:
				self.clock_speed = 20
			else:
				self.clock_speed = 10
			
			# Handle Ticks
			for obj in self.active_objects():
				obj.tick(right_shift, left_shift)
				if isinstance(obj, Player):
					self.objects.extend(obj.tail)


			self.display.fill(BLACK)
			
			#Handle Interact
			for obj1 in self.active_objects():
				for obj2 in self.active_objects():
					if obj1.interact(obj2) or obj2.interact(obj1):
						while True:
							new_food = Food(self)
							overlap = False
							for obj in self.active_objects():
								if new_food.interact(obj, new_food = True):
									overlap = True
									break
							if not overlap:
								self.objects.append(new_food)
								break
			
			# Handle End
			for obj in self.active_objects():
				if isinstance(obj, Player):
					if obj.x >= self.n_cols or obj.x < 0 or obj.y < 0 or obj.y >= self.n_rows:
						self.game_over = True
						break
					else:
						for obj2 in self.active_objects():
							if (isinstance(obj2, Tail) or (isinstance(obj2, Player) and obj2.player_id != obj.player_id)) and obj.interact(obj2, game_over = True):
								self.game_over = True
								break

			if self.game_over:
				break

			# Handle draw
			for obj in self.active_objects():
				obj.draw()
			
			pygame.display.update()

			# Handle End for prob1
			# food_remains = False
			# for obj in self.active_objects():
			# 	if isinstance(obj, Food):
			# 		food_remains = True
		
			# if not food_remains:
			# 	self.game_over = True
			self.clock.tick(self.clock_speed)

if __name__ == '__main__':
	Game(n_rows = 60, n_cols = 80).play(n_foods = 20)