# nautilusdb-python-client

A command-line tool for [NautilusDB](http://nautilusdb.com), a fully-managed, 
cloud-native vector search service.

NautilusDB is currently in <ins>**public alpha**</ins>. We're actively improving 
the product and releasing new features and we'd love to hear your feedback! 
Please take a moment to fill out this [feedback form](https://forms.gle/pif6Vx2LqPjW5v4w5) to help us understand your use-case better.

> By default, all collections are subject to permanent deletion after 2 weeks. Please let us know if you need to keep it for longer via the feedback form.


## Quickstart
You can try out NautilusDB right away. We have prepared a special public 
collection ```openai-web``` that can answer questions about the contents of ```www.openai.com``` 

```shell
nautiluscli ask openai-web "what is red team?"
 ```

## Examples:

### Create a new API key
You can create a new API key and set it in ```NAUTILUSDB_API_KEY``` 
environment variable. NautilusDB will use this key to authorize access to 
collections.
```shell
nautiluscli create-api-key
export NAUTILUSDB_API_KEY='<key>'
```

### Check the current CLI configuration
```shell
nautiluscli info
```

### Create a new Collection 
Create a new collection ```myCollection``` in the shared demo account. If an 
API key is configured, a private collection will be created that is only accessible to the configured API key.
```shell
 nautiluscli create-collection myCollection
```

### List Collections
See the list of Collection accessible to you, including ```myCollection``` 
that you just created.
```shell
nautiluscli list-collections
```

### Upload file from URL
Index a PDF into ```myCollection```. In this example, we will index the original research paper on Transformers.
```shell
 nautiluscli upload-file myCollection https://arxiv.org/pdf/1706.03762.pdf
```

### Upload local file
Alternatively, upload a PDF from local file system for indexing.
```shell
nautiluscli upload-file myCollection README.md
```

### Ask questions 
You can now ask questions within the context of a collection and get answers. 
```shell
nautiluscli ask myCollection "what is a transformer?"
```

### Delete the Collection
You can optionally delete the collection. Deletions are non-reversible. 
```shell
nautiluscli delete-collection myCollection
```
