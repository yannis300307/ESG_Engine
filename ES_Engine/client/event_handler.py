import pygame
from pygame.locals import *


class EventHandler:
	def __init__(self, engine):
		self.engine = engine
		self.events = []

	def register_event(self, event, fun):
		self.events.append((event, fun))

	def remove_event(self, event):
		self.events.pop(event)

	def handle(self):
		for e in pygame.event.get():
			if e.type == QUIT:
				self.engine.quit()
			for event in self.events:
				if event[0] == e.type:
					event[1](e)
