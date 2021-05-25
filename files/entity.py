from files.piece import Piece

class Files:
    def __init__(self, name, pieces_hashes, piece_length, file_size, files):
        self.name = name
        self.pieces = []
        self.files = {}
        self.file_size = file_size
        self.piece_length = piece_length
        self.set_pieces(pieces_hashes)
        self.pieces_amount = len(self.pieces)
        self.set_files(files)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_piece(self, index):
        if index > self.pieces_amount: 
            return -1

        return self.pieces[index]

    def get_pieces(self):
        return self.pieces

    def set_pieces(self, pieces_hashes):
        for i in range(0, len(pieces_hashes), 20):
            self.pieces.append(
                Piece(
                pieces_hashes[i:i+20], 
                self.piece_length,
                ))
    
    def set_files(self, files):
        current_piece, current_file = 0, 0
        while True:
            if current_piece == self.pieces_amount-1: break

            file_path = files[current_file]["path"]
            file_length = files[current_file]["length"]
            piece = self.pieces[current_piece]
        
            pieces_amount, remaining_bytes = divmod(file_length + piece.get_byte_offset(), self.piece_length)

            if pieces_amount:
                piece_offset = piece.get_byte_offset()
                file_pieces = self.pieces[current_piece:current_piece + pieces_amount]
                piece.set_byte_offset(0)
                self.files[tuple(file_path)] = (self.pieces[current_piece].get_byte_offset(), file_pieces)
                current_piece += pieces_amount
                piece = self.pieces[current_piece]
                piece.set_byte_offset(remaining_bytes)
            
            else:
                piece_offset = piece.get_byte_offset()
                
                if (file_length + piece_offset) > self.piece_length:
                    file_pieces = self.pieces[current_piece: current_piece + 1]
                    self.files[tuple(file_path)] = (piece_offset, file_pieces)
                    piece.set_byte_offset(0)
                    current_piece += 1
                    piece = self.pieces[current_piece]
                    piece.set_byte_offset((file_length + piece_offset) % self.piece_length)

                elif (file_length + piece_offset) == self.piece_length:
                    file_piece = [piece]
                    piece.set_byte_offset(0)
                        
                else:
                    file_piece = [piece]
                    piece.set_byte_offset(file_length + piece_offset)

                    self.files[tuple(file_path)] = (piece_offset, file_piece)

            current_file += 1
           
        for key, value in self.files.items():
            print(key, value)
