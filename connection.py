import telnetlib

class TurnTelnetConnection(object):
    def __init__(self, host='localhost', port=5766):
        object.__init__(self)
        self._host = host
        self._port = port
        self._tn = None

    @property
    def tn(self):
        _tn = self._tn
        if not _tn:
            _tn = telnetlib.Telnet(self._host, self._port)
            #_tn.set_debuglevel(2)
            _tn.read_very_eager()
            self._tn = _tn
        return _tn

    def close(self):
        if self._tn:
            self._tn.close()
            self._tn = None

    def list_sessions(self):
        self.tn.write("ps\n")
        return self.tn.read_very_eager()
