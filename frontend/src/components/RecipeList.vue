<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { recipeService } from '@/services/recipeService'

interface Recipe {
  id: string
  title: string
  rating: number
  previewImageUrlTemplate: string
  defaultImageUrl: string
  sourceUrl: string
}

const recipes = ref<Recipe[]>([])


onMounted(async () => {
  try {
    const route = useRoute()
    const page = Number(route.query.page) || 1
    const pageSize = Number(route.query.page_size) || 20
    const data = await recipeService.getRecipes(page, pageSize)
    console.log('Fetched recipes:', data.recipes)
    recipes.value = data.recipes.map((recipe: Recipe) => ({
      ...recipe,
      defaultImageUrl: recipe.previewImageUrlTemplate.replace('<format>', 'crop-240x300')
    }))
  } catch (error) {
    console.error('Failed to fetch recipes:', error)
  }
})
</script>

<template>
  <div>
    <h1>Recipes</h1>
    <div v-if="recipes.length" class="recipe-grid">
      <div v-for="recipe in recipes" :key="recipe.id" class="recipe-item">
        <a :href="recipe.sourceUrl" target="_blank" rel="noopener noreferrer">
          <img :src="recipe.defaultImageUrl" :alt="recipe.title" class="recipe-image" />
        </a>
        <div class="recipe-title">{{ recipe.title }}</div>
      </div>
    </div>
    <p v-else>Loading recipes...</p>
  </div>
</template>

<style scoped>
.recipe-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 4 items per row */
  gap: 20px;
  padding: 20px;
}

.recipe-item {
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.recipe-image {
  width: 100%;
  height: 300px;
  object-fit: cover;
  display: block;
}

.recipe-title {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 10px;
  font-size: 14px;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Responsive adjustments */
@media (max-width: 1200px) {
  .recipe-grid {
    grid-template-columns: repeat(3, 1fr); /* 3 items per row */
  }
}

@media (max-width: 900px) {
  .recipe-grid {
    grid-template-columns: repeat(2, 1fr); /* 2 items per row */
  }
}

@media (max-width: 600px) {
  .recipe-grid {
    grid-template-columns: 1fr; /* 1 item per row */
  }
}
</style>
