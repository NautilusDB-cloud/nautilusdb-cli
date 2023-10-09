from urllib import request

import requests
import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from nautiluscli.model import (
    CreateQACollectionRequest,
    DeleteQACollectionRequest,
    AddDocRequest,
    AskRequest,
)


def create_collection(url: str, name: str):
    url += "/qacollections/create"
    req = CreateQACollectionRequest(name=name)
    resp = requests.post(url=url, data=req.model_dump_json())
    return("status_code:", resp.status_code, resp.json())


def delete_collection(url: str, name: str):
    url += "/qacollections/delete"
    req = DeleteQACollectionRequest(name=name)
    resp = requests.post(url=url, data=req.model_dump_json())
    return("status_code:", resp.status_code, resp.json())


def list_collections(url: str):
    url += "/qacollections/list"
    resp = requests.get(url=url)
    return("status_code:", resp.status_code, resp.json())


def add_doc(url: str, clname: str, file_path: str):
    url += "/qadocs/add"
    req = AddDocRequest(collection_name=clname)
    data = {"request": req.model_dump_json()}
    fname = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        resp = requests.post(url=url, files={'file': (fname, f)}, data=data)
        return("status_code:", resp.status_code, resp.json())


def add_web_doc(url: str, clname: str, file_path: str):
    url += "/qadocs/add"
    req = AddDocRequest(collection_name=clname)
    data = {"request": req.model_dump_json()}
    fname = os.path.basename(file_path)
    with request.urlopen(file_path) as f:
        resp = requests.post(url=url, files={'file': (fname, f)}, data=data)
        return("status_code:", resp.status_code, resp.json())


def ask(url: str, clname: str, q: str, explain: bool):
    url += "/qadocs/ask"
    req = AskRequest(collection_name=clname, question=q)
    resp = requests.post(url=url, data=req.model_dump_json())
    answer = resp.json()

    # Pretty-format success cases
    if not explain and 'answer' in answer:
        return answer.get("answer")
    elif resp.status_code == 200:
        return json.dumps(answer, indent=4)
    return("status_code:", resp.status_code, resp.json())

def list_collections(url: str):
    url += "/qacollections/list"
    resp = requests.get(url=url)
    print("status_code:", resp.status_code, resp.json())
