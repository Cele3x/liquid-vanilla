# Recipe Locking Feature

## Overview
The recipe locking feature allows users to "lock" specific recipes in their recommendations so they remain in place when fetching new recommendations.

## How It Works

### Backend (`/recipes/recommendations`)
- **New Parameter**: `locked_ids` - comma-separated list of recipe IDs to keep in recommendations
- **Logic**: 
  1. Fetch locked recipes by their IDs
  2. Calculate how many new random recipes are needed (8 - locked_count)
  3. Get random recipes excluding already locked ones
  4. Combine locked + new recipes

### Frontend UI
- **Lock Button**: Each recipe card has a lock/unlock button in the top-right corner
- **Visual Indicators**: 
  - Locked recipes have a gold ring border
  - Lock icon changes based on state (locked/unlocked)
  - Counter shows how many recipes are currently locked
- **State Management**: Uses Vue 3 reactive Set to track locked recipe IDs

## User Experience

1. **Initial Load**: Get 8 random recommendations
2. **Lock Recipes**: Click lock button on recipes you want to keep
3. **Get New Recommendations**: Click "Get New Recommendations" button
4. **Result**: Locked recipes stay in place, others are replaced with new random ones
5. **Unlock**: Click lock button again to unlock recipes

## API Usage

### Get recommendations with locked recipes:
```
GET /api/v1/recipes/recommendations?locked_ids=64f1a2b3c4d5e6f7a8b9c0d1,64f1a2b3c4d5e6f7a8b9c0d2
```

### Response format (same as before):
```json
{
  "recommendations": [
    {
      "id": "64f1a2b3c4d5e6f7a8b9c0d1",
      "title": "Locked Recipe",
      ...
    },
    {
      "id": "new_random_id",
      "title": "New Random Recipe", 
      ...
    }
  ]
}
```

## Benefits
- **Personalization**: Users can keep recipes they're interested in
- **Efficiency**: No need to scroll through the same recommendations repeatedly  
- **Discovery**: Still get new suggestions while keeping favorites visible
- **Fast Performance**: Uses efficient MongoDB queries with exclusion filters