import struct


class Packet:
	def __init__(self, packet_id: int, name: str, schema: str):
		self.id = packet_id
		self.data = []
		self.name = name
		self.schema = []
		for part in schema.split("-"):
			if part == "s":
				self.schema.append(0)
			elif part == "i":
				self.schema.append(1)
			elif part == "b":
				self.schema.append(2)
			elif part == "ba":
				self.schema.append(3)
			elif part == "f":
				self.schema.append(4)
			elif part == "ui":
				self.schema.append(5)

	def add_data(self, data):
		if len(data) < len(self.schema):
			raise ValueError("Too few elements in data. Please check your packet' schema.")
		elif len(data) > len(self.schema):
			raise ValueError("Too many elements in data. Please check your packet' schema.")
		for part in enumerate(self.schema):
			if part[1] == 0:
				if type(data[part[0]]) == str:
					self.data.append(data[part[0]])
				else:
					raise ValueError(str(part[0]+1) + "th element's type doesn't match with schema.")
			elif part[1] == 1:
				if type(data[part[0]]) == int:
					self.data.append(data[part[0]])
				else:
					raise ValueError(str(part[0]+1) + "th element's type doesn't match with schema.")
			elif part[1] == 2:
				if type(data[part[0]]) == bytes:
					self.data.append(data[part[0]])
				else:
					raise ValueError(str(part[0]+1) + "th element's type doesn't match with schema.")
			elif part[1] == 3:
				if type(data[part[0]]) == bytes:
					self.data.append(data[part[0]])
				else:
					raise ValueError(str(part[0]+1) + "th element's type doesn't match with schema.")
			elif part[1] == 4:
				if type(data[part[0]]) == float:
					self.data.append(data[part[0]])
				else:
					raise ValueError(str(part[0]+1) + "th element's type doesn't match with schema.")
			elif part[1] == 5:
				if type(data[part[0]]) == int and data[part[0]] >= 0:
					self.data.append(data[part[0]])
				else:
					raise ValueError(str(part[0]+1) + "th element's type or value doesn't match with schema.")

	def read_data(self, receiving_fun):
		self.data = []
		for part in self.schema:
			if part == 0:
				size = int.from_bytes(receiving_fun(4), "big")
				self.data.append(receiving_fun(size).decode())
			elif part == 1:
				self.data.append(int.from_bytes(receiving_fun(4), "big", signed=True))
			elif part == 2:
				receiving_fun(4)
			elif part == 3:
				size = int.from_bytes(receiving_fun(4), "big")
				self.data.append(receiving_fun(size))
			elif part == 4:
				self.data.append(struct.unpack("f", receiving_fun(4))[0])
			elif part == 5:
				self.data.append(int.from_bytes(receiving_fun(4), "big", signed=False))

	def get_raw_data(self):
		raw_data = b''
		for part in enumerate(self.schema):
			if part[1] == 0:
				encoded_text = self.data[part[0]].encode()
				raw_data += int.to_bytes(len(encoded_text), 4, "big")
				raw_data += encoded_text
			elif part[1] == 1:
				raw_data += int.to_bytes(self.data[part[0]], 4, "big", signed=True)
			elif part[1] == 2:
				raw_data += self.data[part[0]]
			elif part[1] == 3:
				raw_data += self.data[part[0]]
			elif part[1] == 4:
				raw_data += struct.pack("f", self.data[part[0]])
			elif part[1] == 1:
				raw_data += int.to_bytes(self.data[part[0]], 4, "big", signed=False)
		return raw_data
