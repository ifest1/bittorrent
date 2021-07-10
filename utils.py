import os

def create_folder(file_path):
    try: 
        os.mkdir(file_path)
    except: 
        return -1

def touch(file_path):
    if os.path.exists(file_path):
        os.utime(file_path, None)
    else:
        open(file_path, 'a').close()

def write_bytes_at(file_path, offset, bytes):
    f = open(file_path, "r+b")
    f.seek(offset)
    f.write(bytes)
    f.close()

def is_bit_set(x, n):
    return x & 1 << n != 0