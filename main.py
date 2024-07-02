from src.views.home_view import HomeView
from src.utils.populate import Populate


def main():
    Populate().populate_sessions()
    HomeView().start()


if __name__ == '__main__':
    main()
