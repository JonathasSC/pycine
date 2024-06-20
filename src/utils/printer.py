from rich.console import Console


class Printer:
    def __init__(self) -> None:
        self.console = Console()

    def generic(self, text: str, color: str = 'white', line: bool = False):
        if line:
            self.line(size=(len(text) + 4), color=color)
            self.console.print(f'[{color}]{text}[/{color}]')
            self.line(size=(len(text) + 4), color=color)
        else:
            self.console.print(f'[{color}]{text}[/{color}]')

    def line(self, size, color: str = 'white') -> None:
        self.console.print(f'[{color}]{"="*size}[/{color}]')

    def error(self, text: str, line: bool = False):
        color: str = 'red'
        self.generic(text, color, line)

    def success(self, text: str, line: bool = False):
        color: str = 'green'
        self.generic(text, color, line)

    def warning(self, text: str, line: bool = False):
        color: str = 'yellow'
        self.generic(text, color, line)

    def option_list(self, options: list):
        for index, item in enumerate(options):
            self.generic(f'[{index + 1}] - {item}')
