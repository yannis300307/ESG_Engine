from ES_Engine.core.server_client import ServerClient


class ReceivedPacket:
	def __init__(self, packet_name: str, packet_id: int, author: ServerClient | None, data: list):
		self.name = packet_name
		self.id = packet_id
		self.author = author
		self.data = data

	def __getitem__(self, item):
		return self.data[item]
