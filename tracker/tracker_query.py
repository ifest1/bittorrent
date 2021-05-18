from random import randbytes
from tf_decode import info
from hashlib import sha1

from bencodepy import encode
from dotenv import dotenv_values

def get_info_hash(file_path):
    info_hash = sha1(encode(info(file_path)))
    return info_hash.hexdigest().encode()

def get_port():
    config = dotenv_values(".env")
    return config['PORT']

def get_uploaded():
    return 0

def get_downloaded():
    return 0

def get_left():
    return 0

def get_compact():
    return 0

def get_no_peer_id():
    return 1

def get_event():
    return 2

def get_peer_id():
    return randbytes(20)