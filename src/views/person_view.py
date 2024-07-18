from src.views.base_view import BaseView
from pydantic import ValidationError


class PersonView(BaseView):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.list_options: list = [
            'Gerenciar Admins',
            'Gerenciar Clients',
            'Gerenciar Persons',
            'Voltar',
        ]

    def start(self):
        while True:
            try:
                self.terminal.clear()
                option: int = self.choose_an_option(self.list_options)

                match option:
                    case 1:
                        self.manage_admin()
                    case 2:
                        self.manage_client()
                    case 3:
                        self.manage_person()
                    case 4:
                        self.manager.admin_view.admin_flow()
                    case _:
                        self.invalid_option()
                        self.start()

            except Exception as e:
                self.printer.error(e, timer=True)

    def manage_admin(self):
        def get_all_admins():
            while True:
                try:
                    self.terminal.clear()
                    header = [
                        'PERSON ID',
                        'ADMIN ID',
                        'NAME',
                        'EMAIL',
                        'PASSWORD'
                    ]
                    admin_list: list = self.admin_crud.select_all_admins()
                    self.printer.display_table(header, admin_list)
                    self.manage_admin()

                except Exception as e:
                    self.terminal.clear()
                    self.printer.error(f'Erro ao mostrar admins {e}')
                    self.manage_admin()

        def del_admin():
            while True:
                try:
                    admin_id: str = input('Admin ID: ')
                    self.admin_crud.delete_admin(admin_id)
                    self.printer.success('Admin deletado com sucesso!')
                    self.manage_admin()

                except Exception as e:
                    self.printer.error(f'Erro ao criar sala: {e}')
                    self.manage_admin()

        def create_admin():
            while True:
                try:
                    person_id: str = input('Person ID: ')
                    self.admin_crud.insert_admin(person_id)
                    self.printer.success('Admin criado com sucesso!')
                    self.manage_admin()

                except Exception as e:
                    self.printer.error(f'Erro ao criar admin: {e}')
                    self.manage_admin()

        def put_admin():
            try:
                admin_id: str = input('Admin ID: ')
                name: str = input('Nome: ')
                email: str = input('Email: ')
                password: str = input('Senha: ')

                data: dict = {
                    'name': name,
                    'email': email,
                    'password': password
                }

                self.admin_crud.update_admin(admin_id, data)
                self.printer.success('Admin atualizado com sucesso!')
                self.manage_admin()
            except Exception as e:
                self.printer.error(f'Erro ao atualizar admin: {e}')
                self.manage_admin()

        while True:

            manage_options: list = [
                'Criar novo admin',
                'Listar admins',
                'Deletar admin',
                'Update admin',
                'Voltar'
            ]

            manage_actions = {
                1: create_admin,
                2: get_all_admins,
                3: del_admin,
                4: put_admin,
                5: self.start,
            }

            try:
                self.terminal.clear()
                option: int = self.choose_an_option(manage_options)
                self.execute_option(manage_actions, option)

            except Exception as e:
                self.printer.error(e)

    def manage_client(self):
        def get_all_clients():
            while True:
                try:
                    self.terminal.clear()
                    header = [
                        'ADMIN ID',
                        'PERSON ID',
                        'NAME',
                        'EMAIL',
                        'PASSWORD'
                    ]
                    admin_list: list = self.client_crud.select_all_clients()
                    self.printer.display_table(header, admin_list)
                    self.manage_admin()

                except Exception as e:
                    self.terminal.clear()
                    self.printer.error(f'Erro ao mostrar admins {e}')
                    self.manage_admin()

        def del_client():
            while True:
                try:
                    self.terminal.clear()
                    self.printer.generic(
                        text='Preencha os campos ou digite "q" para cancelar',
                        line=True)

                    client_id: str = input('Client ID: ')

                    if client_id.lower() == 'q':
                        break

                    confirm_delete: str = self.client_crud.delete_client(
                        client_id)

                    if client_id == confirm_delete:
                        self.terminal.clear()
                        self.printer.success('Cliente deletado com sucesso!')
                        self.terminal.clear()

                    self.manage_client()

                except Exception as e:
                    self.printer.error(f'Erro ao deletar cliente: {e}')
                    self.manage_client()

        def create_client():
            while True:
                try:
                    self.terminal.clear()
                    self.printer.generic(
                        text='Preencha os campos ou digite deixe em branco para cancelar',
                        line=True)

                    person_data: dict = self.inputs.input_person()

                    if any(value == '' for value in person_data.values()):
                        break

                    person_id: str = self.person_crud.insert_person(
                        person_data)

                    self.client_crud.insert_client(person_id)
                    self.printer.success('Admin criado com sucesso!')
                    self.manage_client()

                except ValidationError as e:
                    erro = e.errors()[0]
                    message: str = erro['msg']
                    self.printer.error(message[13:])

                except Exception as e:
                    self.printer.error(f'Erro ao criar cliente: {e}')

        while True:

            manage_options: list = [
                'Criar novo cliente',
                'Listar clientes',
                'Deletar cliente',
                'Voltar'
            ]

            manage_actions = {
                1: create_client,
                2: get_all_clients,
                3: del_client,
                4: self.start,
            }

            try:
                self.terminal.clear()
                option: int = self.choose_an_option(manage_options)
                self.execute_option(manage_actions, option)

            except Exception as e:
                self.printer.error(e)

    def manage_person(self):
        def get_all_persons():
            while True:
                try:
                    self.terminal.clear()
                    header = [
                        'PERSON ID',
                        'NAME',
                        'EMAIL',
                        'PASSWORD'
                    ]
                    admin_list: list = self.person_crud.select_all_persons()
                    self.printer.display_table(header, admin_list)
                    self.manage_admin()

                except Exception as e:
                    self.terminal.clear()
                    self.printer.error(f'Erro ao mostrar admins {e}')
                    self.manage_admin()

        def del_person():
            while True:
                try:
                    self.terminal.clear()
                    self.printer.generic(
                        text='Preencha os campos ou digite "q" para cancelar',
                        line=True)

                    person_id: str = input('Person ID: ')

                    if person_id.lower() == 'q':
                        break

                    confirm_delete: str = self.person_crud.delete_person(
                        person_id)

                    if person_id == confirm_delete:
                        self.terminal.clear()
                        self.printer.success('Pessoa deletado com sucesso!')
                        self.terminal.clear()

                    self.manage_person()

                except Exception as e:
                    self.printer.error(f'Erro ao deletar pessoa: {e}')
                    self.manage_person()

        def create_person():
            while True:
                try:
                    self.terminal.clear()
                    self.printer.generic(
                        text='Preencha os campos ou digite deixe em branco para cancelar',
                        line=True)

                    person_data: dict = self.inputs.input_person()

                    if any(value == '' for value in person_data.values()):
                        break

                    person_id: str = self.person_crud.insert_person(
                        person_data)

                    self.client_crud.insert_client(person_id)
                    self.printer.success('Admin criado com sucesso!')
                    self.manage_client()

                except ValidationError as e:
                    erro = e.errors()[0]
                    message: str = erro['msg']
                    self.printer.error(message[13:])

                except Exception as e:
                    self.printer.error(f'Erro ao criar cliente: {e}')

        while True:

            manage_options: list = [
                'Criar nova pessoa',
                'Listar pessoas',
                'Deletar pessoa',
                'Voltar'
            ]

            manage_actions = {
                1: create_person,
                2: get_all_persons,
                3: del_person,
                4: self.start,
            }

            try:
                self.terminal.clear()
                option: int = self.choose_an_option(manage_options)
                self.execute_option(manage_actions, option)

            except Exception as e:
                self.printer.error(e)

    def close(self):
        self.terminal.clear()
        self.printer.generic("Deseja realmente sair?", line=True)

        confirm_options = ['Sim', 'Não']
        option = self.choose_an_option(
            confirm_options,
            text='Escolha uma opção')

        if option == 1:
            self.terminal.clear()
            self.printer.generic('Fechado...', line=True, timer=True)
            self.terminal.clear()
        else:
            self.start()
