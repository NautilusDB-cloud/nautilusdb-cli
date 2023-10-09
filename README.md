# nautilusdb-python-client

A command-line tool to interact with NautilusDB. You can manage collections, add new vectors and query any collection from this CLI.

    Examples:

     1. Create a new Collection `myCollection` in the shared demo account
     nautiluscli create-collection myCollection

     2. [Optional] See a new Collection `myCollection` created
     nautiluscli list-collections

     3. Index a PDF into `myCollection`. In this example, we will index the original research paper on Transformers.
     nautiluscli upload-file myCollection https://arxiv.org/pdf/1706.03762.pdf

     4. Alternatively, upload a PDF for indexing. Note that demo account and all Collections are publicly accessible
        , so please do not upload anything sensitive!
     nautiluscli upload-file myCollection README.md

     5. Ask and get answers. Referenced source data is also returned.
     nautiluscli ask myCollection "what is a transformer?" --explain

     6. [Optional] Delete the Collection
     nautiluscli delete-collection myCollection
