# Third party libraries
import click


@click.group(
    help=(
        'The 4s Comand Line Interface is a unified tool to manage your '
        'Four Shells services'
    ),
)
def main():
    pass


@main.group(
    name='cachipfs',
)
def cachipfs():
    pass


@cachipfs.command(
    name='daemon',
)
def cachipfs_daemon():
    print('hello')


if __name__ == '__main__':
    main(prog_name='4s')
