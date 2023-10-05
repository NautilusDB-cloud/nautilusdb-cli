# nautilusdb-python-client

A command-line tool to interact with NautilusDB. You can manage collections, add new vectors and query any collection from this CLI.

    Examples:

    1. Create a new Collection `myCollection` in the shared demo account
    nautiluscli create-collection myCollection

    2. Index a PDF into `myCollection`. In this example, we will index the original research paper on Transformers.
    nautiluscli upsert-vectors myCollection --file=https://arxiv.org/pdf/1706.03762.pdf

    3. Alternatively, upload a PDF for indexing. Note that demo account and all Collections are publicly accessible
       , so please do not upload anything sensitive!
    nautiluscli upsert-vectors myCollection --file=README.md

    4. Query a Collection to get answers!
    nautiluscli ask myCollection --query="what is a transformer?"
