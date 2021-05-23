from files.piece import Piece

class Files:
    def __init__(self, name, pieces_hashes, piece_length, files):
        self.name = name
        self.hashes = []
        self.files = {}
        self.downloaded = 0
        self.total_size = 0
        self.piece_length = piece_length
        self.set_files(files)
        self.set_pieces(pieces_hashes)
        self.pieces_amount = len(self.hashes)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_piece_hash(self, index):
        if index > self.pieces_amount: return -1

        return self.hashes[index]

    def get_files(self):
        return self.files

    def get_pieces_amount(self):
        return self.pieces_amount

    def get_piece_length(self):
        return self.piece_length

    def set_total_size(self):
        for file_ in self.files:
            self.total_size += file_["length"]

    def set_pieces(self, pieces_hashes):
        index = 0
        for i in range(0, len(pieces_hashes), 20):
            self.hashes.append(
                Piece(pieces_hashes[i:i+20], self.piece_length, index)
                )
            i += 1

    def set_files(self, files):
        pass