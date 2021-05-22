from torrent_file.info import TorrentInfo
from session.manager import Manager

import socket

def main():
    torrent_info = TorrentInfo("16BF0508DEE533A5430C4AF7E5ED24889614D414.torrent")
    session_test = Manager(ports={"udp_port": 6882, "http_port": 80})
    session_test.create_session(torrent_info)
    print(session_test)
    print(session_test.get_peers_map())
main()