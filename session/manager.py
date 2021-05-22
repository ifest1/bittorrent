from os import urandom
from binascii import b2a_hex
from binascii import a2b_hex
from peer.entity import Peer
from tracker.handler import TrackerHandler

class Manager:
    def __init__(self, **kwargs):
        self.peers_map = {}
        self.peer_id = b2a_hex(urandom(20))
        self.tracker_handler = TrackerHandler(kwargs["ports"])

    def __repr__(self):
        return self.peer_id.decode()

    def __str__(self):
        return self.peer_id.decode()
     
    def get_peers_map(self):
        return self.peers_map

    def create_session(self, torrent_info):
        announce_list = torrent_info.get_announce_list()
        info_hash = torrent_info.get_info_hash()

        encoded_info_hash = a2b_hex(info_hash)
        encoded_peer_id = a2b_hex(self.peer_id)

        peers = self.tracker_handler.get_peers(encoded_info_hash, encoded_peer_id, announce_list)
        self.peers_map[torrent_info] = [Peer(peer[0], peer[1]) for peer in peers]
