import os.path
import sys

import click

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import nautiluscli.api as api
from urllib import parse

PUBLIC_ACCOUNT = 'public'
PUBLIC_API_ENDPOINT = f'http://{PUBLIC_ACCOUNT}.us-west-2.aws.nautilusdb.com'


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
     1. [Optional] Create a new API key and set it in NAUTILUSDB_API_KEY env var
     >>> nautiluscli create-api-key
     >>> export NAUTILUSDB_API_KEY='<key>'

     \b
     2. [Optional] Check the current CLI configuration
     >>> nautiluscli info

     \b
     3. Create a new Collection `myCollection` in the shared demo account
        If an API key is configured, a private collection will be created that
        is only accessible to the configured API key.
     >>> nautiluscli create-collection myCollection

     \b
     4. [Optional] See a new Collection `myCollection` created
     >>> nautiluscli list-collections

     \b
     5. Index a PDF into `myCollection`. In this example, we will index the original research paper on Transformers.
     >>> nautiluscli upload-file myCollection https://arxiv.org/pdf/1706.03762.pdf

     \b
     6. Alternatively, upload a PDF for indexing. Note that demo account and all Collections are publicly accessible
        , so please do not upload anything sensitive!
     >>> nautiluscli upload-file myCollection README.md

     \b
     7. Ask and get answers. Referenced source data is also returned.
     >>> nautiluscli ask myCollection "what is a transformer?"

     \b
     8. [Optional] Delete the Collection
     >>> nautiluscli delete-collection myCollection
     """
    pass


@cli.command("list-collections")
def list_collections():
    """
    List all collection names in the current account.
    """
    click.echo(api.list_collections(PUBLIC_API_ENDPOINT))


@cli.command("delete-collection")
@click.argument('collection', type=click.STRING)
def delete_collections(collection):
    """
    Permanently delete a collection.
    """
    click.echo(api.delete_collection(PUBLIC_API_ENDPOINT, collection))


@cli.command("create-collection")
@click.argument('collection', type=click.STRING)
def create_collections(collection):
    """
    Create a collection
    """
    click.echo(api.create_collection(PUBLIC_API_ENDPOINT, collection))


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
        click.echo(api.add_web_doc(PUBLIC_API_ENDPOINT, collection, file.value))
    else:
        click.echo(api.add_doc(PUBLIC_API_ENDPOINT, collection, file.value))


@cli.command("ask")
@click.argument('collection', type=click.STRING)
@click.argument('question', type=click.STRING)
@click.option('--explain/--noexplain', default=True)
def ask(collection, question, explain):
    """
    Ask a question against a collection
    """
    click.echo(api.ask(PUBLIC_API_ENDPOINT, collection, question, explain))


@cli.command("info")
def info():
    """
    Displays current cli configuration
    """
    api_key = os.getenv('NAUTILUSDB_API_KEY')
    if api_key is None or api_key == '':
        api_key = '<none configured>'
    click.echo("The current configuration of NautilusDB is:")
    click.echo(f"Account:      {PUBLIC_ACCOUNT}")
    click.echo(f"API endpoint: {PUBLIC_API_ENDPOINT}")
    click.echo(f"API key:      {api_key}")


@cli.command("create-api-key")
def create_api_key():
    """
    Creates a new API key
    """
    click.echo(api.create_api_key(PUBLIC_API_ENDPOINT))


def run():
    cli()


if __name__ == "__main__":
    run()
