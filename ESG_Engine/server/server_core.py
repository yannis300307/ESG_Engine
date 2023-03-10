from ESG_Engine.server.server_network import ServerNetwork
from ESG_Engine.core.engine_core import Core


class Server(Core):
	def __init__(self):
		super().__init__()
		self.network = ServerNetwork()

	def init_network(self, port: int):
		self.network.init_server(port)

	def quit(self):
		super().quit()
		self.network.close()
