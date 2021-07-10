from binascii import b2a_hex
from utils import write_bytes_at
from peer import Peer


class Piece:
    def __init__(self, piece_hash, size, index):
        self.index = index
        self._allocated = 0
        self.disk_paths = {}
        self.size = size
        self.downloaded = 0
        self.piece_hash = b2a_hex(piece_hash).decode()
          
    def __str__(self):
        return f"{self.piece_hash} ===> {str(self.progress)}%"

    def __repr__(self):
        return self.__str__()

    @property
    def progress(self):
            return (5 / 100) * 100 # hardcoded dps faco

    @property
    def allocated(self):
        return self._allocated

    def _get_file_at_piece_offset(self, piece_offset):
        pass

    def alloc(self, allocated):
        self._allocated = allocated

    def add_file_disk_paths(self, file_disk_path, offsets):
        if file_disk_path not in self.disk_paths.items():
            self.disk_paths[file_disk_path] = [offsets]
            return
        
        self.disk_paths[file_disk_path] += [offsets]

    def store_block(self, block, piece_offset):
        print(block)
        print(self.disk_paths)
        #piece_disk_info = list(self.disk_paths.items())
        #file_path = piece_disk_info[current_file][0]

        #print(piece_disk_info)
        """
        current_file = 0
        current_piece_offset = 0
        piece_disk_info = list(self.disk_paths.items())
        files_amount = len(piece_disk_info)
        while current_file < files_amount:
            piece_offset = piece_disk_info[current_file][1][0]
            file_path = piece_disk_info[current_file][0]
            disk_offset = piece_disk_info[current_file][1]
            disk_offset = self.size * disk_offset
            path = "{}/{}/{}".format(folder, name, file_path)
            self._download_block(peer, path, piece_offset, disk_offset)
            current_piece_offset += self.block_size
            if current_piece_offset not in range(piece_offset[1]):
                current_file += 1
        """

class Pieces:
    def __init__(self, name, pieces_hashes, piece_size, files, total_size, download_folder):
        self.pieces = []
        self.files = files
        self.main_folder_name = name
        self.total_size = total_size
        self.piece_size = piece_size
        self.files_amount = len(files)
        self.pieces_amount = len(self.pieces)
        self.download_folder = download_folder
        self._set_pieces_list(pieces_hashes)
        self._set_pieces_disk_path(files)
    
    def __iter__(self):
        return (piece for piece in self.pieces)

    def __getitem__(self, index):
        return self.pieces[index]

    def _set_pieces_list(self, pieces_hashes):
        index = 0
        for i in range(0, len(pieces_hashes), 20):
            self.pieces.append(Piece(pieces_hashes[i:i+20], self.piece_size, index))
            index += 1
    
    def _set_pieces_disk_path(self, files):
        current_piece, current_file = 0, 0 
        while current_piece < self.pieces_amount or current_file < self.files_amount:        
            file_path = files[current_file]["path"]
            file_size = files[current_file]["length"]
            piece = self.pieces[current_piece]
            amount, remaining = divmod(file_size + piece.allocated, self.piece_size)
            if amount:
                offset_to_write = piece.allocated
                pieces = self.pieces[current_piece:current_piece + amount]
                for piece_index in range(len(pieces)):
                    piece = pieces[piece_index]
                    path = '/'.join(file_path)
                    piece.add_file_disk_paths(path, ((piece.allocated, self.piece_size), piece_index))
                current_piece += amount
                piece.alloc(self.piece_size)
                piece = self.pieces[current_piece]
                piece.alloc(remaining)
                piece.add_file_disk_paths(path, ((0, remaining), 0))
            else:       
                offset_to_write = piece.allocated
                piece.alloc(file_size + offset_to_write)
                path = '/'.join(file_path)
                piece.add_file_disk_paths(path, ((offset_to_write, file_size + offset_to_write), 0))
            current_file += 1
    