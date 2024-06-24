import os
import platform


class Terminal:
    def __init__(self) -> None:
        self.system_name: str = platform.system()

    def clear(self):
        try:
            if self.system_name == 'Windows':
                os.system("cls")
            else:
                os.system("clear")
        except Exception as e:
            print(f'erro ao limpar terminal: {e}')
