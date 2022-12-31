import pygame
import math


class Renderer:
	def __init__(self, wd_size, core):
		self.window = pygame.display.set_mode(wd_size)
		self.wd_size = wd_size
		self.engineCore = core
		self.tiles = []
		self.base_tile_size = core.map.base_tile_size
		self.anims = {}
		self.backgrounds = []
		self.resized_bg = self.backgrounds.copy()
		self._past_zoom = 0

	def register_tile(self, tile: pygame.Surface):
		"""Add tile to the tile list for rendering"""
		self.tiles.append(tile.convert_alpha())

	def register_background(self, parralax: int, bg: pygame.Surface):
		"""Add the given background into the background list and store it with parralax."""
		if parralax == -1:
			self.backgrounds.insert(0, (parralax, bg.convert()))
		else:
			self.backgrounds.append((parralax, bg))
			self.backgrounds.sort(reverse=True)
			temp_bg = self.backgrounds.copy()
			for i in range(len(self.backgrounds)):
				if temp_bg[i][0] == -1:
					self.backgrounds.insert(0, self.backgrounds.pop(i))

	def bind_anim(self, entity, anim):
		"""Link the animation to the given entity."""
		self.anims[entity] = anim

	def resize_backgrounds(self, size):
		self.resized_bg.clear()
		for bg in self.backgrounds:
			current_bg = bg[1]
			if size[1]/current_bg.get_height() > size[0]/current_bg.get_width():
				self.resized_bg.append((bg[0], pygame.transform.scale(
					current_bg, (current_bg.get_width()*(size[1]/current_bg.get_height()), size[1]))))
			else:
				self.resized_bg.append((bg[0], pygame.transform.scale(
					current_bg, (size[0], current_bg.get_height() * (size[0] / current_bg.get_width())))))

	def update(self, delta: int):
		size = (
			int(math.ceil(self.wd_size[0] / self.engineCore.camera.zoom)),
			int(math.ceil(self.wd_size[1] / self.engineCore.camera.zoom)))
		rendering_surface = pygame.Surface(size)
		rendering_surface.fill((255, 255, 255))

		if self._past_zoom != self.engineCore.camera.zoom:
			self.resize_backgrounds(size)
			self._past_zoom = self.engineCore.camera.zoom

		for bg in self.resized_bg:
			self.render_background(rendering_surface, bg, size)

		self.render_layer(rendering_surface, 0, size)
		self.render_layer(rendering_surface, 1, size)

		for entity in self.engineCore.entity_manager.entities:
			self.render_entity(entity, rendering_surface, size, delta)

		self.render_particles(rendering_surface, size)

		self.render_layer(rendering_surface, 2, size)

		self.window.blit(pygame.transform.scale(rendering_surface, self.wd_size), (0, 0))

		pygame.display.update()

	def render_layer(self, surface: pygame.Surface, nbr: int, size: tuple[int, int]):
		camera_corner_x = int(self.engineCore.camera.x-size[0] * 0.5)
		camera_corner_y = int(self.engineCore.camera.y-size[1] * 0.5)

		y_camera_tile_pos = int(camera_corner_y/self.base_tile_size)
		x_camera_tile_pos = int(camera_corner_x/self.base_tile_size)

		width_tiles = int(size[0]/self.base_tile_size)+2
		height_tiles = int(size[1]/self.base_tile_size)+2

		y_render_range = y_camera_tile_pos+height_tiles

		tiles_to_render = []
		for x in range(x_camera_tile_pos, x_camera_tile_pos+width_tiles):
			for y in range(y_camera_tile_pos, y_render_range):
				tile = self.engineCore.map.get_tile_at(x, y, nbr)
				if tile:
					tiles_to_render.append((self.tiles[tile-1], (
						int(x*self.base_tile_size-camera_corner_x),
						int(y*self.base_tile_size-camera_corner_y))))
		surface.blits(tiles_to_render)

	def render_entity(self, entity, surface: pygame.Surface, size: tuple[int, int], delta: float):
		camera_corner_x = int(self.engineCore.camera.x - size[0] * 0.5)
		camera_corner_y = int(self.engineCore.camera.y - size[1] * 0.5)

		if entity.dir:
			current_frame: pygame.Surface = pygame.transform.flip(self.anims[entity].get_frame(delta), True, False)
		else:
			current_frame: pygame.Surface = self.anims[entity].get_frame(delta)

		if camera_corner_x < entity.x+current_frame.get_width() and entity.x < camera_corner_x+size[0] and\
			camera_corner_y < entity.y+current_frame.get_height() and entity.y < camera_corner_y + size[1]:
			surface.blit(current_frame, (int(entity.x-camera_corner_x), int(entity.y-camera_corner_y)))
			# for p in entity.collider_points:
			# 	surface.set_at((int(entity.x+p[0]*16-camera_corner_x), int(entity.y+p[1]*16-camera_corner_y)), (255, 0, 0))

	def render_background(self, surface: pygame.surface, bg: tuple[int, pygame.Surface], size: tuple[int, int]):
		if bg[0] == -1:
			surface.blit(bg[1], (0, 0))
		else:
			bg_width = bg[1].get_width()
			x_pos = self.engineCore.camera.x / bg[0] % bg_width
			y_pos = -(self.engineCore.camera.y-(
					self.engineCore.map.height*self.engineCore.map.base_tile_size-size[1] * 0.5))/bg[0]
			surface.blit(bg[1], (-x_pos, y_pos))
			surface.blit(bg[1], (-x_pos+bg_width, y_pos))

	def render_particles(self, surface: pygame.surface, size: tuple[int, int]):
		camera_corner_x = int(self.engineCore.camera.x - size[0] * 0.5)
		camera_corner_y = int(self.engineCore.camera.y - size[1] * 0.5)

		particles_to_render = []

		for particle_group in self.engineCore.particles_emitters_manager.particles_emitters:

			for particle in particle_group.particles:
				current_frame: pygame.Surface = particle_group.texture.get_specific_frame(particle[6])

				if camera_corner_x < particle[0] + current_frame.get_width() and \
					particle[0] < camera_corner_x + size[0] and \
					camera_corner_y < particle[1] + current_frame.get_height() and \
					particle[1] < camera_corner_y + size[1]:

					if particle_group.fade_out:
						particle_img = current_frame.copy()

						if particle[5] != 0:
							particle_img.set_alpha(255-(255*particle[5]/particle[4]))

						particles_to_render.append((particle_img, (
							int(particle[0] - camera_corner_x),
							int(particle[1] - camera_corner_y))))
					else:
						particles_to_render.append((current_frame, (
							int(particle[0] - camera_corner_x),
							int(particle[1] - camera_corner_y))))

		surface.blits(particles_to_render)
