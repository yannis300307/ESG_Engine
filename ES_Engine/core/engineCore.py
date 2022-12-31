from ES_Engine.core.entity_manager import EntityManager
from ES_Engine.core.map import Map
from ES_Engine.core.clock import Clock
from ES_Engine.core.network import Network


class Core:
	"""Core object that is the base of the entire engine."""
	def __init__(self):
		self.map = Map()
		self.entity_manager = EntityManager(self.map)
		self.clock = Clock()
		self.network = Network()
		self.running = True

	def tick(self):
		"""Executed each tick."""
		delta = self.clock.get_delta()
		self.clock.update_tasks()
		self.entity_manager.tick(delta)
		return delta

	def quit(self):
		"""Executed when the user close the programme or the programme quit itself."""
		self.running = False
