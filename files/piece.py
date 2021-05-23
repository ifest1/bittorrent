from binascii import b2a_hex

class Piece:
    def __init__(self, piece_hash):
        self.piece_hash = b2a_hex(piece_hash).decode()
        self.downloaded = 0
        self.size_bytes = 0

    def __repr__(self):
        return self.piece_hash
    
    def __str__(self):
        return self.piece_hash


        

