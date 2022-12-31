import time


class Clock:
	def __init__(self):
		self.__past = time.time_ns()*0.000000001
		self.last_delta = 0
		self.repeating_task = []

	def get_delta(self):
		"""Return the current delta time"""
		current_time = time.time_ns()*0.000000001
		self.last_delta = current_time-self.__past
		self.__past = current_time
		return self.last_delta

	def get_fps(self):
		"""Return the game FPS"""
		return 1/self.last_delta

	def register_task(self, delay: float, fun):
		"""Add a task whish will be executed each delay sec."""
		self.repeating_task.append([0., delay, fun])  # timer; delay; function

	def update_tasks(self):
		for task in self.repeating_task:
			task[0] += self.last_delta
			if task[0] >= task[1]:
				task[2]()
				task[0] = 0.
