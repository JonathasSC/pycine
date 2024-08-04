from time import sleep
from tabulate import tabulate
from rich.console import Console
from src.utils.terminal import Terminal


class Printer:
    def __init__(self) -> None:
        self.console = Console()
        self.terminal = Terminal()

    def generic(self,
                text: str,
                color: str = 'white',
                line: bool = False,
                timer: bool = False,
                clear: bool = False):

        if clear:
            self.terminal.clear()

        if line:
            self.line(size=len(text) + 8, color=color)
            self.console.print(
                f'[bold {color}] {text.center(len(text) + 4)} [/bold {color}]')

            self.line(size=len(text) + 8, color=color)
        else:
            self.console.print(f'[bold {color}] {text} [/bold {color}]')

        if timer:
            sleep(3)

        if clear:
            self.terminal.clear()

    def line(self,
             size,
             color: str = 'white') -> None:
        self.console.print(f'[{color}]{"="*size}[/{color}]')

    def error(self,
              text: str,
              line: bool = True,
              timer: bool = True,
              clear: bool = False):
        color: str = 'red'
        self.generic(text, color, line, timer, clear)

    def success(self,
                text: str,
                line: bool = True,
                timer: bool = True,
                clear: bool = False):
        color: str = 'green'
        self.generic(text, color, line, timer, clear)

    def warning(self,
                text: str,
                line: bool = True,
                timer: bool = True,
                clear: bool = False):
        color: str = 'yellow'
        self.generic(text, color, line, timer, clear)

    def option_list(self,
                    options: list):
        for index, item in enumerate(options):
            self.generic(f'[{index + 1}] - {item}')

    def display_table(self,
                      headers: list,
                      table_data: list,
                      page: int = 1,
                      per_page: int = 10):

        total_pages = (len(table_data) + per_page - 1) // per_page

        while True:
            self.terminal.clear()
            try:
                start_idx = (page - 1) * per_page
                end_idx = start_idx + per_page
                paginated_data = table_data[start_idx:end_idx]

                table = tabulate(
                    paginated_data,
                    headers=headers,
                    tablefmt='grid'
                )

                print(table)
                print(f'\nPágina {page} de {total_pages}')

                page_input = self.validate_page(total_pages)

                if page_input == 0:
                    break
                elif 1 <= page_input <= total_pages:
                    page = page_input

            except Exception as e:
                self.error(text=f'{e}', clear=True)

    def validate_page(self, total_pages: int):
        while True:
            try:
                user_input = int(
                    input(f"Escolha a pagina (1 - {total_pages}) ou '0' para voltar: "))
                if 0 <= user_input <= total_pages:
                    return user_input
                else:
                    self.error(
                        f"Valor inválido. Por favor, digite um número entre 0 e {total_pages}.")
            except ValueError:
                self.error('Valor inválido. Por favor, digite um número.')

    def display_movies(self, movies_list: list) -> None:
        headers: list = ['NAME', 'GENRE', 'DURATION', 'SYNOPSIS']

        self.terminal.clear()
        self.printer.generic(
            text='Filmes em cartaz',
            line=True
        )

        movies_compacted = [[
            movie[6],
            movie[7],
            movie[8],
            f'{str(movie[9])[:50]}...'] for movie in movies_list
        ]

        self.display_table(headers, movies_compacted)
        self.start()

    def create_seat_matrix(self, seats: list) -> list:
        max_row = max(seat[3] for seat in seats) + 1
        max_col = max(seat[4] for seat in seats) + 1

        seat_matrix = [['' for _ in range(max_col)] for _ in range(max_row)]

        for seat in seats:
            row = seat[3]
            col = seat[4]
            state = seat[5]
            seat_code = seat[2]

            match state:
                case 'available':
                    color_code = '\033[92m'
                case 'reserved':
                    color_code = '\033[93m'
                case 'sold':
                    color_code = '\033[91m'
                case _:
                    color_code = '\033[0m'

            seat_matrix[row][col] = f"{color_code}[{seat_code}]\033[0m"

        return seat_matrix

    def print_seat_matrix(self, seat_matrix: list) -> None:
        self.terminal.clear()
        print(' Tela '.center(len(seat_matrix[0]) * 5, '-'))

        for row in seat_matrix:
            print(" ".join(row))

    def password_params(self) -> None:
        self.error('A senha deve conter: ', timer=False)

        self.error(
            text='- Pelo menos um digito',
            line=False,
            timer=False)

        self.error(
            '- Pelo menos um caractere especial',
            line=False,
            timer=False)

        self.error(
            '- Pelo menos um letra maiuscula',
            line=False,
            timer=True)
