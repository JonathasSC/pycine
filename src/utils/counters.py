from src.crud.rooms_crud import RoomsCrud


def room_dimensions(room_id: str):
    room: str = RoomsCrud().select_by_room_id(room_id)
    room_dimensions: int = room[2] * room[3]
    return room_dimensions
