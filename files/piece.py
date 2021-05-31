from binascii import b2a_hex
from disk.utils import write_bytes_on_file_at

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
        piece_disk_info = self.disk_paths.items()
        size = len(piece_disk_info)
        piece_offset = piece_disk_info[0][1][0][0]
        current_file = 0
        next_file = True

        while True:
            if current_file == size: 
                break

            if next_file:
                info = piece_disk_info[current_file]
                file_path = info[0]
                chunks_info = info[1]
                piece_range = chunks_info[0]
                disk_offset = chunks_info[1]
                disk_offset = self.size * disk_offset
                path = "{}/{}/{}".format(
                    folder, name, file_path
                )
                next_file = False

            self.download_block(
                peer, path, disk_offset
            )
            piece_offset += self.block_size

            if piece_offset not in range(piece_range):
                current_file += 1
                next_file = True

    def download_block(self, peer, path, disk_offset):
        block = peer.request_block(
            self.index,
            piece_offset,
            self.block_size
        )

        write_bytes_on_file_at(
            path, disk_offset,
            block
        )

        
    