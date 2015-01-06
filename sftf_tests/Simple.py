from .TestBase import TestBase


class Simple(TestBase):
    """Simple Test"""

    def _run(self):
        self.send_invite_request(self.a)
        self.accept_invite(self.b)
        self.send_bye_request(self.a)
        self.accept_bye(self.b)

        self.end_test()