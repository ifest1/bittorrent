from struct import pack

class Packet:
    def __init__(self):
        self.packet_types = [
            "CHOKE",
            "UNCHOKE",
            "INTERESTED",
            "NOT_INTERESTED",
            "HAVE",
            "BITFIELD",
            "REQUEST",
            "PIECE",
            "CANCEL",
            "PORT",
        ]

    def handshake(self, info_hash, peer_id): 
        pack = b'\x13'
        pack += b'BitTorrent protocol'
        pack += b'\00' * 8
        pack += info_hash
        pack += peer_id
        return pack

    def have(self, piece_index): 
        return pack("!ibi", 5, 4, piece_index)

    def request(self, piece_index, byte_offset, block_length):
        pack = pack("!ib", 13, 6)
        pack += pack("!iii", piece_index, byte_offset, block_length)
        return pack

    def unpack_incoming_packet(self, packet):
        if len(packet) == 4: return 'KEEP_ALIVE'
        return self.packet_types[packet[5]]
            

    