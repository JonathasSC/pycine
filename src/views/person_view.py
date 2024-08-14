from pydantic import ValidationError
from src.views.base_view import BaseView
from typing import Optional


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
                    self.terminal.clear()
                    email: str = input('Email: ').strip()

                    if email.lower() == 'q':
                        self.printer.warning(
                            'Exclusão de admin cancelada', clear=True)
                        self.manage_admin()

                    admin: tuple = self.admin_crud.select_by_email(email)
                    if not admin:
                        self.printer.warning(
                            'Nenhum admin com esse email encontrado', clear=True)
                        self.manage_admin()

                    admin_id: str = admin[0]
                    person_id: str = admin[1]

                    my_person_id: str = self.token.person_id_from_token(token)

                    confirm_options = ['Sim']
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

                        option = self.choose_an_option(
                            confirm_options,
                            text='Realmente deseja deletar sua própria conta?',
                            cancel=True)

                        if option and option == 1:
                            self.admin_crud.delete_admin(admin_id)
                            self.printer.success(
                                'Admin deletado com sucesso!', clear=True)

                            self.logout()
                            self.manager.home_view.start()

                        else:
                            self.terminal.clear()
                            self.printer.success('Operação cancelada!')
                    else:
                        option = self.choose_an_option(
                            confirm_options,
                            text='Realmente deseja deletar um admin?',
                            cancel=True)

                        if option and option == 1:
                            self.admin_crud.delete_admin(admin_id)
                            self.printer.success(
                                text='Admin deletado com sucesso!',
                                clear=True)
                        else:
                            self.printer.success(
                                'Operação cancelada!', clear=True)

                except Exception as e:
                    self.printer.error(f'Erro ao criar sala: {e}')

                finally:
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
                        text='Preenchas os campos ou digite "q" para cancelar.',
                        line=True
                    )

                    admin_id: str = input('Admin ID: ').strip()

                    if admin_id.lower() == 'q':
                        self.manage_admin()

                    admin = self.admin_crud.select_by_id(admin_id)

                    if not admin:
                        self.printer.error(
                            text='Nenhum admin identificado, tente novamente',
                            clear=True)

                        put_admin()

                    person = self.person_crud.select_by_id(admin[1])

                    old_data['name'] = person[1]
                    old_data['email'] = person[2]
                    old_data['password'] = person[3]

                    name = input(
                        'Nome (deixe em branco para manter o atual): ').strip()
                    if name == None:
                        self.printer.warning(
                            text='Atualização cancelada',
                            clear=True)
                        continue

                    email = self.inputs.input_email(
                        'Email (deixe em branco para manter o atual): ')
                    if email == None:
                        self.printer.warning(
                            text='Atualização cancelada',
                            clear=True)
                        continue

                    password = self.inputs.input_password(
                        'Senha (deixe em branco para manter a atual): ')
                    if password == None:
                        self.printer.warning(
                            text='Atualização cancelada',
                            clear=True)
                        continue

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
                        'CLIENT ID',
                        'PERSON ID',
                        'NAME',
                        'EMAIL',
                        'PASSWORD'
                    ]

                    client_list: list = self.client_crud.select_all_clients()

                    client_list_formatted = [[
                        client[0],
                        client[1],
                        client[2],
                        client[3],
                        f'{str(client[4])[:50]}...'
                    ] for client in client_list]

                    self.printer.display_table(header, client_list_formatted)
                    self.manage_client()

                except Exception as e:
                    self.terminal.clear()
                    self.printer.error(f'Erro ao mostrar admins {e}')
                    self.manage_client()

        def del_client_by_email() -> None:
            while True:
                try:
                    self.terminal.clear()
                    self.printer.generic(
                        text='Preencha os campos ou digite "q" para cancelar',
                        line=True)

                    client_email: str = input('Email: ').strip()

                    if client_email.lower() == 'q':
                        self.printer.error(
                            text='Exclusão cancelada',
                            clear=True)
                        break

                    if not self.client_crud.select_by_email(client_email):
                        self.printer.error(
                            text='Nenhum cliente com esse EMAIL encontrado',
                            clear=True)
                        break

                    confirm_delete: str = self.client_crud.delete_client_by_email(
                        client_email)

                    if client_email == confirm_delete:
                        self.printer.success(
                            text='Cliente deletado com sucesso!', clear=True)
                        self.manage_client()

                except Exception as e:
                    self.printer.error(f'Erro ao deletar cliente: {e}')
                finally:
                    self.manage_client()

        def del_client_by_id() -> None:
            while True:
                try:
                    self.terminal.clear()
                    self.printer.generic(
                        text='Preencha os campos ou digite "q" para cancelar',
                        line=True)

                    client_id: str = input('Client ID: ')

                    if client_id.lower() == 'q':
                        self.printer.error(
                            text='Exclusão cancelada',
                            clear=True)
                        break

                    if not self.client_crud.select_by_id(client_id):
                        self.printer.error(
                            text='Nenhum cliente com esse ID encontrado',
                            clear=True)
                        break

                    confirm_delete: str = self.client_crud.delete_client_by_id(
                        client_id)

                    if client_id == confirm_delete:
                        self.printer.success(
                            'Cliente deletado com sucesso!', clear=True)

                    self.manage_client()

                except Exception as e:
                    self.printer.error(f'Erro ao deletar cliente: {e}')

                finally:
                    self.manage_client()

        def crt_client() -> None:
            while True:
                try:
                    self.terminal.clear()
                    self.printer.generic(
                        text='Preencha os campos ou digite "q" cancelar',
                        line=True)

                    person_data = self.inputs.input_person()
                    if person_data == None:
                        self.printer.success('Inserção cancelada!', clear=True)
                        break

                    person_id: str = self.person_crud.insert_person(
                        person_data)

                    self.client_crud.insert_client(person_id)
                    self.printer.success('Cliente criado com sucesso!')
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
                    old_data: dict = {}
                    new_data: dict = {}

                    self.terminal.clear()
                    self.printer.generic(
                        'Digite o EMAIL, ou "q" para cancelar', line=True)
                    email: str = input('Email: ').strip().lower()

                    if email == 'q':
                        self.printer.success(
                            text='Edição de cliente cancelada',
                            clear=True)
                        self.manager.person_view.manage_client()

                    client: Optional[tuple] = self.client_crud.select_by_email(
                        email)

                    if not client:
                        self.printer.warning(
                            text='Nenhum cliente identificado, tente novamente',
                            clear=True)
                        put_client()

                    old_data['name'] = client[2]
                    old_data['email'] = client[3]
                    old_data['password'] = client[4]

                    new_data: Optional[dict] = self.inputs.input_put_person()

                    if not new_data:
                        self.printer.success(
                            text='Edição de cliente cancelada',
                            clear=True)
                        self.manager.person_view.manage_client()

                    data: dict = {
                        'name': new_data.get('name') if new_data.get('name') != '' else old_data['name'],
                        'email': new_data.get('email') if new_data.get('email') != '' else old_data['email'],
                        'password': self.hash.generate_hash(new_data.get('password')) if new_data.get('password') != '' else old_data['password'],
                    }

                    self.client_crud.update_client_by_email(email, data)
                    self.printer.success(
                        'Cliente atualizado com sucesso!',
                        clear=True)

                except ValueError as e:
                    self.printer.error(text=f'{e}', clear=True)

                except Exception as e:
                    self.printer.error(f'Erro ao atualizar cliente: {e}')

                finally:
                    self.manage_client()

        while True:

            manage_options: list = [
                'Criar novo cliente',
                'Listar clientes',
                'Deletar cliente por id',
                'Deletar cliente por email',
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
                        del_client_by_id()
                    case 4:
                        del_client_by_email()
                    case 5:
                        put_client()
                    case 6:
                        self.manager.person_view.start()
                    case _:
                        self.invalid_option()
                        self.manager.person_view.start()

            except Exception as e:
                self.printer.error(e)
