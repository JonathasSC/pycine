from src.database.conn import Connection
from src.utils.uuid import UUID
from src.utils.hashing import Hashing


class BaseCrud:
    def __init__(self, conn: Connection = None):
        self.conn = conn if conn else Connection()
        self.uuid: UUID = UUID()
        self.hash: Hashing = Hashing()
