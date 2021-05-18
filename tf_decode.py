from bencodepy import decode

def get_file_data(file_path):
    fd = open(file_path, 'rb')
    data = decode(fd.read())
    fd.close()
    return data

def info(file_path):
    data = get_file_data(file_path)
    return data[b"info"]

def announce(file_path):
    data = get_file_data(file_path)
    return data[b"announce"].decode()

def announce_list(file_path):
    data = get_file_data(file_path)
    return [tracker[0].decode() for tracker in data[b"announce-list"]]

def name(file_path):
    data = get_file_data(file_path)
    return data[b"info"][b"name"].decode()

def pieces_length(file_path):
    data = get_file_data(file_path)
    return data[b"info"][b"pieces length"].decode()
    
def pieces(file_path):
    data = get_file_data(file_path)
    return data[b"info"][b"pieces"]

def files(file_path):
    data = get_file_data(file_path)
    new_files = [{key.decode() if isinstance(key, bytes) else key:
    [name.decode() for name in value] if isinstance(value, list) 
    else value for key, value in f.items()}
    for f in data[b"info"][b"files"]]

    return new_files

