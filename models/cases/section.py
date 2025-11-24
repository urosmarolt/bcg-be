from pydantic import BaseModel
from pydantic import Field

from models.section import SectionModel


class SectionGeneration(BaseModel):
    sectionId: str = Field(
        description="The unique identifier of the section to be generated. Should be in X-Y format",
        example="1-1",
    )

    sections: list[SectionModel] = Field(
        description="The list of sections that the new section should be based on",
        example="""
        [
            {
                "sectionID": "2-1",
                "content": "This is the content of section 2.1" 
            }
        ]
        """
    )

    initialParams: str = Field(
        description="The parameters laid out at the beginning of section generation. Should be a stringified JSON object.",
        example="""
        {
            projectDescription: "This is the description of the project",
            supplementaryInformation: [
                {
                    "title": "EVs in Bristol",
                    "text": "This is a summary of an article saying that EVs have many hidden disadvantages"
                }
            ]
        }
        """
    )


class SectionGenerationResponse(BaseModel):
    content: str = Field(
        description="The response containing the generated section data.",
    )

class SectionGenerationRequest(BaseModel):
    document: SectionGeneration