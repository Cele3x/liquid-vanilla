<script setup lang="ts">
import { onMounted, ref, onUnmounted } from 'vue'
import { recipeService } from '@/services/recipeService'
import placeholderImage from '@/assets/recipe.png'

interface Recipe {
  id: string
  title: string
  rating: number
  previewImageUrlTemplate: string
  defaultImageUrl: string
  sourceUrl: string
}

const recipes = ref<Recipe[]>([])
const page = ref(1)
const pageSize = 20
const loading = ref(false)
const allLoaded = ref(false)

const fetchRecipes = async () => {
  if (loading.value || allLoaded.value) return

  loading.value = true
  try {
    const data = await recipeService.getRecipes(page.value, pageSize)
    const newRecipes = data.recipes.map((recipe: Recipe) => ({
      ...recipe,
      defaultImageUrl: recipe.previewImageUrlTemplate.replace('<format>', 'crop-240x300')
    }))
    recipes.value.push(...newRecipes)
    page.value++
    if (newRecipes.length < pageSize) {
      allLoaded.value = true
    }
  } catch (error) {
    console.error('Failed to fetch recipes:', error)
  } finally {
    loading.value = false
  }
}

const handleScroll = () => {
  const scrollPosition = window.innerHeight + window.scrollY
  const bodyHeight = document.body.offsetHeight
  // Adjust this value to start loading earlier
  const scrollThreshold = bodyHeight - (window.innerHeight * 2)

  if (scrollPosition >= scrollThreshold && !loading.value && !allLoaded.value) {
    fetchRecipes()
  }
}

onMounted(() => {
  fetchRecipes()
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div v-if="recipes.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <div v-for="recipe in recipes" :key="recipe.id" class="recipe-item relative overflow-hidden rounded-lg shadow-lg transition-all duration-300 ease-in-out hover:shadow-2xl">
        <a :href="recipe.sourceUrl" target="_blank" rel="noopener noreferrer" class="block relative overflow-hidden aspect-w-16 aspect-h-9">
          <img :src="recipe.defaultImageUrl || placeholderImage" :alt="recipe.title" class="recipe-image object-cover w-full h-full transition-transform duration-300 ease-in-out" />
          <div class="absolute inset-0 flex flex-col justify-end">
            <div class="text-background p-4 transition-all duration-300 ease-in-out">
              <h3 class="recipe-title text-lg font-semibold text-light truncate">{{ recipe.title }}</h3>
              <div class="flex items-center mt-2">
                <span class="star-icon mr-1">★</span>
                <span class="text-light">{{ recipe.rating.toFixed(1) }}</span>
              </div>
            </div>
          </div>
        </a>
      </div>
    </div>
    <div v-if="loading" class="text-center mt-4">
      <p class="text-light">Loading more recipes...</p>
    </div>
    <div v-if="allLoaded" class="text-center mt-4">
      <p class="text-light">All recipes loaded</p>
    </div>
    <!-- Add this invisible div to trigger earlier loading -->
    <div class="h-screen"></div>
  </div>
</template>

<style scoped>
.recipe-item:hover .recipe-image {
  transform: scale(1.1);
}

.text-background {
  background: linear-gradient(to top,
  rgba(0, 0, 0, 0.9) 0%,
  rgba(0, 0, 0, 0.8) 20%,
  rgba(0, 0, 0, 0.7) 40%,
  rgba(0, 0, 0, 0.5) 60%,
  rgba(0, 0, 0, 0.3) 80%,
  rgba(0, 0, 0, 0) 100%
  );
  transition: all 0.3s ease-in-out;
}

.recipe-item:hover .recipe-title {
  color: #ECDFCC;
}

.star-icon {
  color: #FFD700;
}

</style>
