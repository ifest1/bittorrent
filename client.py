from binascii import b2a_hex
from binascii import a2b_hex

from os import urandom
from peer import Peer
from piece import PiecesPool
from tracker import UDPTrackerHandler


class Client:
    def __init__(self, **kwargs):
        self.sessions = {}
        self.peer_id = b2a_hex(urandom(20))
        self.tracker_handler = UDPTrackerHandler(int(kwargs["udp_port"]))
        self.download_folder = kwargs["download_folder"]

    def __str__(self):
        return self.peer_id.decode()

    def __repr__(self):
        return self.__str__()
    
    @property
    def encoded_peer_id(self):
        return a2b_hex(self.peer_id)

    def _set_torrent_pieces_pool(self, torrent):
        file_size = 0
        for file in torrent.files:
            file_size += file["length"]
        return PiecesPool(
            torrent.name, 
            torrent.pieces, 
            torrent.piece_length,  
            torrent.files,
            file_size, self.download_folder)

    def _set_session_peer(self, peer, torrent, peers_ips):
        peer_ip, peer_port = peer
        if peer_ip not in peers_ips:
            self.sessions[torrent.info_hash]["peers"].append(
                Peer(peer_ip, peer_port, torrent.info_hash, self.peer_id))
        return peer_ip
        
    def create_download_session(self, torrent):
        self.sessions[torrent.info_hash] = {
            "name": torrent.name,
            "files": torrent.files,
            "piece_length": torrent.piece_length,
            "pieces": self._set_torrent_pieces_pool(torrent),
            "peers": [],
        }
        peers_ips = []
        for tracker in torrent.announce_list:
            response = self.tracker_handler.request_peers(
                tracker, torrent.encoded_info_hash, self.encoded_peer_id)
            if not response:
                continue
            for peer in response:
                peer_ip = self._set_session_peer(peer, torrent, peers_ips)
                peers_ips.append(peer_ip)
        return torrent.info_hash

    def torrent_data(self, info_hash):
        return self.sessions[info_hash]