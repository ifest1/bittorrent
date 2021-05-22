from random import randint
from tf_decode import info
from hashlib import sha1
from bencodepy import encode

def get_info_hash(file_path):
    return sha1(encode(info(file_path))).hexdigest()


def get_peer_id(): 
    peer_id = ""
    for _ in range(20): peer_id += chr(randint(42, 90)) 
    return peer_id.encode()

