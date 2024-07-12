from src.views.room_view import RoomView
from src.views.home_view import HomeView
from src.views.admin_view import AdminView
from src.views.movie_view import MoviesCrud
from src.views.client_view import ClientView
from src.views.person_view import PersonView
from src.views.session_view import SessionView


class Manager:
    def __init__(self) -> None:
        self.home_view = HomeView(self)
        self.room_view = RoomView(self)
        self.admin_view = AdminView(self)
        self.movie_view = MoviesCrud(self)
        self.person_view = PersonView(self)
        self.client_view = ClientView(self)
        self.session_view = SessionView(self)

    def start(self):
        self.home_view.start()
