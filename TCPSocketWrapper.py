import pickle
import struct
import socket
from . import AbstractSocketWrapper


class TCPSocketWrapper(AbstractSocketWrapper):
    """abstract wrapper for socket"""

    def __init__(self, sock, *args):
        self.sock = sock
        self.is_closed = False
        self.is_timeout = False

    def set_timeout(self, seconds):
        self.sock.settimeout(seconds)

    def send(self, data):
        message = pickle.dumps(data)
        size = struct.pack('>I', len(message))
        self.sock.sendall(size + message)

    def receive(self):
        raw_size = self.receive_all(4)
        if raw_size is None:
            return None
        size = struct.unpack('>I', raw_size)[0]
        raw_data = self.receive_all(size)
        data = pickle.loads(raw_data)
        return data

    def receive_all(self, size):
        self.is_closed = False
        self.is_timeout = False
        data = ''
        while len(data) < size:
            try:
                packet = self.sock.recv(size - len(data))
            except socket.timeout:
                self.is_timeout = True
                return None
            except OSError:
                self.is_closed = True
                return None

            if not packet:
                self.is_closed = True
                return None
            data += packet
        return data