import pygame

from ESG_Engine.client.particles_emitters_manager import ParticlesEmittersManager
from ESG_Engine.client.renderer import Renderer
from ESG_Engine.client.sound_manager import SoundManager
from ESG_Engine.core.engine_core import Core
from ESG_Engine.client.event_handler import EventHandler
from ESG_Engine.client.camera import Camera
from ESG_Engine.client.client_network import ClientNetwork


pygame.init()


class Client(Core):
	def __init__(self, wd_size):
		super().__init__()
		self.camera = Camera(wd_size, self.map)
		self.renderer = Renderer(wd_size, self)
		self.event_handler = EventHandler(self)
		self.network = ClientNetwork()
		self.particles_emitters_manager = ParticlesEmittersManager()
		self.sound_manager = SoundManager()

	def init_network(self, address, port):
		self.network.init_client(address, port)

	def tick(self):
		delta = super().tick()
		self.event_handler.handle()
		self.particles_emitters_manager.tick(delta)

	def render(self):
		self.camera.center(self.clock.last_delta)
		self.renderer.update(self.clock.last_delta)

	def quit(self):
		if self.network.socket is not None:
			self.network.close()
		pygame.quit()
		super().quit()
