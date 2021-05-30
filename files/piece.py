from binascii import b2a_hex

class Piece:
    def __init__(self, 
                piece_hash, 
                length):
        
        self._allocated = 0
        self.disk_paths = {}
        self.length = length
        self.blocks = []
        self.downloaded_bytes = 0
        self.piece_hash = b2a_hex(piece_hash).decode()
          
    def __str__(self):
        return f"{self.piece_hash} ===> {str(self.progress())}%"

    def __repr__(self):
        return self.__str__()

    def progress(self):
        return (self.downloaded_bytes // self._allocated) * 100

    def allocated(self):
        return self._allocated

    def alloc(self, allocated):
        self._allocated = allocated
    
    def add_file_disk_paths(self, file_disk_path, offsets):
        if file_disk_path not in self.disk_paths.items():
            self.disk_paths[file_disk_path] = [offsets]
            return
        
        self.disk_paths[file_disk_path] += [offsets]

    def store_piece_on_disk(self):
        pass

    def request_block(self):
        pass

    def piece_blocks(self):
        pass

    