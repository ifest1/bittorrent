import socket
from urllib.parse import urlparse
from urllib.parse import unquote
from random import randrange
from struct import pack
from struct import unpack

def udp_tracker_request_peers(url, file_path, peer_id, info_hash, port):
    try:
        url = urlparse(url)
        url, tracker_port = url.netloc.split(':')
        tracker_port = int(tracker_port)

        packet = udp_tracker_connect_input()
        client = udp_socket_open(url, tracker_port)        
        client.sendto(packet, (url, tracker_port))
        
        response = client.recv(1024)
        
        if len(response) != 16: return
        
        connection_id, transaction_id = udp_tracker_connect_output(response)[2], randrange(0, 255)
        
        client.sendto(udp_announce_input(file_path, connection_id, transaction_id, peer_id, info_hash, port), (url, tracker_port))
        packed_peers = client.recv(1024)[20:]
        
        if not packed_peers: return
        
        peers = []

        for i in range(0, len(packed_peers), 6):
            packed_ip = packed_peers[i:i+4]
            packed_port = packed_peers[i+4:i+6]

            ip = socket.inet_ntoa(packed_ip)
            port = unpack("!H", packed_port)
            
            peers.append((ip, port[0]))
 
        return peers

    except Exception as e:
        return []

def udp_announce_input(file_path, connection_id, transaction_id, peer_id, info_hash, port):
    buf = pack('!Qii', connection_id, 1, transaction_id)
    buf += pack('!20s20sQQQ', info_hash, peer_id, 0, 0, 0)
    buf += pack("!iiiiH", 2, 0, 0, -1, port)
    return buf

def udp_tracker_connect_input():
    action, transaction_id, connection_id = 0, randrange(0, 255), 0x41727101980
    buf = pack('!Qii', connection_id, action, transaction_id)
    return buf

def udp_tracker_connect_output(packet):    
    buf = unpack('!iiQ', packet)
    return buf

def udp_socket_open(url, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(0.4)
    return client
