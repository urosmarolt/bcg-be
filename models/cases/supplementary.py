from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from models.base import ResponseModel


class SupplementaryInfo(BaseModel):
    title: str = Field(
        ...,
        description="The title of the supplementary information",
        examples=["Supplementary Information from UK GOV report on Badgers"],
    )
    text: Optional[str] = Field(
        ...,
        description="The copy of the supplementary information",
        examples=[
            "Duis viverra sem a lacus dapibus, facilisis ullamcorper metus pulvinar. Donec vitae pharetra lectus. Quisque accumsan pharetra enim a fringilla. Nam faucibus, erat et luctus consequat, enim enim sagittis magna, ac maximus massa nisi ac augue. Pellentesque eu cursus quam. Aliquam lobortis mattis aliquet. Maecenas vestibulum bibendum diam. Aliquam erat volutpat. Fusce ligula lacus, aliquet sit amet quam vitae, vulputate mollis ligula. Vestibulum sollicitudin lacus ac suscipit faucibus. Quisque quis purus convallis, vestibulum enim a, semper tortor. Aenean lacinia facilisis arcu et ultricies. Suspendisse potenti."],
    )


class SupplementaryInfoRequest(BaseModel):
    document: SupplementaryInfo


class SupplementaryInfoResponse(ResponseModel):
    doc_type: str = Field(
        default="Supplementary Information",
    )