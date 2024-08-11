<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { recipeService } from '@/services/recipeService'

interface Recipe {
  id: string
  title: string
  rating: number
  previewImageUrlTemplate: string
  defaultImageUrl: string
}

const recipes = ref<Recipe[]>([])

onMounted(async () => {
  try {
    const data = await recipeService.getRecipes()
    console.log('Fetched recipes:', data.recipes)
    // recipes.value = data.recipes
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
    <ul v-if="recipes.length">
      <li v-for="recipe in recipes" :key="recipe.id">
        <span>{{ recipe.title }}</span>
        <img :src="recipe.defaultImageUrl" :alt="recipe.title" />
      </li>
    </ul>
    <p v-else>Loading recipes...</p>
  </div>
</template>

<style scoped></style>
