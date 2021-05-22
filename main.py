from tracker.udp_tracker.udp_tracker_request import udp_tracker_request_peers

from tracker.tracker_query import get_info_hash
from tracker.tracker_query import get_peer_id
from tf_decode import announce_list
from peer_protocol import handshake
from url import tracker_type

from dotenv import dotenv_values
from binascii import a2b_hex

import socket

config = dotenv_values(".env")

def main():
    file_path = config["FILE"]
    port = config["PORT"]
    port = int(port)
    peers = []

    peer_id = a2b_hex(get_peer_id())
    info_hash = a2b_hex(get_info_hash(file_path))
    """
    tracker_list = announce_list(file_path)
    
    for tracker in tracker_list:
        if tracker_type(tracker) == 'udp':
            temp = udp_tracker_request_peers(tracker, file_path, peer_id, info_hash, port)
            if len(temp) > len(peers): peers = temp
    """
    #print("trying to connect to -->" + peer[0] + ":" + str(peer[1]))
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client.settimeout(0.5)
    client.connect(("37.239.210.155", 31606))
    client.send(handshake(info_hash, peer_id))
    response = client.recv(1024)
    print(response)
    client.close()

main()