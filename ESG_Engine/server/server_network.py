from ESG_Engine.core.network import Network
from threading import Thread

from ESG_Engine.core.network_event import NetworkEvent
from ESG_Engine.core.received_packet import ReceivedPacket
from ESG_Engine.core.server_client import ServerClient
from ESG_Engine.core.packet import Packet
import socket


class ServerNetwork(Network):
	def __init__(self):
		super().__init__()
		self._server_clients = []
		self.last_id = 0

	def init_server(self, port: int):
		"""Init the network for server side."""
		if not self._network_type:
			self._network_type = 1
			self._log("Initialising Server ...")
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.bind(("", port))
			self.socket.listen()
			Thread(target=self.__accepting_server_thread).start()
			self._log("Server initialised !")
		else:
			raise ConnectionError("Network already initialised !")

	def get_clients(self):
		return self._server_clients.copy()

	def server_send_packet_to_client(self, client: ServerClient, packet_name: str, data: list):
		if self._network_type == 1:
			packet_info = self._packets_id[self._packet_names[packet_name]]
			packet = Packet(packet_info[0], packet_info[1], packet_info[2])
			packet.add_data(data)
			try:
				client.send_data(packet.id.to_bytes(4, "big") + packet.get_raw_data())
			except ConnectionError:
				NetworkEvent(CLIENT_QUIT_EVENT).add(self._event_buffer, {"client": client})
				self._server_clients.remove(client)
			self._log("Sended " + packet.name + " to " + client.sock[1][0] + ".", 2)
		else:
			raise PermissionError("Network not initialised.")

	def close(self):
		for client in self._server_clients:
			client.close()
		self.socket.close()
		super().close()

	def __accepting_server_thread(self):
		while True:
			try:
				client = ServerClient(self.socket.accept(), self.last_id)
				self.last_id += 1
				self._server_clients.append(client)
				self._log("Added new player at " + client.sock[1][0])
				NetworkEvent(CLIENT_CONNECTION_EVENT).add(self._event_buffer, {"client": client})
				Thread(target=lambda: self.__listening_client_server_thread(client)).start()
			except OSError:
				break

	def __listening_client_server_thread(self, client):  # Server side
		while True:
			try:
				raw_packet_id = client.recv_bytes(4)
				if not raw_packet_id:
					NetworkEvent(CLIENT_QUIT_EVENT).add(self._event_buffer, {"client": client})
					self._server_clients.remove(client)
					break
				packet_id = int.from_bytes(raw_packet_id, "big")
				packet_info = self._packets_id[packet_id]
				packet = Packet(packet_id, packet_info[1], packet_info[2])
				packet.read_data(client.recv_bytes)
				received_packet = ReceivedPacket(packet.name, packet.id, client, packet.data)
				self._log("Received " + packet.name + " from " + client.sock[1][0] + ".", 2)
				self.received_packet_buffer.append(received_packet)
			except OSError:
				NetworkEvent(CLIENT_QUIT_EVENT).add(self._event_buffer, {"client": client})
				self._server_clients.remove(client)
				break
