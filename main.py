from client import Client
from torrent_file import TorrentInfo


def main():
    torrent_info = TorrentInfo("C6AB766D2A1A4DF2BC6AEB8FA6094837C0613DCB.torrent")
    session = Client(udp_port="6882", download_folder="/home/iestrela/Downloads")
    info_hash = session.create_download_session(torrent_info)
    print(info_hash)
main()