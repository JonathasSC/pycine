from pydantic import BaseModel


class SessionBase(BaseModel):
    session_id: str


class SessionCreate(SessionBase):
    price: str
    room_id: str
    movie_id: str
    start_time: str

    
