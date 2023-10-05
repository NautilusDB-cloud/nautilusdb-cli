import os.path
import time

import click

from lib.embedding_model import EmbeddingModel
from lib.api import create_collection, add_doc, ask, add_web_doc, delete_collection
from urllib import parse

DEMO_COLLECTION = 'NautilusDBDemoCollection'
DEMO_API_ENDPOINT = "https://b487hc1om1.execute-api.us-west-2.amazonaws.com/alpha"

SUPPORTED_ACTIONS = ['create-collection', 'delete-collection', 'ask', 'upsert-vectors']


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
        if parsed_value.scheme != '' and parsed_value.scheme not in ("http", "https"):
            self.fail(f"Invalid URL or file name \"{value}\"")
        return UrlOrFile('url', value)


@click.command()
@click.argument('action', type=click.Choice(SUPPORTED_ACTIONS))
@click.argument('collection', type=click.STRING)
#@click.option('--model', '-m', type=click.Choice([EmbeddingModel.OPENAI_DEFAULT_EMBEDDING.value]),
#              default=EmbeddingModel.OPENAI_DEFAULT_EMBEDDING.value, show_default=True)
@click.option('--file', '-f', type=UrlOrFile())
@click.option('--query', '-q')
#@click.option('--gen/--nogen', default=True)
def nautilus(action, collection, file: UrlOrFile, query):
    """
    A command-line tool to interact with NautilusDB. You can manage collections, add new vectors and query any
    collection from this CLI.

    \b
    Examples:

    \b
    1. Create a new Collection `myCollection` in the shared demo account
    >>> poetry run python nautiluscli.py create-collection myCollection

    \b
    2. Index a PDF into `myCollection`. In this example, we will index the original research paper on Transformers.
    >>> poetry run python nautiluscli.py upsert-vectors myCollection --file=https://arxiv.org/pdf/1706.03762.pdf

    \b
    3. Alternatively, upload a PDF for indexing. Note that demo account and all Collections are publicly accessible
       , so please do not upload anything sensitive!
    >>> poetry run python nautiluscli.py upsert-vectors myCollection --file=README.md

    \b
    4. Query a Collection to get answers!
    >>> poetry run python nautiluscli.py ask myCollection --query="what is a transformer?"
    """
    t0 = time.monotonic()
    api_endpoint = DEMO_API_ENDPOINT
    match action:
        case 'create-collection':
            create_collection(api_endpoint, collection)
        case 'delete-collection':
            delete_collection(api_endpoint, collection)
        case 'ask':
            if query is None or query == '':
                raise click.BadParameter("No question specified")
            ask(api_endpoint, collection, query)
        case 'upsert-vectors':
            if file is None:
                raise click.BadParameter("Must specify a file or an URL")

            # Handle URL separately
            if file.is_url():
                add_web_doc(api_endpoint, collection, file.value)
            else:
                add_doc(api_endpoint, collection, file.value)
        case _:
            raise click.BadParameter(f"Unsupported action {action}")
    t1 = time.monotonic()
    print(f"Run time: {t1 - t0:.4f}s")


if __name__ == "__main__":
    nautilus()
