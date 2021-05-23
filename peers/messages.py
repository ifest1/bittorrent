from struct import pack

def handshake(info_hash, peer_id): 
    req = b'\x13'
    req += b'BitTorrent protocol'
    req += b'\00' * 8
    req += info_hash
    req += peer_id
    return req

def keep_alive(): return pack("!i", 0)

def choke(): return pack("!ib", 1, 0)

def unchoke():  return pack("!ib", 1, 1)

def interested(): return pack("!ib", 1, 2)

def not_interested(): return pack("!ib", 1, 3)

def have(piece_index): return pack("!ibi", 5, 4, piece_index)

def request(piece_index, byte_offset, block_length=2**14): 
    return pack("!ibiii", 13, 6, piece_index, byte_offset, block_length) 
