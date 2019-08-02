import click

from pyprof.prof import clear_stats, print_stats


class Application:

    def print(self):
        print_stats()

    def clear(self):
        clear_stats()


app = click.make_pass_decorator(Application, ensure=True)


@click.group()
def cli():
    pass


@cli.command()
@app
def print(app: Application):
    app.print()


@cli.command()
@app
def clear(app: Application):
    app.clear()
