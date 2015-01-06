import pickle


class TestBase(object):
    """Abstract Test Class for SFTF SIP Framework"""

    def __init__(self, manager):
        self.manager = manager
        self.a = manager.caller
        self.b = manager.callee

    def run(self):
        print('start processing %s#run()' % self.__class__.__name__)
        self._run()
        print('end processing %s#run()' % self.__class__.__name__)

    def _run(self):
        raise Exception('override me!')

    # requests
    def send_request(self, who, args=None):
        args = {} if args is None else args

        if who == self.a:
            who_name = 'caller'
        elif who == self.b:
            who_name = 'callee'
        else:
            who_name = 'unknown'

        args.update({'request': True, 'who': who_name})
        data = pickle.dumps(args)
        print("<%s> send request to %s with args=%s" % (self.__class__.__name__, who_name, str(args)))
        print("data=%s" % str(pickle.loads(data)))
        who.sendall(data)

    def send_invite_request(self, who, args=None):
        args = {} if args is None else args

        args.update({'type': 'INVITE'})
        self.send_request(who, args)

    def send_reinvite_request(self, who, args=None):
        args = {} if args is None else args

        args.update({'type': 'RE-INVITE'})
        self.send_request(who, args)

    def send_bye_request(self, who, args=None):
        args = {} if args is None else args

        args.update({'type': 'BYE'})
        self.send_request(who, args)

    # responses
    def send_response(self, who, args=None):
        args = {} if args is None else args

        if who == self.a:
            who_name = 'caller'
        elif who == self.b:
            who_name = 'callee'
        else:
            who_name = 'unknown'

        args.update({'response': True, 'who': who_name})
        data = pickle.dumps(args)
        print("<%s> send response to %s with args=%s" % (self.__class__.__name__, who_name, str(args)))
        print("data=%s" % str(pickle.loads(data)))
        who.sendall(data)

    def accept_invite(self, who, args=None):
        args = {} if args is None else args

        args.update({'type': 'ACK INVITE'})
        self.send_response(who, args)

    def accept_bye(self, who, args=None):
        args = {} if args is None else args

        args.update({'type': 'ACK BYE'})
        self.send_response(who, args)

    def cancel_invite(self, who, args=None):
        args = {} if args is None else args

        args.update({'type': 'C INVITE'})
        self.send_response(who, args)

    def cancel_bye(self, who, args=None):
        args = {} if args is None else args

        # todo check if it possible to cancel bye
        args.update({'type': 'C BYE'})
        self.send_response(who, args)

    def end_test(self):
        print("<%s> end test" % self.__class__.__name__)