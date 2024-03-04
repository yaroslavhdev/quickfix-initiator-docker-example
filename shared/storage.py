import psycopg2
from quickfix import MessageStore, MessageStoreFactory, SessionID

class PostgreSQLMessageStore(MessageStore):
    def __init__(self, session_id: SessionID, dbname: str, user: str, password: str, host: str, port: int):
        self.session_id = session_id
        self.connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cursor = self.connection.cursor()

        # Create message table if not exists
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                session_id TEXT,
                direction TEXT,
                message TEXT
            )
        """)
        self.connection.commit()

    def saveMessage(self, msg_seq_num: int, message: str):
        self.cursor.execute("""
            INSERT INTO messages (session_id, direction, message)
            VALUES (%s, %s, %s)
        """, (str(self.session_id), 'SENT', message))
        self.connection.commit()

    def getMessage(self, msg_seq_num: int) -> str:
        self.cursor.execute("""
            SELECT message FROM messages
            WHERE session_id = %s AND id = %s
        """, (str(self.session_id), msg_seq_num))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        return None

    def getNextSenderMsgSeqNum(self) -> int:
        self.cursor.execute("""
            SELECT MAX(id) FROM messages
            WHERE session_id = %s AND direction = 'SENT'
        """, (str(self.session_id),))
        row = self.cursor.fetchone()
        if row and row[0]:
            return row[0]
        return 1

    def getNextTargetMsgSeqNum(self) -> int:
        self.cursor.execute("""
            SELECT MAX(id) FROM messages
            WHERE session_id = %s AND direction = 'RECEIVED'
        """, (str(self.session_id),))
        row = self.cursor.fetchone()
        if row and row[0]:
            return row[0]
        return 1

    def setNextSenderMsgSeqNum(self, value: int):
        pass

    def setNextTargetMsgSeqNum(self, value: int):
        pass

class PostgreSQLMessageStoreFactory(MessageStoreFactory):
    def create(self, session_id: SessionID) -> MessageStore:
        return PostgreSQLMessageStore(session_id, 'quick_fix_initiator', 'user', 'password', 'localhost', 5432)
