from binascii import b2a_hex
from binascii import a2b_hex
from os import urandom
from consts import *
from peer import Peer
from piece import Pieces
from tracker import UDPTrackerHandler


class DownloadBuilder:
    def __init__(self, **kwargs):
        self.sessions = {}
        self.peer_id = b2a_hex(urandom(20))
        self.tracker_handler = UDPTrackerHandler(int(kwargs["udp_port"]))
        self.download_folder = kwargs["download_folder"]

    def __str__(self):
        return self.peer_id.decode()

    def __repr__(self):
        return self.__str__()

    def _set_torrent_pieces_pool(self, torrent):
        file_size = 0
        for file in torrent.files:
            file_size += file["length"]

        return Pieces(
            torrent.name, 
            torrent.pieces, 
            torrent.piece_length,  
            torrent.files,
            file_size, 
            self.download_folder)

    def _set_session_peer(self, peer, torrent, peers_ips):
        peer_ip, peer_port = peer
        if peer_ip not in peers_ips:
            print(torrent.encoded_info_hash, self.encoded_peer_id)
            peer = Peer(peer_ip, peer_port, torrent.encoded_info_hash, self.encoded_peer_id)
            self.sessions[torrent.info_hash]["peers"].append(peer)
            return peer_ip
        else:
            return None

    def _update_piece_frequency_table(self, frequency_table, peer):
        pass

    def _attach_peer_to_pieces(self, pieces, peer):
        pass

    @property
    def encoded_peer_id(self):
        return a2b_hex(self.peer_id)

    def torrent_data(self, info_hash):
        return self.sessions[info_hash]

    def init_download_session(self, torrent):
        pieces_pool = self._set_torrent_pieces_pool(torrent)

        self.sessions[torrent.info_hash] = {
            "name": torrent.name,
            "files": torrent.files,
            "piece_length": torrent.piece_length,
            "pieces_pool": pieces_pool,
            "pieces_frequency_table": {},
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
                if peer_ip:
                    peers_ips.append(peer_ip)

        for peer in self.sessions[torrent.info_hash]["peers"]:
            peer.attach_pieces(self.sessions[torrent.info_hash]["pieces_pool"])
        
        self.sessions[torrent.info_hash]["peers"][0].download_piece(0)
                
        return torrent.info_hash