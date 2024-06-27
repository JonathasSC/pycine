from src.views.base_view import BaseView


class PersonView(BaseView):
    def __init__(self):
        super().__init__()

        self.list_options: list = [
            'Gerenciar Admins',
            # 'Gerenciar Persons',
            # 'Gerenciar Clients',
            # 'Voltar',
            'Sair'
        ]

        self.option_actions = {
            1: self.manage_admin,
            # 2: self.back_to,
            3: self.exit
        }

    def start(self):
        while True:
            try:
                self.terminal.clear()
                option: int = self.choose_an_option(self.list_options)
                self.execute_option(self.option_actions, option)
                break

            except Exception as e:
                self.printer.error(e)

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

                    input('Voltar? [press enter]')
                    break

                except Exception as e:
                    self.terminal.clear()
                    self.printer.error(f'Erro ao mostrar admins {e}')
                    break

            self.start()

        def del_admin(admin_crud=self.admin_crud):
            while True:
                try:
                    person_id: str = input('Person ID: ')
                    admin_crud.delete_admin(person_id)
                    self.printer.success('Admin deletado com sucesso!')
                    break
                except Exception as e:
                    self.printer.error(f'Erro ao criar sala: {e}')
                    break

            self.start()

        while True:

            manage_options: list = [
                'Listar admins',
                'Deletar admin',
                'Sair'
            ]

            manage_actions = {
                1: get_all_admins,
                2: del_admin,
                3: self.exit,
            }

            try:
                self.terminal.clear()
                option: int = self.choose_an_option(manage_options)
                self.execute_option(manage_actions, option)

            except Exception as e:
                self.printer.error(e)
