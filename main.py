from download_builder import DownloadBuilder
from torrent_file import TorrentInfo
from peer import Peer

def main():
    peer_test = Peer('208.78.42.32', 53206, 
                b'\x08\xad\xa5\xa7\xa6\x18:\xae\x1e\t\xd81\xdfgH\xd5f\tZ\x10',
                b'o\x03\xf0+w|\\\xa6\xd4\x82\xa0E\x80\xf1\xbe8\xa0V\x01\xa4'
                )
    torrent_info = TorrentInfo("sintel.torrent")
    builder = DownloadBuilder(udp_port="6882", download_folder="/home/iestrela/Downloads")
    pieces_pool = builder._set_torrent_pieces_pool(torrent_info)
    if not peer_test.attach_pieces(pieces_pool):
        return
    if peer_test.has_piece(626):
        peer_test.download_piece(626)
main()