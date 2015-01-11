

class AbstractSocketWrapper(object):
    """abstract wrapper for socket"""

    def __init__(self, sock, *args):
        """set instance variables"""
        raise NotImplementedError("%s#__init__ is not implementer" % self.__class__.__name__)

    def send(self, msg):
        """send object"""
        raise NotImplementedError("%s#send is not implementer" % self.__class__.__name__)

    def receive(self):
        """send object"""
        raise NotImplementedError("%s#receive is not implementer" % self.__class__.__name__)