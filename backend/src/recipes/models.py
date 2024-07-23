from typing import Optional
from pydantic import BaseModel, Field


class Recipe(BaseModel):
    id: Optional[str] = Field(alias="_id", default_factory=str)
    name: str = Field(min_length=2, max_length=100)
    description: Optional[str] = Field(default=None, max_length=256)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "Spaghetti Carbonara",
                "description": "A classic Italian pasta dish."
            }
        }

    # def __repr__(self):
    #     """Return a string representation of the Recipe instance."""
    #     return f"Recipe(id={self.id}, name='{self.name}')"
