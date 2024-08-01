import os
import json
from typing import Optional
from src.utils.uuid import UUID
from src.crud.persons_crud import PersonsCrud


class Token:
    def __init__(self) -> None:
        self.token_file = 'token.json'
        self.uuid: UUID = UUID()
        self.persons_crud: PersonsCrud = PersonsCrud()

    def create_token(self) -> str:
        self.logger.info('CRIANDO TOKEN')
        return self.uuid.smaller_uuid()

    def create_token_map(self, person_id: str) -> str:
        token: str = self.create_token()

        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as file:
                token_map = json.load(file)
        else:
            token_map = {}

        token_map[token] = person_id

        with open(self.token_file, 'w') as file:
            json.dump(token_map, file)

        self.logger.info('CRIANDO MAPEAMENTO DE TOKEN')
        return token

    def delete_token(self) -> None:
        if os.path.exists(self.token_file):
            os.remove(self.token_file)
        self.logger.info('DELETANDO TOKEN DE AUTENTICAÇÃO')

    def person_id_from_token(self, token: str) -> Optional[str]:
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as file:
                token_map = json.load(file)
            return token_map.get(token)
        return None

    def load_token(self) -> Optional[str]:
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as file:
                token_map = json.load(file)
                if token_map:
                    self.logger.info('CARREGANDO TOKEN DE AUTENTICAÇÃO')
                    return list(token_map.keys())[0]

        return None

    def get_role_from_token(self, token: str) -> Optional[str]:
        person_id = self.person_id_from_token(token)
        if person_id:
            self.logger.info('SELECIONANDO PESSOA POR TOKEN')
            return self.persons_crud.get_person_role(person_id)
        return None
