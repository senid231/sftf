

class AbstractManager(object):
    """abstract manager"""

    def __init__(self, *args):
        """set instance variables"""
        raise NotImplementedError("%s#__init__ is not implementer" % self.__class__.__name__)

    def run(self):
        """run cases"""
        raise NotImplementedError("%s#run is not implementer" % self.__class__.__name__)

    def wait_for_connect(self):
        """wait for all clients"""
        raise NotImplementedError("%s#connect is not implementer" % self.__class__.__name__)

    def set_cases(self, cases_list):
        """add case to case list"""
        raise NotImplementedError("%s#set_cases is not implementer" % self.__class__.__name__)