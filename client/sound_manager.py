from pygame.mixer import Sound
import math


class SoundManager:
	def __init__(self):
		self.sounds = {}

	def register_sound(self, name: str, sound: Sound):
		"""Register the sound with the given name."""
		self.sounds[name] = sound

	def play_sound(self, sound_name: str, volume: float, pos: tuple[float | int, float | int], listening_pos: tuple[float | int, float | int]):
		"""Play the registered sound with the given name and adapts the volume using the pos and the listenning pos."""
		self.set_sound_volume(sound_name, volume, pos, listening_pos)
		self.sounds[sound_name].play()

	def set_sound_volume(self, sound_name: str, volume: float, pos: tuple[float | int, float | int], listening_pos: tuple[float | int, float | int]):
		self.sounds[sound_name].set_volume(max(0, int(volume - math.sqrt((pos[0] - listening_pos[0]) ** 2 + (pos[1] - listening_pos[1]) ** 2))) / volume)