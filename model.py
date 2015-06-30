
# struct turn_session_info
class TurnSession(object):
    def __init__(self):
        object.__init__(self)
        self.sid = 0
        self.username = ''
        self.start_time = None
        self.expiration_time = None
        self.client_protocol = ''
        self.peer_protocol = ''

        # Stats
        self.received_packets = 0
        self.received_bytes = 0
        self.received_rate = 0
        self.sent_packets = 0
        self.sent_bytes = 0
        self.sent_rate = 0
        self.total_rate = 0

        # Realm
        self.realm = ''
        self.origin = ''

    def __repr__(self):
        result = (
            'sid: {0}\n'
            'username: {1}\n'
            'realm: {2}\n'
            'origin: {3}\n'
            'start_time: {4}\n'
            'expiration_time: {5}\n'
            'client_protocol: {6}\n'
            'peer_protocol: {7}\n'
            'received_packets: {8}\n'
            'received_bytes: {9}\n'
            'sent_packets: {10}\n'
            'sent_bytes: {11}\n'
            'received_rate: {12}\n'
            'sent_rate: {13}\n'
            'total_rate: {14}\n'.format(
            self.sid, self.username,
            self.realm,
            self.origin,
            self.start_time,
            self.expiration_time,
            self.client_protocol,
            self.peer_protocol,
            self.received_packets,
            self.received_bytes,
            self.sent_packets,
            self.sent_bytes,
            self.received_rate,
            self.sent_rate,
            self.total_rate))
        return result
