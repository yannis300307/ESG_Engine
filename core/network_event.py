class NetworkEvent:
	def __init__(self, event_id):
		self.type = event_id

	def add(self, event_buffer: list, keys: dict):
		self.__dict__.update(keys)
		event_buffer.append(self)
