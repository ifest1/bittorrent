import socket
from urllib.parse import urlparse
from random import randrange
from struct import pack
from struct import unpack


class UDPTrackerHandler:
    def __init__(self, port):
        self.port = port
        self.connection_id = None
        self.transaction_id = None

    def request_peers(self, tracker, info_hash, peer_id):
        try:
            url = urlparse(tracker)
            url, tracker_port = url.netloc.split(':')
            tracker_port = int(tracker_port)
            client = self.open_udp_socket()      
            client.sendto(self._connect_input(), (url, tracker_port))
            response = client.recv(1024)
            if len(response) != 16: 
                return
            self.transaction_id = randrange(0, 255)
            self.connection_id = self._connect_output(response)[2]
            client.sendto(self._announce_input(info_hash, peer_id), (url, tracker_port))
            packed_peers = client.recv(1024)[20:]
            if not packed_peers: 
                return
            peers = self.get_peers_from_packet(packed_peers)
            return peers
        except Exception:
            return []

    def _announce_input(self, info_hash, peer_id):
        buf = pack('!Qii', self.connection_id, 1, self.transaction_id)
        buf += pack('!20s20sQQQ', info_hash, peer_id, 0, 0, 0)
        buf += pack("!iiiiH", 2, 0, 0, -1, self.port)
        return buf
    
    def _connect_input(self):
        return pack('!Qii', 0x41727101980, 0, randrange(0, 255))

    def _connect_output(self, packet):    
        return unpack('!iiQ', packet)

    def get_peers_from_packet(self, packed_peers):
        peers = []
        for i in range(0, len(packed_peers), 6):
            packed_ip = packed_peers[i:i+4]
            packed_port = packed_peers[i+4:i+6]
            ip = socket.inet_ntoa(packed_ip)
            port = unpack("!H", packed_port)
            if ip != "0.0.0.0": peers.append((ip, port[0]))
        return peers

    def open_udp_socket(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(0.4)
        return client