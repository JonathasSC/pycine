from src.views.base_view import BaseView


class AdminView(BaseView):
    def __init__(self):
        super().__init__()

    def start(self):
        print('Admin area')
