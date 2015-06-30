import sqlite3
from os.path import split, join, exists

_SQLITE3_CONN = None

def _stats_db():
    global _SQLITE3_CONN
    if not _SQLITE3_CONN:
        filename = join(split(__file__)[0], r'coturn_stats.db')
        _SQLITE3_CONN = _Sqlite3Connection(filename)
    return _SQLITE3_CONN

class _Sqlite3Connection(object):
    def __init__(self, filename):
        object.__init__(self)
        self._filename = filename
        self._conn = None

    @property
    def conn(self):
        if not self._conn:
            self._setup_connection()
            self._create_table()
        return self._conn

    def _setup_connection(self):
        assert(self._conn is None)
        conn = sqlite3.connect(
                self._filename, detect_types=sqlite3.PARSE_DECLTYPES)
        self._conn = conn

    def _create_table(self):
        sql = ('CREATE TABLE IF NOT EXISTS session ('
                   'id INTEGER PRIMARY KEY,'
                   'sid INTEGER,'
                   'username TEXT,'
                   'start_time TIMESTAMP,'
                   'received_packets INTEGER,'
                   'received_bytes INTEGER,'
                   'sent_packets INTEGER,'
                   'sent_bytes INTEGER,'
                   'UNIQUE (sid, username) ON CONFLICT FAIL)')
        self._conn.execute(sql)

class TurnSessionDao(object):
    def __init__(self):
        object.__init__(self)
        self._conn = _stats_db().conn

    def find_all(self):
        sql = 'SELECT * FROM session'
        return _stats_db().conn.execute(sql).fetchall()

    def save(self, session):
        return self.save_many((session,))

    def save_many(self, sessions):
        # UPSERT in SQLite
        sql = ('INSERT OR REPLACE INTO session '
            'VALUES ((SELECT id FROM session WHERE (sid=? AND username=?)),'
            '?, ?, ?, ?, ?, ?, ?)')

        def isession():
            for session in sessions:
                data = (session.sid, session.username,
                        session.sid, session.username, session.start_time,
                        session.received_packets, session.received_bytes,
                        session.sent_packets, session.sent_bytes)
                yield data

        with self._conn:
            self._conn.executemany(sql, isession())

if __name__ == '__main__':

    def main():
        from datetime import datetime, timedelta
        from model import TurnSession
        now = datetime.utcnow()
        dao = TurnSessionDao()

        session = TurnSession()

        session.sid = 1
        session.username = 'uname_1'
        session.start_time = now
        dao.save(session)

        session.sid = 2
        session.username = 'uname_2'
        dao.save(session)

        session.sid = 1
        session.username = 'uname_1'
        session.start_time += timedelta(minutes=11)

        session2 = TurnSession()
        session2.sid = 3
        session2.username = 'uname_3'
        session2.start_time = now
        dao.save_many((session, session2))

        for s in dao.find_all():
            print s

    main()
