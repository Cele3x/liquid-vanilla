from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class Ingredient(BaseModel):
    ingredientId: str
    unitId: str
    amount: float


class IngredientGroup(BaseModel):
    header: Optional[str]
    ingredients: List[Ingredient]


class Recipe(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    title: str = Field(min_length=2, max_length=100)
    rating: Optional[float] = Field(ge=0.0, le=5.0, default=None)
    sourceUrl: Optional[str] = Field(min_length=10, max_length=2000, default=None)
    previewImageUrlTemplate: Optional[str] = Field(min_length=10, max_length=2000, default=None)
    additionalDescription: Optional[str] = None
    cookingTime: Optional[int] = None
    createdAt: Optional[datetime] = None
    difficulty: Optional[int] = None
    ingredients: Optional[List[IngredientGroup]] = None
    ingredientsText: Optional[str] = None
    instructions: Optional[List[str]] = None
    miscellaneousText: Optional[str] = None
    preparationTime: Optional[int] = None
    restingTime: Optional[int] = None
    servings: Optional[int] = None
    source: Optional[str] = None
    sourceId: Optional[str] = None
    sourceRating: Optional[float] = None
    sourceRatingVotes: Optional[int] = None
    sourceViewCount: Optional[int] = None
    status: Optional[str] = None
    subtitle: Optional[str] = None
    tags: Optional[List[str]] = None
    totalTime: Optional[int] = None
    userId: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "title": "Spaghetti Carbonara",
                "rating": 4.5,
                "sourceUrl": "https://www.chefkoch.de/rezepte/21763",
                "previewImageUrlTemplate": "https://img.chefkoch-cdn.de/rezepte/3584231538593337/bilder/1157296"
                                           "/<format>/tandoori-haehnchen-mit-reis.jpg",
                "additionalDescription": "A classic Italian pasta dish",
                "cookingTime": 20,
                "createdAt": "2023-06-01T12:00:00Z",
                "difficulty": 2,
                "ingredientsText": "400g spaghetti, 200g pancetta, 4 eggs, 100g Pecorino cheese, Black pepper",
                "instructions": ["Cook pasta", "Fry pancetta", "Mix eggs and cheese", "Combine all ingredients"],
                "preparationTime": 10,
                "servings": 4,
                "source": "Chefkoch",
                "sourceRating": 4.7,
                "sourceRatingVotes": 1000,
                "status": "active",
                "subtitle": "Quick and delicious",
                "tags": ["Italian", "Pasta", "Quick"],
                "totalTime": 30
            }
        }
    )

    # def __repr__(self):
    #     """Return a string representation of the Recipe instance."""
    #     return f"Recipe(id={self.id}, title='{self.title}')"
