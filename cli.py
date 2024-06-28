import os
import argparse


def cli(command: str):
    match command:
        case 'tests':
            os.system('python -m pytest')
        case 'populate':
            os.system('python -m pytest')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CLI for pycine v2')
    parser.add_argument('--command',
                        type=str,
                        required=True,
                        choices=['tests', 'populate'],
                        help='Type of the command')

    args = parser.parse_args()
    cli(args.command)
