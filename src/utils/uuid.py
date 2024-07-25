from uuid import uuid4


class UUID:
    def __init__(self) -> None:
        pass

    def smaller_uuid(self) -> str:
        uuid: str = str(uuid4())
        return uuid.split('-')[0]
