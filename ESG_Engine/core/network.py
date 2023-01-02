from ESG_Engine.core.constants import NORMAL_LOG
from ESG_Engine.core.network_event import NetworkEvent
from ESG_Engine.core.received_packet import ReceivedPacket


class Network:
	"""Network object which can be used to create easily a client or a server."""
	def __init__(self):
		self._packets_id = {}
		self._packet_names = {}
		self.last_id = 0
		self.socket = None
		self.received_packet_buffer = []
		self._network_type = 0  # 0 : nothing; 1 : server; 2 : client
		self.log = NORMAL_LOG
		self._event_buffer = []

	def _log(self, text, lvl=1):
		if self.log >= lvl:
			print(text)

	def get_state(self):
		return self._network_type

	def get_events(self) -> list[NetworkEvent]:
		events = []
		while len(self._event_buffer) != 0:
			events.append(self._event_buffer.pop())
		return events

	def close(self):
		self._log("Network closed !")

	def get_packets(self) -> list[ReceivedPacket]:
		"""Return received packet for iterations."""
		packets = []
		while len(self.received_packet_buffer) != 0:
			packets.append(self.received_packet_buffer.pop())
		return packets

	def register_new_packet(self, name: str, schema: str):
		"""Register new Packet schema.
		schema if a string wich contan the data in the packet with letters separated with "-" caractere.
		s : string (preceded by an int which indicate the string len);
		i : int;
		ui : unsigned int;
		b : byte;
		f : float;
		ba : byte array (preceded by an int which indicate the string len);
		You must use it like this : \"i-s-b-ba-f\""""
		self._packets_id[self.last_id] = [self.last_id, name, schema]
		self._packet_names[name] = self.last_id
		self.last_id += 1
		self._log("Registered new packet " + name + " !")
