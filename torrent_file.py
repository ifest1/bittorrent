from bencodepy import encode
from bencodepy import decode
from binascii import a2b_hex
from hashlib import sha1

class TorrentInfo:
    def __init__(self, file_path):
        self.data = self.decode(file_path)
        self.hash = sha1(encode(self.data["info"])).hexdigest()
    
    @property
    def dictionary(self):
        return self.data

    @property
    def name(self):
        return self.data["name"]

    @property
    def files(self):
        return self.data["files"]

    @property
    def info_hash(self):
        return self.hash

    @property
    def encoded_info_hash(self):
        return a2b_hex(self.hash)

    @property
    def info(self):
        return self.data["info"]

    @property
    def pieces(self):
        return self.data["pieces"]

    @property
    def announce_list(self):
        return self.data["announce_list"]

    @property
    def piece_length(self):
        return self.data["piece_length"]
    
    def __hash__(self):
        return hash(self.info_hash)

    def __eq__(self, other):
        return self.info_hash == other.get_info_hash()

    def __str__(self):
        return self.info_hash

    def __repr__(self):
        return self.__str__()

    def decode(self, file_path):
        torrent_info = {}

        fd = open(file_path, 'rb')
        data = decode(fd.read())
        fd.close()
        
        torrent_info["info"] = data[b"info"]
        torrent_info["pieces"] = data[b"info"][b"pieces"]
        torrent_info["name"] = data[b"info"][b"name"].decode()
        torrent_info["piece_length"] = data[b"info"][b"piece length"]
        torrent_info["announce_list"] = [
            tracker[0].decode() for tracker in data[b"announce-list"]
        ]
        torrent_info["files"] = [
            {key.decode() if isinstance(key, bytes) else 
            key: [name.decode() for name in value] if 
            isinstance(value, list) else value 
            for key, value in f.items()}
            for f in data[b"info"][b"files"]
        ]
        return torrent_info