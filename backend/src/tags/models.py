
from typing import Annotated, Optional
from pydantic import BaseModel, BeforeValidator, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class Tag(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(min_length=2, max_length=100)
    usage_count: int = Field(default=0, ge=0)
    categoryId: Optional[str] = Field(default=None)
