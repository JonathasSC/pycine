from src.views.base_view import BaseView


class PersonView(BaseView):
    def __init__(self):
        super().__init__()
        self.before_view = None

        self.list_options: list = [
            'Gerenciar Admins',
            'Voltar',
            'Sair'
        ]

        self.option_actions = {
            1: self.manage_admin,
            2: self.back_to_admin,
            3: self.close
        }

    def start(self):
        while True:
            try:
                self.terminal.clear()
                option: int = self.choose_an_option(self.list_options)

                match option:
                    case 1:
                        self.manage_admin()
                    case 2:
                        self.back_to_admin()
                    case 3:
                        self.close()
                        break
                    case _:
                        self.invalid_option()
                        self.start()

            except Exception as e:
                self.printer.error(e, timer=True)

    def set_back_view(self, view):
        self.before_view = view

    def back_to_admin(self):
        if self.before_view:
            self.before_view.start()
        self.printer.error('AdminView não definida')

    def manage_admin(self):
        def get_all_admins(admin_crud=self.admin_crud):
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
                    admin_list: list = admin_crud.select_all_admins()
                    self.printer.display_table(header, admin_list)
                    self.manage_admin()

                except Exception as e:
                    self.terminal.clear()
                    self.printer.error(f'Erro ao mostrar admins {e}')
                    self.manage_admin()

        def del_admin(admin_crud=self.admin_crud):
            while True:
                try:
                    person_id: str = input('Person ID: ')
                    admin_crud.delete_admin(person_id)
                    self.printer.success('Admin deletado com sucesso!')
                    self.manage_admin()

                except Exception as e:
                    self.printer.error(f'Erro ao criar sala: {e}')
                    self.manage_admin()

        def create_admin(admin_crud=self.admin_crud):
            while True:
                try:
                    person_id: str = input('Person ID: ')
                    admin_crud.insert_admin(person_id)
                    self.printer.success('Admin criado com sucesso!')
                    self.manage_admin()

                except Exception as e:
                    self.printer.error(f'Erro ao criar sala: {e}')
                    self.manage_admin()

        while True:

            manage_options: list = [
                'Criar novo admin',
                'Listar admins',
                'Deletar admin',
                'Voltar'
            ]

            manage_actions = {
                1: create_admin,
                2: get_all_admins,
                3: del_admin,
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
