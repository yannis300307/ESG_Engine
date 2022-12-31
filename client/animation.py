class Anim:
	def __init__(self, change_frame_time):
		self.frames = []
		self.change_frame_time = change_frame_time
		self.current_frame = 0
		self.time = 0

	def add_frame(self, frame):
		self.frames.append(frame.convert_alpha())

	def get_frame_nbr(self):
		return len(self.frames)

	def get_frame(self, delta: int):
		self.update_current_frame(delta)
		if self.time >= self.change_frame_time:
			self.current_frame += 1
			self.time = 0
			if self.current_frame >= len(self.frames):
				self.current_frame = 0
		return self.frames[self.current_frame]

	def update_current_frame(self, delta: float):
		self.time += delta

	def get_specific_frame(self, base: int):
		if self.time >= self.change_frame_time:
			self.current_frame += 1
			self.time = 0
			if self.current_frame >= len(self.frames):
				self.current_frame = 0
		return self.frames[(self.current_frame+base) % (len(self.frames))]
