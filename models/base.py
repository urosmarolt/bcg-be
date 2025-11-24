from datetime import datetime
from datetime import timezone
from typing import Generic
from typing import Optional
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar('T')


class ResponseModel(BaseModel, Generic[T]):
    status: str = "success"  # or "error"
    message: Optional[str] = None
    data: Optional[T] = None
    date: Optional[datetime] = datetime.now(tz=timezone.utc)