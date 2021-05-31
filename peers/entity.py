from peers.messages import Packets
import socket

class Peer:
    def __init__(self, ip, port, recv_size):
        self.ip = ip
        self.port = int(port)
        self.connection = None
        self.recv_buffer = None
        self.available_pieces = []
        self.recv_size = self.recv_size

    def __str__(self):
        return self.ip + ":" + self.port

    def __repr__(self):
        return self.__str__()

    def fetch_available_pieces(self):
        self.connect()
        self.send_packet()
    
    def request_block(self, piece_index, 
                    piece_offset, block_size):
        self.send_packet(Packets.request(
            piece_index, 
            piece_offset, 
            block_size
        ))
        
        block = Packets.unpack_incoming_packet(
            self.recv_buffer
        )

        return block

    def connect(self, info_hash, peer_id):
        self.connection = socket.socket(
            socket.AF_INET, 
            socket.SOCK_STREAM
        )

        self.connection.connect((
            self.ip, self.port
        ))

        self.connection.settimeout(5)
        self.send_packet(Packets.handshake(
            info_hash, peer_id
        ))

    def close_conn(self):
        self.connection.close()

    def send_packet(self, packet):
        self.connection.send(packet)
        size = self.recv_size
        self.recv_buffer = self.connection.recv(size)
