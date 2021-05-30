from binascii import b2a_hex

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
        self.blocks = []
        self.downloaded = 0
        self.block_size = 2 ** 14
        self.piece_hash = b2a_hex(piece_hash)\
                                    .decode()
          
    def __str__(self):
        return f"{self.piece_hash} \
        ===> {str(self.progress())}%"

    def __repr__(self):
        return self.__str__()

    def progress(self):
        return (5 / 100) * 100

    def allocated(self):
        return self._allocated

    def alloc(self, allocated):
        self._allocated = allocated
    
    def add_file_disk_paths(self, 
                            file_disk_path, 
                            offsets
                            ):

        if file_disk_path not in self.disk_paths.items():
            self.disk_paths[file_disk_path] = [offsets]
            return
        
        self.disk_paths[file_disk_path] += [offsets]

    def download_piece(self):
        piece_disk_info = self.disk_paths

        for info in piece_disk_info.items():
            file_path = info[0]
            chunks_info = info[1]
            piece_range = chunks_info[0]
            disk_offset = chunks_info[1]
            self.download_blocks()

    # downloads blocks in paralell
    def download_blocks(self):
        piece_offset = 0
        blocks = self.size // self.block_size
        
        for i in range(blocks):
            packet = Packets.request(
                                    self.index,
                                    piece_offset,
                                    self.block_size
                                    )

            response = self.request_block(packet)
            block = Packets.unpack_incoming_packet(response)
            # now store block (To Do)

            piece_offset += self.block_size
        
    