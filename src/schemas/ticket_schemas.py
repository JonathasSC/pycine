from pydantic import BaseModel


class TicketBase(BaseModel):
    ticket_id: str


class TicketCreate(TicketBase):
    person_id: str
    session_id: str
    seat_id: str
