from files.piece import Piece

class FilesPieces:
    def __init__(self, name, pieces_hashes, piece_length, file_size, files):
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
                self.piece_length,
                ))
    
    def map_piece_to_file_on_disk(self, piece, file_path, bytes_range, file_disk_offset):
        piece.add_file_disk_paths(file_path, (bytes_range, file_disk_offset))
        return


    def set_files_pieces_disk_path(self, files):
        current_piece, current_file = 0, 0
        while True:
            if current_piece > self.pieces_amount - 1: break

            if current_file >= len(files): break
        
            file_path = files[current_file]["path"]
            file_length = files[current_file]["length"]
            piece = self.pieces[current_piece]
        
            pieces_amount, remaining_bytes = divmod(file_length + piece.get_byte_offset(), self.piece_length)

            if pieces_amount:
                piece_offset = piece.get_byte_offset()
                file_pieces = self.pieces[current_piece:current_piece + pieces_amount]

                for file_disk_offset in range(len(file_pieces)):
                    piece = file_pieces[file_disk_offset]
                    path = '/'.join(file_path)
                    self.map_piece_to_file_on_disk(piece, path, (piece.get_byte_offset(), self.piece_length), file_disk_offset)

                piece.set_byte_offset(self.piece_length)
                current_piece += pieces_amount
                piece = self.pieces[current_piece]
                piece.set_byte_offset(remaining_bytes)
            
            else:       
                piece_offset = piece.get_byte_offset()
                file_piece = [piece]
                piece.set_byte_offset(file_length + piece_offset)
                path = '/'.join(file_path)
                self.map_piece_to_file_on_disk(piece, path, (piece_offset, file_length + piece_offset), 0)

            current_file += 1

        for piece in self.pieces:
            for key, value in piece.disk_paths.items():
                print(key, value)
        
