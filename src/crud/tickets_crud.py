from typing import Dict, Any, List

from src.crud.base_crud import BaseCrud
from src.database.conn import Connection

from src.schemas.ticket_schemas import TicketCreate
from src.queries.tickets_queries import (
    INSERT_TICKET,
    SELECT_TICKETS_BY_PERSON_ID,
    SELECT_TICKETS_BY_ID
)


class TicketsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)
        self.conn: Connection = Connection(auto_connect=False)

    def insert_ticket(self, data: Dict[str, Any]) -> bool:
        try:
            ticket_id: str = self.uuid.smaller_uuid()
            data['ticket_id'] = ticket_id
            ticket_data: Dict[str, Any] = dict(TicketCreate(**data))
            data_list: List[Any] = list(ticket_data.values())

            self.conn.connect()
            self.conn.cursor.execute(INSERT_TICKET, data_list)
            self.conn.connection.commit()
            self.conn.close()

            return ticket_id

        except Exception as e:
            raise e

    def select_ticket_by_id(self, ticket_id):
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_TICKETS_BY_ID, [ticket_id])
            ticket: tuple = self.conn.cursor.fetchone()
            self.conn.close()
            return ticket

        except Exception as e:
            raise e

    def select_tickets_by_person_id(self, person_id):
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_TICKETS_BY_PERSON_ID, [person_id])
            tickets_list: list = self.conn.cursor.fetchall()
            self.conn.close()

            return tickets_list

        except Exception as e:
            raise e
