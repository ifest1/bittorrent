import sys

class Log:
    @staticmethod
    def event(message):
        sys.stdout.write("\r\x1b[K"+message.__str__())
        sys.stdout.flush()

