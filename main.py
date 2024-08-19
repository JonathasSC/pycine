from src.views.manager import Manager
from src.database.conn import Connection


def main():
    Connection().create_tables()
    Manager().start()


if __name__ == '__main__':
    main()
