import socket
import ssl
import time
import pickle
# from SftfConfig import SftfConfig


class SftfClientBase(object):
    """client"""


    def __init__(self):
        self.sock = socket.socket()

        self.host = None
        self.port = None
        self.timeout = 5

        self.use_ssl = False
        self.cert_file = None

        self.is_authenticated = False
        self.batch_size = 1024*1024

    def connect(self):
        if self.use_ssl:
            self.sock = ssl.wrap_socket(self.sock, server_side=False, certfile=self.cert_file)

        while 1:
            try:
                self.sock.connect((self.host, self.port))
                break
            except ConnectionRefusedError:
                print('caught <ConnectionRefusedError>')
                time.sleep(self.timeout)
        print('connected!')

    def disconnect(self):
        self.sock.close()

    def listen_manager(self):
        while 1:
            b_data = self.sock.recv(self.batch_size)

            if b_data == b'auth':
                self.sock.sendall(self.__class__.__name__.encode('utf-8'))
                self.is_authenticated = True
            else:
                if self.process_event(b_data):
                    break

    def process_event(self, data):
        try:
            event = pickle.loads(data)
        except EOFError:
            print('caught <EOFError> from pickle.loads(data)')
            return True

        if not self.is_authenticated:
            raise Exception("manager don't know who I am")
        ret = "<%s> received %s" % (self.__class__.__name__, str(event))
        print(ret)
        return False

    def run(self):
        self.connect()
        self.listen_manager()
        self.disconnect()

    @staticmethod
    def usage():
        return "\n".join([
            'stub'
        ])