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

    <!-- Pagination controls -->
    <div class="pagination">
      <button
        :disabled="!paginationData.has_previous"
        @click="goToPage(currentPage - 1)"
      >
        Previous
      </button>
      <span>Page {{ currentPage }} of {{ Math.ceil(paginationData.total / paginationData.page_size) }}</span>
      <button
        :disabled="!paginationData.has_next"
        @click="goToPage(currentPage + 1)"
      >
        Next
      </button>
    </div>
  </div>
</template>

<style scoped>
.recipe-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 4 items per row */
  gap: 20px;
  padding: 20px;
  margin-bottom: 40px; /* Add this line to create space below the grid */
}

.recipe-item {
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.recipe-item:hover {
  transform: scale(1.03);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

.recipe-image {
  width: 100%;
  height: 300px;
  object-fit: cover;
  display: block;
  transition: transform 0.3s ease, filter 0.3s ease;
}

.recipe-item:hover .recipe-image {
  transform: scale(1.1);
  filter: brightness(1.1);
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
  transition: background-color 0.3s ease;
}

.recipe-item:hover .recipe-title {
  background-color: rgba(0, 0, 0, 0.8);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 40px 0; /* Change this line to add space above and below */
  gap: 20px;
  color: white;
}

.pagination button {
  padding: 12px 24px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
  min-width: 120px;
}

.pagination button:hover:not(:disabled) {
  background-color: #45a049;
  transform: scale(1.05);
}

.pagination button:active:not(:disabled) {
  transform: scale(0.95); /* Slight scale effect on click */
}

.pagination button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.pagination span {
  font-size: 16px;
}

/* Responsive adjustments for pagination */
@media (max-width: 600px) {
  .pagination {
    flex-direction: column;
  }

  .pagination button {
    width: 100%;
    margin-bottom: 10px;
  }
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
