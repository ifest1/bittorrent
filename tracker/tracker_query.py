from random import randint
from tf_decode import info
from hashlib import sha1
from bencodepy import encode
import os, binascii

def get_info_hash(file_path):
    return sha1(encode(info(file_path))).hexdigest()


def get_peer_id(): 
    return binascii.b2a_hex(os.urandom(20))
