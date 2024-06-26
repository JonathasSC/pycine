from rich.console import Console
from typing import List
from tabulate import tabulate
from time import sleep


class Printer:
    def __init__(self) -> None:
        self.console = Console()

    def generic(self, text: str, color: str = 'white', line: bool = False, timer: bool = False):
        if line:
            self.line(size=(len(text) + 4), color=color)
            self.console.print(f'[{color}]{text}[/{color}]')
            self.line(size=(len(text) + 4), color=color)
        else:
            self.console.print(f'[{color}]{text}[/{color}]')
        if timer:
            sleep(5)

    def line(self, size, color: str = 'white') -> None:
        self.console.print(f'[{color}]{"="*size}[/{color}]')

    def error(self, text: str, line: bool = True, timer: bool = True):
        color: str = 'red'
        self.generic(text, color, line, timer)

    def success(self, text: str, line: bool = True, timer: bool = True):
        color: str = 'green'
        self.generic(text, color, line, timer)

    def warning(self, text: str, line: bool = True, timer: bool = True):
        color: str = 'yellow'
        self.generic(text, color, line, timer)

    def option_list(self, options: list):
        for index, item in enumerate(options):
            self.generic(f'[{index + 1}] - {item}')

    def display_table(self, headers: list, table_data: list, page: int = 1, per_page: int = 10):
        try:
            start_idx: int = (page - 1) * per_page
            end_idx: int = start_idx + per_page

            paginated_movies = table_data[start_idx:end_idx]
            table = tabulate(paginated_movies,
                             headers=headers, tablefmt='grid')
            print(table)

        except Exception as e:
            print(f'Erro ao mostrar filmes: {e}')
