from os import urandom
from binascii import b2a_hex
from binascii import a2b_hex
from peers.entity import Peer
from tracker.handler import TrackerHandler

class Manager:
    def __init__(self, **kwargs):
        self.peers_map = {}
        self.peer_id = b2a_hex(urandom(20))
        self.tracker_handler = TrackerHandler(kwargs["ports"])

    def __str__(self):
        return self.peer_id.decode()

    def __repr__(self):
        return self.__str__()
     
    def get_peers_map(self):
        return self.peers_map

    def get_peer_id(self):
        return self.peer_id

    def get_encoded_peer_id(self):
        return a2b_hex(self.peer_id)

    def create_session(self, torrent_info):
        announce_list = torrent_info.get_announce_list()
        info_hash = torrent_info.get_encoded_info_hash()
        peer_id = self.get_encoded_peer_id()

        peers = self.tracker_handler.get_peers(
                                        info_hash, 
                                        peer_id, 
                                        announce_list)

        self.peers_map[torrent_info] = [
                                Peer(peer[0], peer[1]) 
                                for peer in peers
                                ]
