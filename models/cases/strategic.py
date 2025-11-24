from enum import Enum
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from models.base import ResponseModel
from models.cases.supplementary import SupplementaryInfo


class ProjectSector(str, Enum):
    TRANSPORT = "Transport & Infrastructure"
    HEALTH = "Health & Social Care"
    EDUCATION = "Education"
    HOUSING = "Housing & Planning"
    ENVIRONMENT = "Environment & Sustainability"
    DIGITAL = "Digital & Technology"
    ECONOMIC = "Economic Development"
    OTHER = "Other"


class StrategicCase(BaseModel):
    projectTitle: str = Field(
        ...,
        description="Title of the project",
        examples=["Business Report"]
    )
    projectDescription: str = Field(
        ...,
        description="Detailed description of the project including budget, location, objectives, and key outcomes",
        examples=[
            "a £2.5m Active Travel infrastructure scheme in Oxford targeting improved modal shift and climate outcomes"]
    )
    keyFactsIssues: Optional[str] = Field(
        None,
        description="Key facts or issues that need to be taken into account in developing this business case",
        examples=["Provide additional context to help create a more tailored business case"]
    )
    estimatedBudget: Optional[str] = Field(
        None,
        description="Estimated budget for the project",
        examples=["£2.5m"]
    )
    location: Optional[str] = Field(
        None,
        description="Location of the project",
        examples=["Oxford"]
    )
    projectSector: Optional[ProjectSector] = Field(
        None,
        description="Sector the project belongs to"
    )

    frameworks: Optional[List[str]] = None

    supplementaryInformation: Optional[List[SupplementaryInfo]] = Field(
        description="Supplementary info about the project",
        examples=[]
    )


class StrategicCaseRequest(BaseModel):
    document: StrategicCase


class StrategicCaseResponse(ResponseModel):
    doc_type: str = Field(
        default="Business Case",
    )