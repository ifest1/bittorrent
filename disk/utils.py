import os

def create_folder(file_path):
    try: 
        os.mkdir(file_path)
    except: 
        return -1

def touch(file_path):
    if os.path.exists(file_path):
        os.utime(path, None)
    else:
        open(file_path, 'a').close()

def write_bytes_on_file_at(file_path, 
                        offset, data):
    f = open(file_path, "r+b")
    f.seek(offset)
    f.write(data)
    f.close()

