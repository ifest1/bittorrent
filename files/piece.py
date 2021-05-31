from binascii import b2a_hex
from disk.utils import write_bytes_at_offset

class Piece:
    def __init__(self, 
                piece_hash, 
                size,
                index,
                ):

        self.index = index
        self._allocated = 0
        self.disk_paths = {}
        self.size = size
        self.downloaded = 0
        self.block_size = 2 ** 14
        self.blocks = self.size // self.block_size
        self.piece_hash = b2a_hex(piece_hash).decode()
          
    def __str__(self):
        return f"{self.piece_hash} \
        ===> {str(self.progress())}%"

    def __repr__(self):
        return self.__str__()

    def progress(self):
        return (5 / 100) * 100 # hardcoded dps faco

    def allocated(self):
        return self._allocated

    def alloc(self, allocated):
        self._allocated = allocated
    
    def add_file_disk_paths(self, file_disk_path, offsets):
        if file_disk_path not in self.disk_paths.items():
            self.disk_paths[file_disk_path] = [offsets]
            return
        
        self.disk_paths[file_disk_path] += [offsets]

    def download(self, peer, folder, name):
        piece_disk_info = self.disk_paths

        for info in piece_disk_info.items():
            file_path = info[0]
            chunks_info = info[1]
            piece_range = chunks_info[0]
            disk_offset = chunks_info[1]
            disk_offset = self.size * disk_offset

            path = "{}/{}/{}".format(
                folder,
                name,
                file_path
            )

            self.download_blocks(
                peer, path, disk_offset
            )

    def download_blocks(self, peer, path, disk_offset):
        piece_offset = 0
        
        for i in range(self.blocks):
            block = peer.request_block(
                self.index,
                piece_offset,
                self.block_size
            )

            write_bytes_on_file_at(
                path,
                disk_offset,
                block
            )

            piece_offset += self.block_size
        
    