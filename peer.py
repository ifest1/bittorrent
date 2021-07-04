import socket
from packet import Packet


class Peer:
    def __init__(self, ip, port, info_hash, peer_id):
        self.ip = ip
        self.port = int(port)
        self.info_hash = info_hash
        self.peer_id = peer_id
        self.connection = self
        self.recv_buffer = None
        self.available_pieces = []
        self.recv_size = 2**14

    def __str__(self):
        return self.ip + ":" + str(self.port)

    def __repr__(self):
        return self.__str__()

    def connect(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.ip, self.port))
        self.connection.settimeout(5)
        self.send_packet(Packet.handshake(self.info_hash, self.peer_id))

    def _close_connection(self):
        self.connection.close()

    def _send_packet(self, packet):
        self.connection.send(packet)
        size = self.recv_size
        self.recv_buffer = self.connection.recv(size)

    def _fetch_available_pieces(self):
        self.connect()
        self.send_packet()
    
    def request_block(self, piece_index, piece_offset, block_size):
        self._send_packet(Packet.request(piece_index, piece_offset, block_size))
        response = Packet.unpack(self.recv_buffer)
        return response
