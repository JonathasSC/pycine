from src.crud.rooms_crud import RoomsCrud
from src.crud.seats_crud import SeatsCrud


def maximum_room_capacity(room_id: str):
    seats_count = SeatsCrud().count_seats_by_room_id(room_id)
    room: str = RoomsCrud().select_room_by_id(room_id)
    room_dimensions: int = room[2] * room[3]

    if room_dimensions <= seats_count:
        return True
    return False
