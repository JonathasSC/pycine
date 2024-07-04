from rich.console import Console
from tabulate import tabulate
from time import sleep
from src.utils.terminal import Terminal


class Printer:
    def __init__(self) -> None:
        self.console = Console()
        self.terminal = Terminal()

    def generic(self, text: str, color: str = 'white', line: bool = False, timer: bool = False):
        if line:
            self.line(size=len(text) + 8, color=color)
            self.console.print(
                f'[bold {color}] {text.center(len(text) + 4)} [/bold {color}]')

            self.line(size=len(text) + 8, color=color)
        else:
            self.console.print(f'[bold {color}] {text} [/bold {color}]')

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

                page_input = self.validate_page(total_pages)

                if page_input is None:
                    break
                elif 1 <= page_input <= total_pages:
                    page = page_input
                else:
                    print(
                        f"Digite um número de página válido (1 - {total_pages}) ou '0' para voltar.")

            except Exception as e:
                print(f'Erro ao mostrar tabela: {e}')

    def validate_page(self, total_pages):
        while True:
            try:
                user_input = int(
                    input(f"Digite o número da página (1 - {total_pages}) ou '0' para voltar: "))

                if user_input == 0 or user_input not in range(1, total_pages + 1):
                    return None
                else:
                    return user_input

            except ValueError:
                print("Entrada inválida. Por favor, digite um número válido.")
            except Exception as e:
                raise e
