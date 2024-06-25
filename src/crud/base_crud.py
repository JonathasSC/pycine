from src.database.conn import Connection
from src.utils.uuid import UUID
from src.utils.hashing import Hashing


class BaseCrud:
    def __init__(self, conn: Connection = Connection()):
        self.conn = conn
        self.uuid: UUID = UUID()
        self.hash: Hashing = Hashing()
