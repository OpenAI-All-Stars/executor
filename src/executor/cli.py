import logging
import click
import uvicorn

from executor.web import app


@click.group()
def cli() -> None:
    logging.basicConfig(level=logging.INFO)


@cli.command()
def server() -> None:
    uvicorn.run(app)
