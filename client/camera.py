class Camera:
	def __init__(self, wd_size, map_):
		self.x = 0
		self.y = 0
		self.zoom = 2
		self.lock = False
		self.wd_size = wd_size
		self.map = map_
		self.smooth = 2
		self.target_x = 0
		self.target_y = 0

	def center_on_pos(self, pos):
		if not self.lock:
			self.x = pos[0]
			self.y = pos[1]
			self.check_for_map_outside()

	def center_on_pos_smoothly(self, x, y, smooth, delta):
		if not self.lock:
			centering_speed = self.zoom * delta
			self.x -= (self.x - x) / smooth * centering_speed
			self.y -= (self.y - y) / smooth * centering_speed
			self.check_for_map_outside()

	def center(self, delta):
		if self.smooth > 0:
			self.center_on_pos_smoothly(self.target_x, self.target_y, self.smooth, delta)
		else:
			self.center_on_pos((self.target_x, self.target_y))

	def check_for_map_outside(self):
		self.x = max(min(
			self.x,
			self.map.width * self.map.base_tile_size - (self.wd_size[0] / 2) / self.zoom),
			self.wd_size[0] / 2 / self.zoom)
		self.y = max(min(
			self.y,
			self.map.height * self.map.base_tile_size - (self.wd_size[1] / 2) / self.zoom),
			self.wd_size[1] / 2 / self.zoom)
