from struct import pack
from struct import unpack


class Packet:
    @staticmethod
    def unpack(self, packet):
        pass

    @staticmethod
    def have(self, piece_index): 
        return pack("!ibi", 5, 4, piece_index)

    @staticmethod
    def request(self, piece_index, byte_offset, block_size):
        return pack("!ibiii", 13, 6, piece_index, byte_offset, block_size)
    
    @staticmethod
    def handshake(self, info_hash, peer_id): 
        return b'\x13' + b'BitTorrent protocol' + b'\00' * 8 + info_hash + peer_id

