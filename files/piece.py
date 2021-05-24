from binascii import b2a_hex

class Piece:
    def __init__(self, 
                piece_hash, 
                length):

        self.byte_offset = 0
        self.piece_hash = b2a_hex(piece_hash).decode()
        self.length = length

    def __repr__(self):
        return f"{self.piece_hash} ===> {str(self.progress())}%"
    
    def __str__(self):
        return f"{self.piece_hash} ===> {str(self.progress())}%"

    def progress(self):
        return (self.byte_offset // self.length) * 100

    def set_byte_offset(self, byte_offset):
        self.byte_offset = byte_offset

    def get_byte_offset(self):
        return self.byte_offset