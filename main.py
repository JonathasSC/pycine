from src.views.manager import Manager
from src.database.conn import Connection
from src.utils.populate import Populate


def main():
    Connection().create_tables()
    Manager().start()


if __name__ == '__main__':
    main()
