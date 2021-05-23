class Peer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = str(port)

    def __repr__(self):
        return self.ip + ":" + self.port

    def __str__(self):
        return self.ip + ":" + self.port

    