from files.piece import Piece

class Files:
    def __init__(self, name, pieces_hashes, piece_length, file_size, files):
        self.name = name
        self.pieces = []
        self.files = {}
        self.file_size = file_size
        self.piece_length = piece_length
        self.set_pieces(pieces_hashes)
        self.set_files(files)
        self.pieces_amount = len(self.pieces)

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
        piece_index = 0
        bytes_counter = 0

        for _file in files:
            file_pieces = []
            file_length = _file["length"]
            file_path = _file["path"]
            
            piece_bytes_fulfillment = file_length + self.pieces[piece_index].get_byte_offset()
            pieces_amount, remaining_bytes = divmod(piece_bytes_fulfillment, self.piece_length)
            
            for index in range(pieces_amount): 
                piece = self.pieces[index]
                file_pieces.append(piece)
                bytes_counter += self.piece_length
                piece_index += 1

            if remaining_bytes: 
                current_piece_offset = self.pieces[piece_index].get_byte_offset()
                piece_bytes_fulfillment = current_piece_offset + remaining_bytes
                next_piece_offset = remaining_bytes

                if piece_bytes_fulfillment > self.piece_length:
                    next_piece_offset = piece_bytes_fulfillment % self.piece_length
                    piece_bytes_fulfillment -= next_piece_offset
                    piece = self.pieces[piece_index]
                    piece.set_byte_offset(next_piece_offset)
                    piece_index += 1

                else:
                    piece = self.pieces[piece_index]
                    next_piece_offset += piece.get_byte_offset()
                    piece.set_byte_offset(next_piece_offset)
                    file_pieces.append(piece)
                print(piece_index)
                print(file_pieces)

            self.files[tuple(file_path)] = file_pieces
