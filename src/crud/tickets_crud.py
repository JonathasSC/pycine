from typing import Dict, Any, List, Optional, Tuple

from src.crud.base_crud import BaseCrud
from src.database.conn import Connection

from src.queries.tickets_queries import (
    INSERT_TICKET,
    DELETE_TICKET_BY_ID,
    SELECT_TICKETS_BY_ID,
    SELECT_TICKETS_BY_PERSON_ID,
)
from src.schemas.ticket_schemas import TicketCreate


class TicketsCrud(BaseCrud):
    def __init__(self, conn: Connection = None):
        super().__init__(conn)
        self.logger.info('INSTANCIA TICKETS CRUD CRIADA')

    def insert_ticket(self, data: Dict[str, Any]) -> Optional[str]:
        try:
            ticket_id: str = self.uuid.smaller_uuid()
            data['ticket_id'] = ticket_id
            ticket_data: Dict[str, Any] = dict(TicketCreate(**data))
            data_list: List[Any] = list(ticket_data.values())

            self.conn.connect()
            self.conn.cursor.execute(INSERT_TICKET, data_list)
            self.conn.connection.commit()
            self.conn.close()

            self.logger.info('INSERIDO TICKET')
            return ticket_id

        except Exception as e:
            raise e

    def select_ticket_by_id(self, ticket_id) -> Optional[tuple]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_TICKETS_BY_ID, [ticket_id])
            ticket: tuple = self.conn.cursor.fetchone()
            self.conn.close()

            self.logger.info('SELECIONADO TICKET POR ID')
            return ticket

        except Exception as e:
            raise e

    def select_tickets_by_person_id(self, person_id) -> Optional[List[Tuple[str]]]:
        try:
            self.conn.connect()
            self.conn.cursor.execute(SELECT_TICKETS_BY_PERSON_ID, [person_id])
            tickets_list: list = self.conn.cursor.fetchall()
            self.conn.close()

            self.logger.info('SELECIONADO TICKETS POR PERSON ID')
            return tickets_list

        except Exception as e:
            raise e

    def delete_ticket_by_id(self, ticket_id: str) -> Optional[Tuple[str]]:
        try:
            if not self.select_ticket_by_id(ticket_id):
                raise ValueError('Nenhum ticket com esse ID foi encontrado.')

            self.conn.connect()
            self.conn.cursor.execute(DELETE_TICKET_BY_ID, [ticket_id])
            self.conn.connection.commit()
            self.conn.close()

            return ticket_id
        except Exception as e:
            raise e
