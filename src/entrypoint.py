import click

from train import TrainingPipeline


@click.group(help="CLI tool to manage full development cycle of projects")
def cli():
    click.echo("Hello World!")


@click.command()
def train():
    TrainingPipeline.train()


@click.command()
@click.option("--cv", "-c", default=5, type=int, help="Number of CV")
@click.option(
    "--scoring",
    "-s",
    default="recall",
    type=click.Choice(["recall", "precision", "f1"], case_sensitive=True),
    prompt="Choosing scoring metric",
    help="Scoring metric for CV",
)
def evaluate(cv, scoring):
    TrainingPipeline.evaluate(cv, scoring)


cli.add_command(train)
cli.add_command(evaluate)

if __name__ == "__main__":
    cli()
