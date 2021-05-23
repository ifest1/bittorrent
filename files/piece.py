from binascii import b2a_hex

class Piece:
    def __init__(self, 
                piece_hash, 
                length, 
                index, 
                current_offset):

        self.piece_hash = b2a_hex(piece_hash).decode()
        self.current_offset = current_offset
        self.length = length
        self.index = index

    def __repr__(self):
        return f"[{self.index}]:{self.piece_hash} ===> {str(self.progress())}%"
    
    def __str__(self):
        return f"[{self.index}]:{self.piece_hash} ===> {str(self.progress())}%"

    def progress(self):
        return (self.current_offset // self.length) * 100

    def get_current_offset(self):
        return self.current_offset

    def update_offset(self, block_size):
        self.current_offset += self.block_size
