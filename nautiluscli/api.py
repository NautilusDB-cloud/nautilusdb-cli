from urllib import request

import requests
import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from nautiluscli.model import (
    CreateCollectionRequest,
    DeleteCollectionRequest,
    AddDocRequest,
    AskRequest,
    CreateApiKeyRequest,
)


def _get_headers():
    api_key = os.getenv('NAUTILUSDB_API_KEY', None)
    return {'api-key': api_key} if api_key is not None and api_key != "" else None


def post(url, data=None, files=None):
    return requests.post(url=url, data=data, files=files, headers=_get_headers())


def get(url):
    return requests.get(url=url, headers=_get_headers())


def get_response(resp: requests.Response):
    if resp.status_code == 200:
        return resp.json()

    try:
        # Try parsing out server error
        reason = json.loads(resp.content)
        return reason.get('detail')
    except Exception as e:
        # Probably an error thrown somewhere else
        # simply return the response content.
        return resp.content


def create_api_key(url: str):
    url += "/apikey/create"
    req = CreateApiKeyRequest()
    resp = post(url=url, data=req.model_dump_json())
    return ("status_code:", resp.status_code, get_response(resp))


def create_collection(url: str, name: str):
    url += "/collections/create"
    metas = {"text": "string", "tokens": "int", "filename": "string"}
    req = CreateCollectionRequest(name=name, dimension=1536, metas=metas)
    resp = post(url=url, data=req.model_dump_json())
    return ("status_code:", resp.status_code, get_response(resp))


def delete_collection(url: str, name: str):
    url += "/collections/delete"
    req = DeleteCollectionRequest(name=name)
    resp = post(url=url, data=req.model_dump_json())
    return ("status_code:", resp.status_code, get_response(resp))


def list_collections(url: str):
    url += "/qacollections/list"
    resp = get(url=url)
    return ("status_code:", resp.status_code, get_response(resp))


def add_doc(url: str, clname: str, file_path: str):
    url += "/qadocs/add"
    req = AddDocRequest(collection_name=clname)
    data = {"request": req.model_dump_json()}
    fname = os.path.basename(file_path)
    validation_error = validate_file(file_path)
    if validation_error is not None:
        return validation_error
    with open(file_path, 'rb') as f:
        resp = post(url=url, files={'file': (fname, f)}, data=data)
        return ("status_code:", resp.status_code, get_response(resp))


def add_web_doc(url: str, clname: str, file_path: str):
    url += "/qadocs/add"
    req = AddDocRequest(collection_name=clname)
    data = {"request": req.model_dump_json()}
    fname = os.path.basename(file_path)

    validation_error = validate_url_file(file_path)
    if validation_error is not None:
        return validation_error

    with request.urlopen(file_path) as f:
        resp = post(url=url, files={'file': (fname, f)}, data=data)
        return ("status_code:", resp.status_code, get_response(resp))


def validate_url_file(url):
    nbyte = 0
    try:
        resp = requests.request('HEAD', url)
        nbyte = int(resp.headers.get("Content-Length"))
    except Exception as e:
        pass
    if nbyte > 9_500_000:
        return (
            f"File {url} exceeds size limit 9.5MB, actual size {nbyte} "
            f"bytes")
    return None


def validate_file(path: str):
    nbyte = os.path.getsize(path)
    if nbyte > 9_500_000:
        return (f"File {path} exceeds size limit 9.5MB, actual size {nbyte} "
                f"bytes")
    return None


def ask(url: str, clname: str, q: str, explain: bool):
    url += "/qadocs/ask"
    req = AskRequest(collection_name=clname, question=q)
    resp = post(url=url, data=req.model_dump_json())
    answer = resp.json()

    # Pretty-format success cases
    if not explain and 'answer' in answer:
        return answer.get("answer")
    elif resp.status_code == 200:
        return json.dumps(answer, indent=4)
    return ("status_code:", resp.status_code, resp.json())
