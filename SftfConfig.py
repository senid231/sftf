import configparser
import sys
import os


class SftfConfig(object):
    """config"""

    DEFAULT_PATH = 'c:\\sftf.ini' if sys.platform == 'win32' else '/etc/sftf/sftf.conf'

    def __init__(self, file_path):
        if not os.path.exists(file_path):
            raise Exception("config file '%s' doesn't exist" % file_path)

        self.c = configparser.ConfigParser()
        self.c.read(file_path)

        self.manager_host = self.c.get('manager', 'host', fallback='127.0.0.1')
        self.manager_port = self.c.getint('manager', 'port', fallback=9999)
        self.use_ssl = self.c.getboolean('DEFAULT', 'use_ssl', fallback=False)
        self.batch_size = self.c.getint('DEFAULT', 'batch_size', fallback=(1024*1024))