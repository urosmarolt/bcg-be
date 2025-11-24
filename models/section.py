from enum import Enum
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from models.base import ResponseModel

class PromptsInputModel(str, Enum):
    AI = "AI"
    USER = "USER"

class SectionModel(BaseModel):
    sectionID: str
    content: str = Field(default_factory=str)

class SectionPromptsModel(BaseModel):
    text: str
    sender: PromptsInputModel = Field(
        None,
        description="Prompt's content creator"
    )

class PromptsRequestModel(BaseModel):
    sections: List[SectionModel] = Field(default_factory=list)
    prompts: List[SectionPromptsModel] = Field(default_factory=list)
    originalText: str
    userQuery: str

class PromptsResponseModel(ResponseModel):
    response: str = Field(default_factory=str)