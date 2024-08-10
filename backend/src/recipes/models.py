from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class Recipe(BaseModel):
    id: Optional[str] = Field(alias="_id", default_factory=str)
    title: str = Field(min_length=2, max_length=100)
    rating: Optional[float] = Field(ge=0.0, le=5.0)
    previewImageUrlTemplate: Optional[str] = Field(min_length=10, max_length=2000)

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "title": "Spaghetti Carbonara",
                "rating": 4.5,
                "previewImageUrlTemplate": "https://img.chefkoch-cdn.de/rezepte/3584231538593337/bilder/1157296"
                                           "/<format>/tandoori-haehnchen-mit-reis.jpg"
            }
        }
    )

    # def __repr__(self):
    #     """Return a string representation of the Recipe instance."""
    #     return f"Recipe(id={self.id}, title='{self.title}')"
