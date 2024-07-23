from src.views.base_view import BaseView
from src.crud.admins_crud import AdminsCrud

from src.utils.token import Token


class HomeView(BaseView):
    def __init__(self, manager):
        super().__init__()

        self.manager = manager

        self.token_manager: Token = Token()
        self.admins_crud: AdminsCrud = AdminsCrud()

        self.list_options: list = [
            'Login',
            'Register',
            'Sair'
        ]

        # self.option_actions = {
        #     1: self.redirect_before_login,
        #     2: self.manager.auth_view.register,
        #     3: self.close
        # }


# def start(self):
#         self.logger.info('START ADMIN VIEW')
#         while True:
#             try:
#                 self.terminal.clear()
#                 option: int = self.choose_an_option(
#                     self.list_options, text='Escolha o que gerenciar')

#                 if option == 1:
#                     self.manager.client_view.start(True)

#                 elif option == 2:
#                     self.admin_flow()

#                 elif option == 3:
#                     self.logout()
#                     self.manager.home_view.start()

#                 elif option == 4:
#                     if self.close():
#                         break

#                 else:
#                     self.invalid_option()

#             except Exception as e:
#                 self.printer.error(f'Erro ao iniciar tela de admin: {e}')

    def start(self):
        while True:
            try:
                if self.admins_crud.get_count_admin() == 0:
                    self.terminal.clear()
                    self.printer.generic('Create first admin', line=True)
                    self.create_admin()

                token = self.token.load_token()
                person_role = self.token.get_role_from_token(token)
                
                if token and person_role:
                    if person_role == 'client':
                        self.manager.client_view.start()
                        break
                    
                    elif person_role == 'admin':
                        self.manager.admin_view.start()
                        break 

                self.terminal.clear()
                
                option: int = self.choose_an_option(
                    options=self.list_options,
                    text='Pycine - Your cinema in terminal'
                )
                
                if option == 1: 
                    self.manager.auth_view.login()
                    self.start()
                    
                elif option == 2:
                    self.manager.auth_view.register()
                    self.manager.auth_view.login()
                    self.start()

                elif option == 3:
                    self.close()
                    break
                break 
                 
            except Exception as e:
                self.printer.error(f'Erro ao iniciar Inicial {e}')

    # def redirect_before_login(self):
    #     person_role: str = self.manager.auth_view.login()
    #     self.redirect_to_role(person_role)
    #     self.start()

    # def redirect_to_role(self, person_role: str):
    #     if person_role == 'client':
    #         self.manager.client_view.start()
    #     elif person_role == 'admin':
    #         self.manager.admin_view.start()
