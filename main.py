from torrent_files.entity import TorrentInfo
from sessions.entity import Manager
from files.pieces import FilesPieces
from peers.messages import *
import socket

def main():
    torrent_info = TorrentInfo(
            "16BF0508DEE533A5430C4AF7E5ED24889614D414.torrent")
    download_folder = "/home/iestrela/Downloads"
    session = Manager(
        ports = {
            "udp_port": 6882,
            "http_port": 80
            })

    file_size = 0
    
    for f in torrent_info.get_files():
        file_size += f["length"]

    files_pieces = FilesPieces(
        torrent_info.get_name(), 
        torrent_info.get_pieces(), 
        torrent_info.get_piece_length(),  
        torrent_info.get_files(),
        file_size,
        download_folder
        )

    #files_pieces.download_all()

main()