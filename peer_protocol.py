from struct import pack
from tracker.tracker_query import get_peer_id
from tracker.tracker_query import get_info_hash
from dotenv import dotenv_values

config = dotenv_values(".env")
file_path = config["FILE"]

# peer handshake
def handshake(info_hash, peer_id): 
    req = b'\x13'
    req += b'BitTorrent protocol'
    req += info_hash
    req += peer_id
    return req

# ==========================================================================================
# downloading messages
def keep_alive(): return pack("!i", 0)
def choke_peer(): return pack("!ib", 1, 0)
def unchoke_peer():  return pack("!ib", 1, 1)
def interested(): return pack("!ib", 1, 2)
def not_interested(): return pack("!ib", 1, 3)
def have(piece_index): return pack("!ibi", 5, 4, piece_index)
def request(piece_index,byte_offset, block_length=2**14): 
    return pack("!ibiii", 13, 6, piece_index, byte_offset, block_length) 

# ==========================================================================================

# seeding messages