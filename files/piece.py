from binascii import b2a_hex

class Piece:
    def __init__(self, 
                piece_hash, 
                length):

        self.byte_offset = 0
        self.disk_paths = {}
        self.length = length
        self.piece_hash = b2a_hex(piece_hash).decode()
        
    
    def __str__(self):
        return f"{self.piece_hash} ===> {str(self.progress())}%"

    def __repr__(self):
        return self.__str__()

    def progress(self):
        return (self.byte_offset // self.length) * 100

    def get_byte_offset(self):
        return self.byte_offset

    def set_byte_offset(self, byte_offset):
        self.byte_offset = byte_offset
    
    def add_file_disk_paths(self, file_disk_path, offsets):

        if file_disk_path not in self.disk_paths.items():
            self.disk_paths[file_disk_path] = [offsets]
            return
        
        self.disk_paths[file_disk_path] += [offsets]
