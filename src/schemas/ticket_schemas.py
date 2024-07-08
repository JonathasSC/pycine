from pydantic import BaseModel


class TicketBase(BaseModel):
    ticket_id: str


class TicketCreate(TicketBase):
    seat_id: str
    person_id: str
    session_id: str
