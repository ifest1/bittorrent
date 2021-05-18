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
    url = urlparse(url)
    url, port = url.netloc.split(':')
    port = int(port)

    packet = udp_tracker_connect_input()

    try:
        client = udp_socket_open(url, port)
        
        client.sendto(packet, (url, port))
        response = client.recv(1024)
        
        if response and len(response) == 16: 
            connection_id = udp_tracker_connect_output(response)[2]

            transaction_id =  randrange(0, 255)
            packet = udp_announce_input(file_path, connection_id, transaction_id)
            client.sendto(packet, (url, port))

            response = client.recv(1024)

            packed_peers = response[20:]
            
            peers = []

            if packed_peers:

                i = 0

                while True:
                    
                    if i + 6 <= len(packed_peers):
                        ip, port = unpack_peers_address(packed_peers[i:i+6])
                        peers += (ip, port)                      
                        i += 6
                    
                    else: break
            
            print(peers)

            return peers

    except Exception as e:
        pass

def udp_tracker_connect_input():
    action, transaction_id, connection_id = 0, randrange(0, 255), 0x41727101980
    return pack('!qii', connection_id, action, transaction_id)

def udp_tracker_connect_output(packet):    
    return unpack('!iiq', packet)


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

    return pack('!qii20s20sqqqiiiih',
                connection_id,
                action,
                transaction_id,
                info_hash,
                peer_id,
                downloaded,
                left,
                uploaded,
                event,
                ip,
                key,
                num_want,
                port)

def unpack_peers_address(packet):
    port = unpack("!h", packet[4:])
    ip = socket.inet_ntoa(packet[:4])
    return ip, port 
