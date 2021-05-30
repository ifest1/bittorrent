from files.piece import Piece
from disk.manager import DiskManager

class FilesPieces:
    def __init__(self, 
                name, 
                pieces_hashes, 
                piece_size, 
                total_size, 
                files,
                download_folder
                ):

        self.pieces = []
        self.main_folder_name = name
        self.total_size = total_size
        self.piece_size = piece_size
        self.set_pieces_array(pieces_hashes)
        self.pieces_amount = len(self.pieces)
        self.set_files_pieces_disk_path(files)
        self.disk_manager = DiskManager(download_folder)

    def __str__(self):
        return self.main_folder_name

    def __repr__(self):
        return self.__str__()

    def set_pieces_array(self, pieces_hashes):
        for i in range(0, len(pieces_hashes), 20):
            self.pieces.append(
                        Piece(
                        pieces_hashes[i:i+20], 
                        self.piece_size))

    def set_files_pieces_disk_path(self, files):
        current_piece, current_file = 0, 0
        
        while True:
            if current_piece > self.pieces_amount - 1: 
                break

            if current_file >= len(files): 
                break
        
            file_path = files[current_file]["path"]
            file_size = files[current_file]["length"]
            piece = self.pieces[current_piece]
        
            amount, remaining = divmod(
                                    file_size 
                                    + piece.allocated(), 
                                    self.piece_size)

            if amount:
                offset_to_write = piece.allocated()
                file_pieces = self.pieces[
                                    current_piece:current_piece 
                                    + amount]

                for pieces in range(len(file_pieces)):
                    piece = file_pieces[pieces]
                    path = '/'.join(file_path)
                    piece.add_file_disk_paths(
                                        path, 
                                        ((piece.allocated(), 
                                        self.piece_size), 
                                        pieces))

                current_piece += amount
                piece.alloc(self.piece_size)
                piece = self.pieces[current_piece]
                piece.alloc(remaining)
                piece.add_file_disk_paths(
                                    path,
                                    ((0,
                                    remaining),
                                    0))
            
            else:       
                offset_to_write = piece.allocated()
                piece.alloc(file_size + offset_to_write)
                path = '/'.join(file_path)
                piece.add_file_disk_paths(
                                    path, 
                                    ((offset_to_write,
                                    file_size 
                                    + offset_to_write), 
                                    0))
            current_file += 1


    def download_pieces(self):
        for piece in self.pieces:
            piece_disk_info = piece.disk_paths
            print(piece, piece_disk_info)
            #for info in piece_disk_info.items():
                #file_path = info[0]


