from ES_Engine.server.server_network import ServerNetwork
from ES_Engine.core.engineCore import Core


class Server(Core):
	def __init__(self):
		super().__init__()
		self.network = ServerNetwork()

	def init_network(self, port: int):
		self.network.init_server(port)

	def quit(self):
		super().quit()
		self.network.close()
