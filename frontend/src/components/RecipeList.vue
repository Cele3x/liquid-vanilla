<script setup lang="ts">
import { onMounted, ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { recipeService } from '@/services/recipeService'

interface Recipe {
  id: string
  title: string
  rating: number
  previewImageUrlTemplate: string
  defaultImageUrl: string
  sourceUrl: string
}

interface PaginationData {
  page: number
  page_size: number
  total: number
  has_next: boolean
  has_previous: boolean
}

const recipes = ref<Recipe[]>([])
const paginationData = ref<PaginationData>({
  page: 1,
  page_size: 20,
  total: 0,
  has_next: false,
  has_previous: false
})

const route = useRoute()
const router = useRouter()

const currentPage = computed(() => Number(route.query.page) || 1)
const pageSize = computed(() => Number(route.query.page_size) || 20)

const fetchRecipes = async (page: number, pageSize: number) => {
  try {
    const data = await recipeService.getRecipes(page, pageSize)
    console.log('Fetched recipes:', data.recipes)
    recipes.value = data.recipes.map((recipe: Recipe) => ({
      ...recipe,
      defaultImageUrl: recipe.previewImageUrlTemplate.replace('<format>', 'crop-240x300')
    }))
    paginationData.value = {
      page: data.page,
      page_size: data.page_size,
      total: data.total,
      has_next: data.has_next,
      has_previous: data.has_previous
    }
  } catch (error) {
    console.error('Failed to fetch recipes:', error)
  }
}

const goToPage = (page: number) => {
  router.push({ query: { ...route.query, page: page.toString() } })
}

onMounted(() => {
  fetchRecipes(currentPage.value, pageSize.value)
})

// Watch for changes in the route query parameters
watch(
  () => route.query,
  () => {
    fetchRecipes(currentPage.value, pageSize.value)
  },
  { deep: true }
)
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div v-if="recipes.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div v-for="recipe in recipes" :key="recipe.id" class="recipe-item bg-dark-secondary rounded-lg overflow-hidden shadow-lg transition-all duration-300 ease-in-out hover:shadow-2xl">
        <a :href="recipe.sourceUrl" target="_blank" rel="noopener noreferrer" class="block relative overflow-hidden aspect-w-4 aspect-h-3">
          <img :src="recipe.defaultImageUrl" :alt="recipe.title" class="recipe-image object-cover w-full h-full transition-transform duration-300 ease-in-out rounded-t-lg" />
        </a>
        <div class="p-4">
          <h3 class="recipe-title text-lg font-semibold text-dark-text truncate">{{ recipe.title }}</h3>
          <div class="flex items-center mt-2">
            <span class="text-yellow-400 mr-1">★</span>
            <span class="text-dark-text">{{ recipe.rating.toFixed(1) }}</span>
          </div>
        </div>
      </div>
    </div>
    <p v-else class="text-dark-text text-center text-xl mt-8">Loading recipes...</p>

    <!-- Pagination controls -->
    <div class="flex justify-center items-center space-x-4 mt-8">
      <button
        :disabled="!paginationData.has_previous"
        @click="goToPage(currentPage - 1)"
        class="px-4 py-2 bg-indigo-600 text-white rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-indigo-700 transition-colors duration-300"
      >
        Previous
      </button>
      <span class="text-dark-text">Page {{ currentPage }} of {{ Math.ceil(paginationData.total / paginationData.page_size) }}</span>
      <button
        :disabled="!paginationData.has_next"
        @click="goToPage(currentPage + 1)"
        class="px-4 py-2 bg-indigo-600 text-white rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-indigo-700 transition-colors duration-300"
      >
        Next
      </button>
    </div>
  </div>
</template>

<style scoped>
.recipe-item:hover .recipe-image {
  transform: scale(1.1);
}

@media (max-width: 640px) {
  .grid {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
}

@media (min-width: 641px) and (max-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (min-width: 1025px) {
  .grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}
</style>
