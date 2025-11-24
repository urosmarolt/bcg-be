from typing import List
from typing import Optional

from pydantic import BaseModel

from models.base import ResponseModel


class PolicyDocument(BaseModel):
    title: str


class PolicyDocumentResponse(ResponseModel):
    accessible: bool
    url: Optional[str] = None
    name: str


class PolicyDocsRequest(BaseModel):
    documents: List[PolicyDocument]


class PolicyDocsResponse(ResponseModel):
    message: List[PolicyDocumentResponse]