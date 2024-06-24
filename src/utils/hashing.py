import bcrypt


class Hashing:
    def generate_hash(self, text: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(text.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_hash(self, text: str, hashed: str) -> bool:
        return bcrypt.checkpw(text.encode('utf-8'), hashed.encode('utf-8'))
