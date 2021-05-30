import socket

class Peer:
    def __init__(self, ip, port, recv_size):
        self.ip = ip
        self.port = int(port)
        self.recv_size = self.recv_size
        self.connection = None
        self.buffer = None

    def __str__(self):
        return self.ip + ":" + self.port

    def __repr__(self):
        return self.__str__()

    def connect(self):
        conn = socket.socket(socket.AF_INET, 
                            socket.SOCK_STREAM
                            )
        conn.connect((self.ip, self.port))
        self.connection = conn

    def close_conn(self):
        self.connection.close()

    def send_packet(self, packet):
        self.connection.send(packet)
        response = self.connection.recv(self.recv_size)
        self.buffer = response

    def read_buffer(self):
        return self.buffer
        
