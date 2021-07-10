import socket

class Connection:    
    def __init__(self, ip, port):
        self.recv_buffer = b""
        self.connection = None
        self.ip = ip
        self.port = int(port)

    def __str__(self):
        return self.ip + ":" + str(self.port)

    def __repr__(self):
        return self.__str__()

    def _wait_buffer(self):
        self.recv_buffer = b""
        while True:
            recv_buffer = self.connection.recv(4096)
            print(recv_buffer)
            if not recv_buffer:
                break
            self.recv_buffer += recv_buffer

    def send(self, packet):
        self.connection.send(packet)
        self._wait_buffer()
        
    def open_connection(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.ip, self.port))

    def close_connection(self):
        self.connection.close()