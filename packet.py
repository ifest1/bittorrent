from struct import pack
from struct import unpack
from consts import *

class Packet:
    MESSAGE_TYPE = {
        1: UNCHOKE,
        4: HAVE,
        5: BITFIELD,
        7: PIECE
    }

    @staticmethod
    def _pieces_from_bitfield(payload, start, end):
        return unpack("!{}b".format(end-start), payload[start:end])

    @staticmethod
    def _pieces_from_have_message(payload, start, end):
        return

    def _unpack_handshake_header(payload, offset):
        offset += 28
        info_hash = unpack("!20s", payload[offset:offset+20])[0]
        offset += 20
        peer_id = unpack("!20s", payload[offset:offset+20])[0]
        offset += 20
        return (offset, peer_id, info_hash)

    def _unpack_message_header(payload, offset):
        message_len = unpack("!i", payload[offset:offset+4])[0]
        offset += 4
        message_type = unpack("!b", payload[offset:offset+1])[0]
        offset += 1
        return (offset, message_type, message_len)

    @staticmethod
    def unpack_handshake_response(payload):
        offset, peer_id, info_hash = Packet._unpack_handshake_header(payload, 0)
        data = {
            "peer_id": peer_id,
            "info_hash": info_hash,
            "pieces": [],
        }
        offset, message_type, message_len = Packet._unpack_message_header(payload, offset)
        data["pieces"] = list(Packet._pieces_from_bitfield(payload, offset, offset + message_len - 1))
        return data

    @staticmethod
    def unpack_interested_response(payload):
        offset, message_type, message_len = Packet._unpack_message_header(payload, 0)
        return message_type

    @staticmethod
    def have(piece_index): 
        return pack("!ibi", 5, 4, piece_index)

    @staticmethod
    def request(piece_index, byte_offset, block_size):
        return pack("!ibiii", 13, 6, piece_index, byte_offset, block_size)
    
    @staticmethod
    def handshake(info_hash, peer_id): 
        return b'\x13' + b'BitTorrent protocol' + b'\00' * 8 + info_hash + peer_id
    
    @staticmethod
    def interested():
        return pack("!ib", 1, 2)
