from src.views.room_view import RoomView
from src.views.home_view import HomeView
from src.views.admin_view import AdminView
from src.views.movie_view import MovieView
from src.views.client_view import ClientView
from src.views.person_view import PersonView
from src.views.session_view import SessionView
from src.views.purchase_view import PurchaseView
from src.views.auth_view import AuthView


class Manager:
    def __init__(self) -> None:
        self.auth_view = AuthView(self)
        self.home_view = HomeView(self)
        self.room_view = RoomView(self)
        self.admin_view = AdminView(self)
        self.movie_view = MovieView(self)
        self.person_view = PersonView(self)
        self.client_view = ClientView(self)
        self.session_view = SessionView(self)
        self.purchase_view = PurchaseView(self)

    def start(self):
        self.home_view.start()
