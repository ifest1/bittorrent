from torrent_files.entity import TorrentInfo
from files.entity import File
from sessions.entity import Manager
from peers.messages import *
import socket

def main():
    torrent_info = TorrentInfo("16BF0508DEE533A5430C4AF7E5ED24889614D414.torrent")
    session = Manager(
        ports = {
            "udp_port": 6882,
            "http_port": 80
        })
    #session.create_session(torrent_info)
    #print(session)
    #print(session.get_peers_map())

    peer_example_1 = ("27.147.201.70", 63654)
    peer_example_2 = ("27.5.168.31", 12963)
    peer_example_3 = ("42.190.104.93", 24163)
    peer_example_4 = ("116.73.243.238", 57675)
    peer_example_5 = ("49.37.74.57", 61290)

    pieces = torrent_info.get_pieces()
    name = torrent_info.get_name()
    length = torrent_info.get_piece_length()

    file_description = File(name, pieces, length)
    
    print(file_description)

    print(file_description.get_piece_hash(3))

    for i in file_description.hashes:
        print(i)

    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client.settimeout(10)
    client.connect(peer_example_3)
    print("connected")
    client.send(handshake(torrent_info.get_encoded_info_hash(), session.get_encoded_peer_id()))
    print("sending handshake")
    response = client.recv(1024)
    print("waiting handshake response")
    print(response)
    client.send(interested())
    response = client.recv(1024)
    print("waiting interested response")
    print(response)
    """

main()