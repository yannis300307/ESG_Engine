import random

from ES_Engine.client.animation import Anim


class ParticlesEmitter:
	def __init__(self, x, y, width, height, max_speed: int, max_lifetime: float, texture: Anim, fade_out=True):
		self.rect = [x, y, width, height]
		self.particles = []
		self.texture = texture
		self.fade_out = fade_out
		self.max_speed = max_speed
		self.max_lifetime = max_lifetime
		self.extra_down = 0
		self.extra_up = 0
		self.extra_right = 0
		self.extra_left = 0

	def create_particles(self, nbr: int):
		for i in range(nbr):
			self.particles.append([
				random.randint(self.rect[0], self.rect[0]+self.rect[2]),								# spawn x
				random.randint(self.rect[1], self.rect[1]+self.rect[3]),								# spawn y
				random.randint(-self.max_speed-self.extra_left, self.max_speed+self.extra_right),		# speed x
				random.randint(-self.max_speed-self.extra_up, self.max_speed+self.extra_down),			# speed y
				random.random()*self.max_lifetime,														# max lifetime
				0,																						# current lifetime
				random.randint(0, self.texture.get_frame_nbr())											# base frame nbr
			])

	def update(self, delta: float):
		self.texture.update_current_frame(delta)
		for p in self.particles:
			p[0] += p[2]*delta
			p[1] += p[3]*delta
			p[5] += delta
			if p[5] >= p[4]:
				self.particles.remove(p)
