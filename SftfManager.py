import sys
import socket
import ssl
import getopt
import sftf_tests
from SftfConfig import SftfConfig


class SftfManager(object):
    """Main Test manager"""

    @staticmethod
    def version():
        return 'Extended SFTF\nSIP Test Framework\nversion %s' % '0.0.1'

    @staticmethod
    def usage():
        return "\n".join([
            " ".join(['Python',  sys.version, sys.platform]),
            SftfManager.version(),
            "-h, --host - manager ip address (default listen all interfaces)",
            "-p, --port - manager port (default 9999)",
            "-c, --config - config file in ini format (default /etc/sftf/sftf.ini)",
            "-i, --interactive - interactive mode with own shell",
            "-t, --test - test class names separated with comma from test dir (conflict with -a, --all)"
            "-t, --test - all tests from test dir (conflict with -t, --test)",
            "-d, --debug - turn on debug mode",
            "-v, --version - print version and exit"
        ])

    def __init__(self):
        self.main_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.caller = None
        self.callee = None

        self.host = None
        self.port = None
        self.cfg = None

        self.is_interactive = False
        self.is_debug = False
        self.all_tests = False

        self.test_names = []

        self.use_ssl = None
        self.batch_size = 1024*1024

    def wait_for_clients(self):
        print('wait for clients')
        while 1:
            new_sock, addr = self.main_sock.accept()
            print('new connection')
            if self.use_ssl:
                new_sock - ssl.wrap_socket(new_sock, server_side=True, certfile=self.cfg.certfile, keyfile=self.cfg.keyfile)
                print('use ssl')

            if not self.auth_client(new_sock):
                print('wrong client. disconnected')
                new_sock.close()

            if self.caller is not None and self.callee is not None:
                print('caller and callee already connected')
                break
                
    def auth_client(self, sock):
        sock.sendall(b'auth')
        data = sock.recv(self.batch_size).decode('utf-8')
        
        if data == 'SftfCaller':
            self.caller = sock
            print('caller is authenticated')
            return True
        elif data == 'SftfCallee':
            self.callee = sock
            print('callee is authenticated')
            return True
        else:
            print('wrong auth response |%s|' % data)
            return False

    def apply_configurations(self):
        if self.cfg is None:
            self.cfg = SftfConfig(SftfConfig.DEFAULT_PATH)
        if self.host is None:
            self.host = self.cfg.manager_host
        if self.port is None:
            self.port = self.cfg.manager_port
        if self.use_ssl is None:
            self.use_ssl = self.cfg.use_ssl
        print('config applied')

    def disconnect(self):
        if self.caller is not None:
            self.caller.close()
            self.caller = None
            print('caller is disconnected')
        if self.caller is not None:
            self.callee.close()
            self.callee = None
            print('callee is disconnected')
        self.main_sock.close()
        print('disconnected')

    def run_case(self, case_name):
        print('run case %s' % case_name)
        eval('sftf_tests.' + case_name)(self).run()

    def start(self):
        self.apply_configurations()
        self.main_sock.bind((self.host, self.port))
        self.main_sock.listen(2)
        self.wait_for_clients()
        if len(self.test_names) == 0:
            self.disconnect()
            print(SftfManager.usage())
            sys.exit(3)
        for case in self.test_names:
            self.run_case(case)

    def start_interactive(self):
        raise Exception('<%s#start_interactive()> not implemented yet' % self.__class__.__name__)

    def run(self):
        if self.is_interactive:
            print('start interactive')
            self.start_interactive()
        else:
            print('start')
            self.start()


# ----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    manager = SftfManager()
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "h:p:c:t:aidv",
                                   ["host=", "port=", "config=", "test=", "all", "interactive", "debug", "version"])
    except getopt.GetoptError as err:
        print(err)
        print(SftfManager.usage())
        sys.exit(2)

    if len(opts) == 0 and len(args) == 0:
        print(SftfManager.usage())
        sys.exit(1)

    for o, a in opts:
        if o in ("-h", "--host"):
            manager.host = a
        elif o in ("-p", "--port"):
            manager.port = int(a)
        elif o in ("-c", "--config"):
            manager.cfg = SftfConfig(a)
        elif o in ("-t", "--test"):
            manager.test_names = a.split(',')
        elif o in ("-a", "--all"):
            manager.all_tests = True
        elif o in ("-i", "--interactive"):
            manager.is_interactive = True
        elif o in ("-d", "--debug"):
            manager.is_debug = True
        elif o in ("-v", "--version"):
            print(SftfManager.version())
            sys.exit(0)
        else:
            print("unknown option %s" % o)
            print(SftfManager.usage())
            sys.exit(2)

    if manager.all_tests and len(manager.test_names) > 0:
        print('-t|--test conflict with -a|--all')
        sys.exit(2)

    # start manager
    manager.run()