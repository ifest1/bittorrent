from tracker.udp import UDPTrackerHandler
from urllib.parse import urlparse

class TrackerHandler:
    def __init__(self, ports):
        self.announce_list = []
        self.udp_port = ports["udp_port"]
        self.http_port = ports["http_port"]
        self.udp_tracker_handler = UDPTrackerHandler(ports["udp_port"])
        self.http_tracker_handler = None

    def get_peers(self, info_hash, peer_id, announce_list):
        peers = []
        for tracker in announce_list:
            if self.tracker_type(tracker) == 'udp':
                temp = self.udp_tracker_handler.request_peers(tracker, info_hash, peer_id)
                if temp and len(temp) > len(peers): peers = temp
        return peers

    def tracker_type(self, announce):
        url = urlparse(announce) 
        return url.scheme

