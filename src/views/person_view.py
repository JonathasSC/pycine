from pydantic import ValidationError
from src.views.base_view import BaseView
from src.utils.validators import exists_email, password_validator


class PersonView(BaseView):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.list_options: list = [
            'Gerenciar Admins',
            'Gerenciar Clients',
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
                        self.manager.admin_view.admin_flow()
                    case _:
                        self.invalid_option()
                        self.start()

            except Exception as e:
                self.printer.error(e, timer=True)

    def manage_admin(self):
        def get_admins() -> None:
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

        def del_admin() -> None:
            while True:
                try:
                    token: str = self.token.load_token()

                    admin_id: str = input('Admin ID: ')
                    admin: tuple = self.admin_crud.select_by_id(admin_id)

                    person_id: str = admin[1]
                    my_person_id: str = self.token.person_id_from_token(token)

                    if person_id == my_person_id:
                        self.terminal.clear()

                        self.printer.warning('CUIDADO!', timer=False)

                        self.printer.generic(
                            'Você está tentando deletar sua própria conta.'
                        )
                        self.printer.generic(
                            'Isso resultará na perda permanente do seu acesso ao sistema e o logout automático.'
                        )
                        self.printer.generic(
                            'Por favor, confirme se realmente deseja proceder com esta ação.'
                        )

                        confirm_options = ['Sim']
                        option = self.choose_an_option(
                            confirm_options,
                            text='Realmente deseja deletar sua própria conta?',
                            cancel=True)

                        if option and option == 1:
                            self.admin_crud.delete_admin(admin_id)
                            self.printer.success('Admin deletado com sucesso!')

                            self.logout()
                            self.manager.home_view.start()

                        else:
                            self.terminal.clear()
                            self.printer.success('Operação cancelada!')
                            self.manage_admin()

                except Exception as e:
                    self.printer.error(f'Erro ao criar sala: {e}')
                    self.manage_admin()

        def crt_admin() -> None:
            while True:
                try:
                    self.terminal.clear()
                    self.printer.generic(
                        text='Preencha os campos ou digite "q" para cancelar',
                        line=True)

                    person_data: dict = self.inputs.input_person()

                    if not person_data:
                        self.terminal.clear()
                        self.printer.success('Operação cancelada!')
                        self.manage_admin()

                    person_id: str = self.person_crud.insert_person(
                        person_data)

                    self.admin_crud.insert_admin(person_id)
                    self.printer.success('Admin criado com sucesso!')
                    self.manage_admin()

                except ValidationError as e:
                    erro = e.errors()[0]
                    message: str = erro['msg']
                    self.printer.error(message[13:])

                except Exception as e:
                    self.printer.error(f'Erro ao criar admin: {e}')

        def put_admin() -> None:
            while True:
                try:
                    old_data = {}
                    data = {}

                    self.terminal.clear()
                    self.printer.generic(
                        'Digite o Admin ID, ou "q" para cancelar', line=True)
                    admin_id: str = input('Admin ID: ').strip().lower()

                    if admin_id == 'q':
                        self.manage_admin()

                    admin = self.admin_crud.select_by_id(admin_id)

                    if not admin:
                        self.terminal.clear()
                        self.printer.error(
                            'Nenhum admin identificado, tente novamente')
                        self.terminal.clear()
                        put_admin()

                    person = self.person_crud.select_by_id(admin[1])

                    old_data['name'] = person[1]
                    old_data['email'] = person[2]
                    old_data['password'] = person[3]

                    name = input(
                        'Nome (deixe em branco para manter o atual): ').strip()
                    email = input(
                        'Email (deixe em branco para manter o atual): ').strip()
                    password = input(
                        'Senha (deixe em branco para manter a atual): ').strip()

                    while email and not exists_email(email):
                        self.terminal.clear()
                        self.printer.error('Esse email já está em uso')
                        self.terminal.clear()

                        email = input('Email: ').strip()

                    while password and not password_validator(password):
                        self.terminal.clear()
                        self.printer.password_params()
                        self.terminal.clear()

                        password = input('Senha: ').strip()

                    if not name:
                        data['name'] = old_data['name']
                    else:
                        data['name'] = name

                    if not email:
                        data['email'] = old_data['email']
                    else:
                        data['email'] = email

                    if not password:
                        data['password'] = old_data['password']
                    else:
                        data['password'] = self.hash.generate_hash(
                            password
                        )

                    if data:
                        self.admin_crud.update_admin(admin_id, data)
                        self.printer.success('Admin atualizado com sucesso!')
                    else:
                        self.printer.info(
                            'Nenhum dado fornecido para atualização.')

                except ValueError as e:
                    self.terminal.clear()
                    self.printer.error(f'{e}')
                    self.terminal.clear()
                    self.put_admin()

                except Exception as e:
                    self.printer.error(f'Erro ao atualizar admin: {e}')
                    self.put_admin()

                finally:
                    self.manage_admin()

        while True:

            manage_options: list = [
                'Criar novo admin',
                'Listar admins',
                'Deletar admin',
                'Atualizar admin',
                'Voltar'
            ]

            try:
                self.terminal.clear()
                option: int = self.choose_an_option(manage_options)

                match option:
                    case 1:
                        crt_admin()
                    case 2:
                        get_admins()
                    case 3:
                        del_admin()
                    case 4:
                        put_admin()
                    case 5:
                        self.manager.person_view.start()
                    case _:
                        self.invalid_option()
                        self.manager.person_view.start()

            except Exception as e:
                self.printer.error(e)

    def manage_client(self) -> None:
        def get_all_clients() -> None:
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

        def del_client() -> None:
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

        def crt_client() -> None:
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

        def put_client() -> None:
            while True:
                try:
                    old_data = {}
                    data = {}

                    self.terminal.clear()
                    self.printer.generic(
                        'Digite o Client ID, ou "q" para cancelar', line=True)
                    client_id: str = input('Client ID: ').strip().lower()

                    if client_id == 'q':
                        self.manage_client()

                    client: tuple = self.client_crud.select_by_id(client_id)

                    if not client:
                        self.terminal.clear()
                        self.printer.error(
                            'Nenhum cliente identificado, tente novamente')
                        self.terminal.clear()
                        put_client()

                    person = self.person_crud.select_by_id(client[1])

                    old_data['name'] = person[1]
                    old_data['email'] = person[2]
                    old_data['password'] = person[3]

                    name = input(
                        'Nome (deixe em branco para manter o atual): ').strip()
                    email = input(
                        'Email (deixe em branco para manter o atual): ').strip()
                    password = input(
                        'Senha (deixe em branco para manter a atual): ').strip()

                    while email and not exists_email(email):
                        self.terminal.clear()
                        self.printer.error('Esse email já está em uso')
                        self.terminal.clear()

                        email = input('Email: ').strip()

                    while password and not password_validator(password):
                        self.terminal.clear()
                        self.printer.password_params()
                        self.terminal.clear()

                        password = input('Senha: ').strip()

                    if not name:
                        data['name'] = old_data['name']
                    else:
                        data['name'] = name

                    if not email:
                        data['email'] = old_data['email']
                    else:
                        data['email'] = email

                    if not password:
                        data['password'] = old_data['password']
                    else:
                        data['password'] = self.hash.generate_hash(
                            password
                        )

                    if data:
                        self.client_crud.update_client(client_id, data)
                        self.printer.success('Cliente atualizado com sucesso!')
                    else:
                        self.printer.info(
                            'Nenhum dado fornecido para atualização.')

                except ValueError as e:
                    self.terminal.clear()
                    self.printer.error(f'{e}')
                    self.terminal.clear()
                    self.put_admin()

                except Exception as e:
                    self.printer.error(f'Erro ao atualizar cliente: {e}')
                    self.put_client()

                finally:
                    self.manage_client()

        while True:

            manage_options: list = [
                'Criar novo cliente',
                'Listar clientes',
                'Deletar cliente',
                'Atualizar cliente',
                'Voltar'
            ]

            try:
                self.terminal.clear()
                option: int = self.choose_an_option(manage_options)

                match option:
                    case 1:
                        crt_client()
                    case 2:
                        get_all_clients()
                    case 3:
                        del_client()
                    case 4:
                        put_client()
                    case 5:
                        self.manager.person_view.start()
                    case _:
                        self.invalid_option()
                        self.manager.person_view.start()

            except Exception as e:
                self.printer.error(e)

    def close(self) -> None:
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
