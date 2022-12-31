import math


class Entity:
	"""Represent an entity. It can be moved."""
	def __init__(self):
		self.x = 20
		self.y = 0
		self.speed_x = 0
		self.speed_y = 0
		self.colliding = [False, False, False, False]  # right, left, up, down
		self.collider_points = []
		self.gravity = 0
		self.dir = 0  # 0: right; 1: left

	def set_collider_points(self, points):
		"""Add collider points.
		Ex: [(0, 0), (1, 1), (0, 1), (1, 0)]
		((0, 0) is top left point and (1, 1) is bottom right point)"""
		self.collider_points = points

	def update(self, delta, map_):
		self.speed_y += self.gravity * delta
		speed = math.ceil(math.sqrt(self.speed_x**2+self.speed_y**2))*2
		step_x = self.speed_x*delta / max(speed, 1)  # TODO: modify by max speed (or no)
		step_y = self.speed_y*delta / max(speed, 1)
		self.colliding = [False, False, False, False]
		for i in range(int(speed)):
			self._move(step_x, step_y, map_)

	def _move(self, step_x, step_y, map_):
		self.y += step_y
		if self._check_for_collision(map_):
			self.y -= step_y
			if self.speed_y > 0:
				self.colliding[3] = True
			elif self.speed_y < 0:
				self.colliding[2] = True
			self.speed_y = 0
		self.x += step_x
		if self._check_for_collision(map_):
			self.x -= step_x
			if self.speed_x > 0:
				self.colliding[0] = True
			elif self.speed_x < 0:
				self.colliding[1] = True
			self.speed_x = 0

	def _check_for_collision(self, map_):
		for point in self.collider_points:
			colliding_point_x = self.x/map_.base_tile_size+point[0]
			colliding_point_y = self.y/map_.base_tile_size+point[1]
			if map_.get_tile_at(int(colliding_point_x), int(colliding_point_y), map_.colliding_layer) > 0:
				return True
		return False
