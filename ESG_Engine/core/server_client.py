class ServerClient:
	def __init__(self, sock, id_):
		self.sock = sock
		self.id = id_

	def send_data(self, data):
		self.sock[0].sendall(data)

	def recv_bytes(self, byte_nbr):
		return self.sock[0].recv(byte_nbr)

	def close(self):
		self.sock[0].close()
