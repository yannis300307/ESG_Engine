from core.entity import Entity
import pygame


class Player(Entity):
	def __init__(self, speed, floor_inertia, void_inertia, jump_strengh):
		super().__init__()
		self.arrows = [False, False, False, False]
		self.speed = speed
		self.walking = False
		self.jumping = False
		self.falling = False
		self.floor_inertia = floor_inertia
		self.void_inertia = void_inertia
		self.jump_strengh = jump_strengh

	def player_control_key_up(self, e):
		if e.key == pygame.K_RIGHT:
			self.arrows[0] = False
		elif e.key == pygame.K_LEFT:
			self.arrows[1] = False
		elif e.key == pygame.K_UP:
			self.arrows[2] = False
		elif e.key == pygame.K_DOWN:
			self.arrows[3] = False

	def player_control_key_down(self, e):
		if e.key == pygame.K_RIGHT:
			self.arrows[0] = True
			self.dir = 0
		elif e.key == pygame.K_LEFT:
			self.arrows[1] = True
			self.dir = 1
		elif e.key == pygame.K_UP:
			self.arrows[2] = True
			if self.colliding[3]:
				self.speed_y -= self.jump_strengh
		elif e.key == pygame.K_DOWN:
			self.arrows[3] = True

	def update(self, delta, map_):
		super().update(delta, map_)
		if self.arrows[0]:
			self.speed_x += self.speed*delta
			self.walking = True
		elif self.arrows[1]:
			self.speed_x -= self.speed*delta
			self.walking = True
		else:
			self.walking = False
			if self.colliding[3]:
				if self.floor_inertia >= 0:
					if self.speed_x == abs(self.speed_x):
						self.speed_x = max(self.speed_x - self.floor_inertia * delta, 0)
					else:
						self.speed_x = min(self.speed_x + self.floor_inertia * delta, 0)
				else:
					self.speed_x = 0
			else:
				if self.void_inertia >= 0:
					if self.speed_x == abs(self.speed_x):
						self.speed_x = max(self.speed_x - self.void_inertia * delta, 0)
					else:
						self.speed_x = min(self.speed_x + self.void_inertia * delta, 0)
				else:
					self.speed_x = 0

		if not self.colliding[3]:
			self.falling = True
			self.jumping = False
			self.walking = False
		elif self.speed_y < 0:
			self.falling = False
			self.jumping = True
			self.walking = False
		else:
			self.falling = False
			self.jumping = False
