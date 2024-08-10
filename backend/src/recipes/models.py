from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class Recipe(BaseModel):
    id: Optional[str] = Field(alias="_id", default_factory=str)
    title: str = Field(min_length=2, max_length=100)

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "title": "Spaghetti Carbonara",
            }
        }
    )

    # def __repr__(self):
    #     """Return a string representation of the Recipe instance."""
    #     return f"Recipe(id={self.id}, title='{self.title}')"
