

class AbstractClient(object):
    """abstract client"""

    def __init__(self, *args):
        """set instance variables"""
        raise NotImplementedError("%s#__init__ is not implementer" % self.__class__.__name__)

    def run(self):
        """start main loop and wait for messages from manager or other client"""
        raise NotImplementedError("%s#run is not implementer" % self.__class__.__name__)

    def connect(self):
        """connect to the manager"""
        raise NotImplementedError("%s#connect is not implementer" % self.__class__.__name__)

