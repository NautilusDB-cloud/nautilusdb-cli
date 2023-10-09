import os.path

import click

import nautiluscli.api as api
from urllib import parse

DEMO_COLLECTION = 'NautilusDBDemoCollection'
DEMO_API_ENDPOINT = "https://b487hc1om1.execute-api.us-west-2.amazonaws.com/alpha"


class UrlOrFile(click.ParamType):
    name: str = "File path or URL"
    type: str
    value: str

    def __init__(self, type='', value=''):
        self.type = type
        self.value = value

    def is_url(self):
        return self.type == 'url'

    def convert(self, value, param, ctx):
        if os.path.isfile(value):
            self.type = 'file'
            return UrlOrFile('file', value)

        parsed_value = parse.urlparse(value)
        if parsed_value.scheme not in ("http", "https"):
            self.fail(f"Invalid URL or file name \"{value}\"")
        return UrlOrFile('url', value)


@click.group()
def cli():
    """
     A command-line tool to interact with NautilusDB. You can manage collections, add new vectors and query any
     collection from this CLI.

     \b
     Examples:

     \b
     1. Create a new Collection `myCollection` in the shared demo account
     >>> nautiluscli create-collection myCollection

     \b
     2. [Optional] See a new Collection `myCollection` created
     >>> nautiluscli list-collections

     \b
     3. Index a PDF into `myCollection`. In this example, we will index the original research paper on Transformers.
     >>> nautiluscli upload-file myCollection https://arxiv.org/pdf/1706.03762.pdf

     \b
     4. Alternatively, upload a PDF for indexing. Note that demo account and all Collections are publicly accessible
        , so please do not upload anything sensitive!
     >>> nautiluscli upload-file myCollection README.md

     \b
     5. Ask and get answers. Referenced source data is also returned.
     >>> nautiluscli ask myCollection "what is a transformer?" --explain

     \b
     6. [Optional] Delete the Collection
     >>> nautiluscli delete-collection myCollection
     """
    pass


@cli.command("list-collections")
def list_collections():
    """
    List all collection names in the current account.
    """
    click.echo(api.list_collections(DEMO_API_ENDPOINT))


@cli.command("delete-collection")
@click.argument('collection', type=click.STRING)
def delete_collections(collection):
    """
    Permanently delete a collection.
    """
    click.echo(api.delete_collection(DEMO_API_ENDPOINT, collection))


@cli.command("create-collection")
@click.argument('collection', type=click.STRING)
def create_collections(collection):
    """
    Create a collection
    """
    click.echo(api.create_collection(DEMO_API_ENDPOINT, collection))


@cli.command("upload-file")
@click.argument('collection', type=click.STRING)
@click.argument('file', type=UrlOrFile())
def upload_file(collection, file):
    """
    Upload and index a file. Either URL or local file path is accepted. URL must contain leading http/https prefix.
    """
    if file is None:
        raise click.BadParameter("Must specify a file or an URL")

    # Handle URL separately
    if file.is_url():
        click.echo(api.add_web_doc(DEMO_API_ENDPOINT, collection, file.value))
    else:
        click.echo(api.add_doc(DEMO_API_ENDPOINT, collection, file.value))


@cli.command("ask")
@click.argument('collection', type=click.STRING)
@click.argument('question', type=click.STRING)
@click.option('--explain/--noexplain', default=True)
def ask(collection, question, explain):
    """
    Ask a question against a collection
    """
    click.echo(api.ask(DEMO_API_ENDPOINT, collection, question, explain))


def run():
    cli()


if __name__ == "__main__":
    run()
