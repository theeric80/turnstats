from os.path import split, join

class TurnConnectionStub(object):
    def close(self):
        pass

    def list_sessions(self):
        filepath = join(split(__file__)[0], 'coturn_session.log')
        with open(filepath, 'r') as fp:
            return fp.read()
