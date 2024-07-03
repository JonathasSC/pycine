from src.views.home_view import HomeView
from src.utils.populate import Populate
from src.database.conn import Connection


def main():
    Connection().delete_data()
    Connection().create_database()

    Populate().populate_sessions()
    HomeView().start()


if __name__ == '__main__':
    main()
