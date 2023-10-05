import os.path
import time

import click

from lib.embedding_model import EmbeddingModel
from lib.cli import create_collection, add_doc, ask, add_web_doc, delete_collection
from urllib import parse

DEMO_COLLECTION = 'NautilusDBDemoCollection'
DEMO_API_ENDPOINT = "https://b487hc1om1.execute-api.us-west-2.amazonaws.com/alpha"

SUPPORTED_ACTIONS = ['create-collection', 'delete-collection', 'ask', 'askquestion', 'upsert-vector', 'upsert-vectors']


class UrlOrFile(click.ParamType):
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
@click.option('--model', '-m', type=click.Choice([EmbeddingModel.OPENAI_DEFAULT_EMBEDDING.value]),
              default=EmbeddingModel.OPENAI_DEFAULT_EMBEDDING.value, show_default=True)
@click.option('--file', '-f', type=UrlOrFile())
@click.option('--query', '-q')
@click.option('--gen/--nogen', default=True)
def nautilus(action, collection, model, file: UrlOrFile, query, gen):
    t0 = time.monotonic()
    api_endpoint = DEMO_API_ENDPOINT
    match action:
        case 'create-collection':
            create_collection(api_endpoint, collection)
        case 'delete-collection':
            delete_collection(api_endpoint, collection)
        case 'ask' | "askquestion":
            if query is None or query == '':
                raise click.BadParameter("No question specified")
            if gen:
                ask(api_endpoint, collection, query)
            else:
                raise click.BadParameter("Non-generative answer not yet supported")
        case 'upsert-vectors' | "upsert-vector":
            if file is None:
                raise click.BadParameter("Must specify a file or an URL")

            # Handle URL separately
            if file.is_url():
                add_web_doc(api_endpoint, collection, file.value)
            else:
                add_doc(api_endpoint, collection, file.value)
    t1 = time.monotonic()
    print(f"Run time: {t1 - t0:.4f}s")


if __name__ == "__main__":
    nautilus()
