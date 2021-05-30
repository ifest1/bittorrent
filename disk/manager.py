import os

class DiskManager():
    def __init__(self, download_folder):
        self.download_folder = download_folder

    def create_folder(self, folder):
        try: os.mkdir(self.absolute_path(folder))
        except: return -1

    def touch(file_path):
        if os.path.exists(self.absolute_path(file_path)):
            os.utime(file_path, None)
        else:
            open(file_path, 'a').close()

    def write_bytes_at_offset(file_path, offset, data):
        f = open(self.absolute_path(file_path), "r+b")
        f.seek(offset)
        f.write(data)
        f.close()

    def absolute_path(self, file_path):
        return "{}/{}".format(
            self.download_folder,
            file_path
        )



