from enum import Enum
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from models.base import ResponseModel
from models.cases.supplementary import SupplementaryInfo


class CriticalSuccessFactorCategory(str, Enum):
    STRATEGIC = "Strategic Fit",
    VALUE = "Value for Money",
    SUPPLY = "Supply Side Capability and Capacity",
    AFFORDABILITY = "Affordability",
    ACHIEVABILITY = "Achievability",


class CriticalSuccessFactor(BaseModel):
    category: CriticalSuccessFactorCategory = Field(
        ...,
        description="The category of the critical success factor",
    )
    description: str = Field(
        ...,
        description="The text of the critical success factor",
        examples=["Duis viverra sem a lacus dapibus, facilisis ullamcorper metus pulvinar."],
    )


class EconomicCase(BaseModel):
    strategicCase: str = Field(
        description="The current strategic case",
        example="""strategic": {
      "sectionsData": {
        "1-1": {
          "content": "<h3>Strategic Context</h3><p>As stated, this is the 'My Super Cool Business Project' with a planned start in January 2026. The estimated budget is £1.5 billion, and the project falls under the Health & Social Care sector, covering the geographic area of the United Kingdom. The key aim is to implement a strategy for repopulating the UK countryside with badgers, as their colonies have reduced greatly across the nation. <a href='https://www.gov.uk/government/publications/population-estimates-for-uk-badgers/population-estimates-for-uk-badgers' target='_blank'>Government estimates</a> suggest badger populations have declined by around 30% over the past few decades due to factors like habitat loss and disease.</p>",
          "completed": true
        }, 
        "2-1": { .... }
    """
    )

    criticalSuccessFactors: Optional[List[CriticalSuccessFactor]] = Field(
        description="The list of critical success factors",
    )

    frameworks: Optional[List[str]] = None

    supplementaryInformation: Optional[List[SupplementaryInfo]] = Field(
        description="Supplementary info about the project",
        examples=[]
    )


class EconomicCaseResponse(ResponseModel):
    doc_type: str = Field(
        default="Economic Case",
    )


class EconomicCaseRequest(BaseModel):
    document: EconomicCase
