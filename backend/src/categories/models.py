from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, BeforeValidator, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class Category(BaseModel):
    """
    Category model for organizing tags into logical groups.
    
    :param id: Unique identifier for the category
    :param name: Display name of the category
    :param description: Description of what this category contains
    :param createdAt: Timestamp when category was created
    :param updatedAt: Timestamp when category was last updated
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=5, max_length=500)
    createdAt: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updatedAt: Optional[datetime] = Field(default_factory=datetime.utcnow)