from typing import Dict, Any, List

from src.crud.base_crud import BaseCrud
from src.database.conn import Connection

from src.schemas.ticket_schemas import TicketCreate
from src.queries.tickets_queries import INSERT_TICKET


class TicketsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)
        self.conn: Connection = Connection(auto_connect=False)

    def insert_ticket(self, data: Dict[str, Any]) -> bool:
        try:
            ticket_id: str = self.uuid.smaller_uuid()
            data['ticket_id'] = ticket_id
            session_data: Dict[str, Any] = dict(TicketCreate(**data))
            data_list: List[Any] = list(session_data.values())

            self.conn.cursor.execute(INSERT_TICKET, data_list)
            self.conn.connection.commit()
            self.conn.close()

            return ticket_id

        except Exception as e:
            raise e
