from torrent_files.entity import TorrentInfo
from files.entity import Files
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

    pieces = torrent_info.get_pieces()
    name = torrent_info.get_name()
    piece_length = torrent_info.get_piece_length()
    files = torrent_info.get_files()
    file_size = 0


    for f in files:
        file_size += f["length"]


    files_manager = Files(name, pieces, piece_length, file_size, files)








    """
    session.create_session(torrent_info)
    print(session)
    print(session.get_peers_map())

    peer_example_1 = ("27.147.201.70", 63654)
    peer_example_2 = ("27.5.168.31", 12963)
    peer_example_3 = ("42.190.104.93", 24163)
    peer_example_4 = ("116.73.243.238", 57675)
    peer_example_5 = ("49.37.74.57", 61290)

    print(files_manager.get_pieces())
    print(files_manager.get_pieces_amount())
    print(files_manager.get_piece(3658))
    print(files_manager.get_files())
    print(files)
    print(files_manager)
    print(files_manager.get_piece_hash(3))

    virtual_f_size = files_manager.get_pieces_amount() * files_manager.get_piece_length()
    print(files_manager.get_pieces_amount())
    print(virtual_f_size, files_manager.get_piece_length())
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(10)
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