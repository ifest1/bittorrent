import socket

from urllib.parse import urlparse
from urllib.parse import unquote

from random import randrange

from struct import pack
from struct import unpack

from tracker.tracker_query import *

def udp_socket_open(url, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(0.4)

    return client

def udp_tracker_request_peers(url, file_path):
    try:
        url = urlparse(url)
        url, port = url.netloc.split(':')
        port = int(port)

        packet = udp_tracker_connect_input() 
        client = udp_socket_open(url, port)        
        client.sendto(packet, (url, port))
        
        response = client.recv(1024)
        
        if len(response) != 16: return

        connection_id, transaction_id = udp_tracker_connect_output(response)[2], randrange(0, 255)
        client.sendto(udp_announce_input(file_path, connection_id, transaction_id), (url, port))
        packed_peers = client.recv(1024)[20:]
        
        if not packed_peers: return
        
        peers = [(socket.inet_ntoa(packed_peers[i:i+4]), 
        unpack("!h", packed_peers[i+4:i+6])) for i in range(0, len(packed_peers), 6)]

        print(peers)
        return peers

    except Exception as e:
        pass

def udp_tracker_connect_input():
    action, transaction_id, connection_id = 0, randrange(0, 255), 0x41727101980
    buf = pack('!qii', connection_id, action, transaction_id)
    return buf
def udp_tracker_connect_output(packet):    
    buf = unpack('!iiq', packet)
    return buf

def udp_announce_input(file_path, connection_id, transaction_id):
    action = 1
    info_hash = get_info_hash(file_path)
    peer_id = get_peer_id()
    downloaded = get_downloaded()
    left = get_left()
    uploaded = get_uploaded()
    event = get_event()
    ip = 0
    key = 0
    num_want = -1
    port = int(get_port())

    buf = pack('!qii', connection_id, action, transaction_id)
    buf += pack('!20s20sqqq', info_hash, peer_id, downloaded, left, uploaded)
    buf += pack("!iiiih",event, ip, key, num_want, port)

    return buf
