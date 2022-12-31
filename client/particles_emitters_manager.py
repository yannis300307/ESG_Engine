from client.particles_emitter import ParticlesEmitter


class ParticlesEmittersManager:
	def __init__(self):
		self.particles_emitters = []

	def add_particles_emitter(self, particles_emitter: ParticlesEmitter) -> ParticlesEmitter:
		"""Add a new particles emitter into the particles emitters list."""
		self.particles_emitters.append(particles_emitter)
		return particles_emitter

	def tick(self, delta):
		for pe in self.particles_emitters:
			pe.update(delta)
