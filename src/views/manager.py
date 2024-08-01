from src.views.auth_view import AuthView
from src.views.seat_view import SeatView
from src.views.room_view import RoomView
from src.views.home_view import HomeView
from src.views.admin_view import AdminView
from src.views.movie_view import MovieView
from src.views.client_view import ClientView
from src.views.person_view import PersonView
from src.views.session_view import SessionView
from src.views.purchase_view import PurchaseView


class Manager:
    def __init__(self) -> None:
        self.seat_view: SeatView = SeatView(self)
        self.auth_view: AuthView = AuthView(self)
        self.home_view: HomeView = HomeView(self)
        self.room_view: RoomView = RoomView(self)
        self.admin_view: AdminView = AdminView(self)
        self.movie_view: MovieView = MovieView(self)
        self.person_view: PersonView = PersonView(self)
        self.client_view: ClientView = ClientView(self)
        self.session_view: SessionView = SessionView(self)
        self.purchase_view: PurchaseView = PurchaseView(self)

    def start(self) -> None:
        self.home_view.start()
