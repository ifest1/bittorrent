from struct import pack
from struct import unpack

class Packets:
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
    
    @staticmethod
    def unpack_incoming_packet(self, packet):
        if len(packet) == 4: 
            return 'KEEP_ALIVE'

        packet_type = self.packet_types[packet[4]]
        
        if packet_type == "PIECE":
            length = unpack("!i", packet[0:3])
            length -= 9
            index, begin = unpack("!ii", packet[5:13])
            
            # now unpack block To Do

    @staticmethod
    def have(self, piece_index): 
        return pack("!ibi", 
                    5, 
                    4, 
                    piece_index
                    )

    @staticmethod
    def request(self, 
                piece_index, 
                byte_offset, 
                block_size):

        pack = pack("!ib", 13, 6)
        pack += pack("!iii", 
                    piece_index, 
                    byte_offset, 
                    block_size
                    )
        return pack
    
    @staticmethod
    def handshake(self, 
            info_hash, 
            peer_id): 
        pack = b'\x13'
        pack += b'BitTorrent protocol'
        pack += b'\00' * 8
        pack += info_hash
        pack += peer_id
        return pack    

