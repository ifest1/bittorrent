from consts import *
from utils import is_bit_set
from connection import Connection
from packet import Packet
from logging import Log

class Peer(Connection):
    def __init__(self, ip, port, info_hash, peer_id):
        super().__init__(ip, port)
        self.info_hash = info_hash
        self.peer_id = peer_id
        self.connection = None
        self.is_available = False
        self.available_pieces = {}

    def _handshake(self):
        try:
            Log.event("Connecting to peer: {}".format(self))
            self.open_connection()
            handshake = Packet.handshake(self.info_hash, self.peer_id)
            self.send(handshake)
        except Exception as err:
            Log.event("Unable to connect due to {}: {}".format(self, err))
    
    def _interested(self):
        try:
            Log.event("Sending interested message to: {}".format(self))
            interested = Packet.interested()
            self.send(interested)
        except Exception as err:
            Log.event("Unable to interest due to {}: {}".format(self, err))
    
    def _request(self, piece_index, piece_offset, block_size):
        try:
            Log.event("Sending request block message to: {}".format(self))
            request = Packet.request(piece_index, piece_offset, block_size)
            self.send(request)
        except Exception as err:
            Log.event("Unable to request block due to {}: {}".format(self, err))
    
    def _is_piece_available(self, bitset, bit):
        return is_bit_set(bitset, bit)

    def _set_bitset_pieces(self, bitset, bitfield, pieces):
        for bit in range(8):
            if self._is_piece_available(bitfield[bitset], bit):
                curr_index = (bitset * 8) + bit
                self.available_pieces[curr_index] = pieces[curr_index]

    def _set_peer_available_pieces(self, bitfield, pieces):
        try:
            for bitset in range(len(bitfield)):
                self._set_bitset_pieces(bitset, bitfield, pieces)
        except:
            pass
    
    def has_piece(self, piece_index):
        return piece_index in self.available_pieces

    def attach_pieces(self, pieces):
        self._handshake()
        if self.recv_buffer:
            data = Packet.unpack_handshake_response(self.recv_buffer)
            self._set_peer_available_pieces(data["pieces"], pieces)
            self._interested()
            data = Packet.unpack_interested_response(self.recv_buffer)
            if Packet.MESSAGE_TYPE[data] == UNCHOKE:
                self.is_available = True
                return True
        return False
    
    def download_piece(self, piece_index):
        piece = self.available_pieces[piece_index]
        block = self._request(piece_index, 0, 2**14)
        piece.store_block(block, 0)