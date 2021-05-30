from files.piece import Piece

class FilesPieces:
    def __init__(self, 
                name, 
                pieces_hashes, 
                piece_length, 
                file_size, 
                files):

        self.name = name
        self.pieces = []
        self.file_size = file_size
        self.piece_length = piece_length
        self.set_pieces_array(pieces_hashes)
        self.pieces_amount = len(self.pieces)
        self.set_files_pieces_disk_path(files)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def set_pieces_array(self, pieces_hashes):
        for i in range(0, len(pieces_hashes), 20):
            self.pieces.append(
                        Piece(
                        pieces_hashes[i:i+20], 
                        self.piece_length))

    def set_files_pieces_disk_path(self, files):
        current_piece, current_file = 0, 0
        
        while True:
            if current_piece > self.pieces_amount - 1: 
                break

            if current_file >= len(files): 
                break
        
            file_path = files[current_file]["path"]
            file_length = files[current_file]["length"]
            piece = self.pieces[current_piece]
        
            amount, remaining = divmod(
                                    file_length 
                                    + piece.allocated(), 
                                    self.piece_length)

            if amount:
                offset_to_write = piece.allocated()
                file_pieces = self.pieces[
                                    current_piece:current_piece 
                                    + amount]

                for file_disk_offset in range(len(file_pieces)):
                    piece = file_pieces[file_disk_offset]
                    path = '/'.join(file_path)
                    piece.add_file_disk_paths(
                                        path, 
                                        (piece.allocated(), 
                                        self.piece_length), 
                                        file_disk_offset)

                piece.alloc(self.piece_length)
                current_piece += amount
                piece = self.pieces[current_piece]
                piece.alloc(remaining)
            
            else:       
                offset_to_write = piece.allocated()
                file_piece = [piece]
                piece.alloc(file_length + offset_to_write)
                path = '/'.join(file_path)
                piece.add_file_disk_paths(
                                    path, 
                                    (offset_to_write,
                                    file_length 
                                    + offset_to_write), 
                                    0)
            current_file += 1
        
