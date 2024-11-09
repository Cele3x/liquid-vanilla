from typing import Annotated, List, Optional
from pydantic import BaseModel, BeforeValidator, Field, ConfigDict
from datetime import datetime
from bson import ObjectId

PyObjectId = Annotated[str, BeforeValidator(str)]

class Ingredient(BaseModel):
    ingredientId: Optional[PyObjectId] = None
    unitId: Optional[PyObjectId] = None
    amount: Optional[float] = None

class IngredientGroup(BaseModel):
    header: Optional[str] = None
    ingredients: Optional[List[Ingredient]] = None

# class Tag(BaseModel):
#     id: Optional[str] = Field(alias="_id", default=None)
#     name: str = Field(min_length=2, max_length=100)

class Recipe(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(min_length=2, max_length=100)
    rating: Optional[float] = Field(ge=0.0, le=5.0, default=None)
    sourceUrl: Optional[str] = Field(min_length=10, max_length=2000, default=None)
    previewImageUrlTemplate: Optional[str] = Field(min_length=10, max_length=2000, default=None)
    additionalDescription: Optional[str] = None
    cookingTime: Optional[int] = None
    createdAt: Optional[datetime] = None
    difficulty: Optional[int] = None
    ingredientGroups: Optional[List[IngredientGroup]] = None
    ingredientsText: Optional[str] = None
    instructions: Optional[str] = None
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
    tagIds: Optional[List[PyObjectId]] = None
    totalTime: Optional[int] = None
    userId: Optional[PyObjectId] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        json_encoders={ObjectId: str},
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
                "instructions": "Cook pasta\nFry pancetta \nMix eggs and cheese\nCombine all ingredients",
                "preparationTime": 10,
                "servings": 4,
                "source": "Chefkoch",
                "sourceRating": 4.7,
                "sourceRatingVotes": 1000,
                "status": "active",
                "subtitle": "Quick and delicious",
                "tagIds": ["6628c6369b0fefc37a4de90d", "6628c6369b0fefc37a4de90d"],
                "ingredientGroups": [
                    {
                        "header": "Für das Gemüse:",
                        "ingredients": [
                            {"ingredientId": "6628c6429b0fefc37a4de945", "unitId": "6628c6289b0fefc37a4de8a6",
                             "amount": 500},
                            {"ingredientId": "6628c6289b0fefc37a4de8b1", "unitId": "6628c6289b0fefc37a4de8ab",
                             "amount": 0}
                        ]
                    }
                ],
                "totalTime": 30,
                "userId": "6624e2a193986e2790e3c69f",
            }
        }
    )

    # def __repr__(self):
    #     """Return a string representation of the Recipe instance."""
    #     return f"Recipe(id={self.id}, title='{self.title}')"
