from connection import TurnTelnetConnection
from gateway import TurnTelnetGateway
from dao import TurnSessionDao

class TurnStatsService(object):
    def __init__(self, gateway, session_dao):
        object.__init__(self)
        self._gateway = gateway
        self._session_dao = session_dao

    def collect_session_stats(self):
        sessions = self._gateway.list_sessions()
        self._session_dao.save_many(sessions)

        for session in sessions:
            print session

def main():
    from stub.connection import TurnConnectionStub
    conn = TurnConnectionStub()
    #conn = TurnTelnetConnection()
    gateway = TurnTelnetGateway(conn)
    session_dao = TurnSessionDao()

    service = TurnStatsService(gateway, session_dao)
    service.collect_session_stats()

    conn.close()

if __name__ == '__main__':
    main()
