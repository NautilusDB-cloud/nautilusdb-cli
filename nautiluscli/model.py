import json
from pydantic import BaseModel, model_validator
from typing import List

ANSWER_REF_SAMPLE_TEXT_LEN = 50


class CreateQACollectionRequest(BaseModel):
    name: str


class DeleteQACollectionRequest(BaseModel):
    name: str


class AddDocRequest(BaseModel):
    collection_name: str

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

    def to_json_string(self) -> str:
        # fastapi server expects "property name enclosed in double quotes" when
        # using with UploadFile. pydantic.model_dump_json() uses single quote.
        # explicitly uses json.dumps for AddDocRequest.
        return json.dumps(self.__dict__)


class AskRequest(BaseModel):
    collection_name: str
    question: str


class AnswerReference(BaseModel):
    doc_name: str
    sample_text: str


class AskResponse(BaseModel):
    answer: str
    refs: List[AnswerReference]
