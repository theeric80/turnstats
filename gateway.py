import re
from datetime import datetime, timedelta
from model import TurnSession

class TurnTelnetGateway(object):
    def __init__(self, connection):
        object.__init__(self)
        self._connection = connection
        self._setup_patterns()

    def list_sessions(self):
        response = self._connection.list_sessions()
        return self._build_sessions(response)

    def _setup_patterns(self):
        _ = re.compile
        self._session_pat = r'(\d+)[)] id=(\d+), user <(\S+?)>:'
        self._session_regex = _(self._session_pat)
        self._realm_regex = _('realm: (\S+)')
        self._origin_regex = _('origin: (\S+)')
        self._start_time_regex = _('started (\d+) secs ago')
        self._expiration_time_regex = _('expiring in (\d+) secs')
        self._protocol_regex = _('client protocol (\S+), relay protocol (\S+)')
        self._usage_regex = _('usage: rp=(\d+), rb=(\d+), sp=(\d+), sb=(\d+)')
        self._rate_regex = _('rate: r=(\d+), s=(\d+), total=(\d+)')

    def _build_sessions(self, string):
        sessions = []
        pat = self._session_pat + r'(.*?)(\r?\n){2}'
        regex = re.compile(pat, re.DOTALL)
        for m in regex.finditer(string):
            session = self._build_session(m.group())
            if not session: continue
            sessions.append(session)
        return sessions

    def _build_session(self, string):
        match = self._session_regex.search(string)
        if not match: return None

        seq, sid, username = match.groups()
        session = TurnSession()
        session.sid = int(sid)
        session.username = username

        now = datetime.utcnow()

        self._build_realm(string, session)
        self._build_origin(string, session)
        self._build_start_time(string, now, session)
        self._build_expiration_time(string, now, session)
        self._build_protocol(string, session)
        self._build_usage(string, session)
        self._build_rate(string, session)

        return session

    def _build_realm(self, string, session):
        match = self._realm_regex.search(string)
        if not match: return
        session.realm, = match.groups()

    def _build_origin(self, string, session):
        match = self._origin_regex.search(string)
        if not match: return
        session.origin, = match.groups()

    def _build_start_time(self, string, now, session):
        match = self._start_time_regex.search(string)
        if not match: return
        session.start_time = now - timedelta(seconds=int(match.group(1)))

    def _build_expiration_time(self, string, now, session):
        match = self._expiration_time_regex.search(string)
        if not match: return
        session.expiration_time = now + timedelta(seconds=int(match.group(1)))

    def _build_protocol(self, string, session):
        match = self._protocol_regex.search(string)
        if not match: return
        session.client_protocol, session.peer_protocol = match.groups()

    def _build_usage(self, string, session):
        match = self._usage_regex.search(string)
        if not match: return
        session.received_packets, session.received_bytes, \
                session.sent_packets, session.sent_bytes \
                = [int(m) for m in match.groups()]

    def _build_rate(self, string, session):
        match = self._rate_regex.search(string)
        if not match: return
        session.received_rate, session.sent_rate, \
                session.total_rate = [int(m) for m in match.groups()]

if __name__ == '__main__':
    def main():
        from stub.connection import TurnConnectionStub

        conn = TurnConnectionStub()
        gateway = TurnTelnetGateway(conn)
        for session in gateway.list_sessions():
            print session
        conn.close()

    main()
