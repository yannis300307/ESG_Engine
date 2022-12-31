import json


class Map:
	"""Map object. It contans layers which contans tiles."""
	def __init__(self):
		self.layers = []
		self.width = 0
		self.height = 0
		self.spawn_x = 0
		self.spawn_y = 0
		self.base_tile_size = 16
		self.colliding_layer = 1

	def load_from_json(self, data):
		"""Load a new map using a json whish respect the correct architecture.
		You can convert a Tiled map to the correct format using the map converter."""
		map_data = json.loads(data)
		self.layers = map_data["layers"]
		self.width = map_data["width"]
		self.height = map_data["height"]

	def get_tile_at(self, x: int, y: int, layer: int):
		tile_index = x+self.width*y
		if 0 <= layer < len(self.layers) and 0 <= tile_index < len(self.layers[layer]):
			return self.layers[layer][tile_index]
		else:
			return -1
