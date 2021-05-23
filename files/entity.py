from files.piece import Piece

class File:
    def __init__(self, name, pieces_hashes, length):
        self.name = name
        self.length = length
        self.hashes = []
        self.downloaded = 0

        self.set_hashes(pieces_hashes)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def set_hashes(self, pieces_hashes):
        for i in range(0, len(pieces_hashes), 20):
            self.hashes.append(
                Piece(pieces_hashes[i:i+20])
                )

    def get_piece_hash(self, index):
        if index > self.length: return -1

        return self.hashes[index]

    