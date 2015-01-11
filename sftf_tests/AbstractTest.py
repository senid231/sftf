

class AbstractTest(object):
    """abstract test case"""

    def __init__(self, *args):
        """set instance variables"""
        raise NotImplementedError("%s#__init__ is not implementer" % self.__class__.__name__)

    def run(self):
        """run case"""
        raise NotImplementedError("%s#run is not implementer" % self.__class__.__name__)