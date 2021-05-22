from tracker.udp_tracker.udp_tracker_request import udp_tracker_request_peers
from tracker.tracker_query import get_info_hash
from tracker.tracker_query import get_peer_id
from tf_decode import announce_list
from dotenv import dotenv_values
from url import tracker_type

config = dotenv_values(".env")

def main():
    file_path = config["FILE"]
    port = config["PORT"]
    port = int(port)

    peer_id = get_peer_id()
    info_hash = get_info_hash(file_path)
    tracker_list = announce_list(file_path)
    
    for tracker in tracker_list:
        if tracker_type(tracker) == 'udp':
            udp_tracker_request_peers(tracker, file_path, peer_id, info_hash, port)

main()