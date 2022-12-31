from ESG_Engine.core.network import Network
from threading import Thread
from ESG_Engine.core.packet import Packet
from ESG_Engine.core.received_packet import ReceivedPacket

import socket


class ClientNetwork(Network):
	def __init__(self):
		super().__init__()

	def init_client(self, address: str, port: int):
		"""Init the network for client side."""
		if not self._network_type:
			self._network_type = 2
			self._log("Initialising Client ...")
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.connect((address, port))
			Thread(target=self.__receiving_server_client_thread).start()
			self._log("Client initialised !")
		else:
			raise ConnectionError("Network already initialised !")

	def client_send_packet_to_server(self, packet_name: str, data: list):
		"""[Client-Side only !] Send packet to the server when the network is configured as a client."""
		if self._network_type == 2:
			packet_info = self._packets_id[self._packet_names[packet_name]]
			packet = Packet(packet_info[0], packet_info[1], packet_info[2])
			packet.add_data(data)
			self.socket.sendall(packet.id.to_bytes(4, "big") + packet.get_raw_data())
		else:
			raise PermissionError("Network not initialised.")

	def close(self):
		self.socket.close()
		super().close()

	def __receiving_server_client_thread(self):  # client side
		while True:
			try:
				raw_packet_id = self.socket.recv(4)
				if not raw_packet_id:
					self.close()
					break
				packet_id = int.from_bytes(raw_packet_id, "big")
				packet_info = self._packets_id[packet_id]
				packet = Packet(packet_id, packet_info[1], packet_info[2])
				packet.read_data(self.socket.recv)
			except ConnectionError:
				self.close()
				break
			received_packet = ReceivedPacket(packet.name, packet.id, None, packet.data)
			self._log("Received " + packet.name + " from server.", 2)
			self.received_packet_buffer.append(received_packet)
