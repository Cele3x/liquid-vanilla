<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { recipeService } from '@/services/recipeService'
import placeholderImageDark from '@/assets/recipe-dark.png'
import RecommendationFilters from '@/components/RecommendationFilters.vue'

interface Recipe {
  id: string
  title: string
  rating: {
    rating: number | null
    numVotes: number | null
  } | null
  previewImageUrlTemplate: string | null
  cachedImageUrl?: string | null
  sourceUrl: string
  tags: string[]
}

const recommendations = ref<Recipe[]>([])
const loading = ref(false)
const lockedRecipeIds = ref<Set<string>>(new Set())
const currentFilters = ref<any>(null)

// Helper function to safely get a valid rating value from nested structure
const getSafeRating = (rating: any): number => {
  if (!rating || typeof rating !== 'object' || !('rating' in rating)) {
    return 0
  }
  
  const ratingValue = Number(rating.rating)
  return isNaN(ratingValue) || ratingValue < 0 || ratingValue > 5 ? 0 : ratingValue
}

const fetchRecommendations = async () => {
  loading.value = true

  // Immediately filter out unlocked recipes to show loading placeholders
  const lockedRecipes = recommendations.value.filter((recipe) =>
    lockedRecipeIds.value.has(recipe.id)
  )
  recommendations.value = lockedRecipes

  try {
    const lockedIds = Array.from(lockedRecipeIds.value)
    const response = await recipeService.getRecommendations(lockedIds, currentFilters.value)
    recommendations.value = response.recommendations
  } catch (error) {
    console.error('Fehler beim Laden der Empfehlungen:', error)
    // On error, restore locked recipes at least
    recommendations.value = lockedRecipes
  } finally {
    loading.value = false
  }
}

const onFiltersChanged = (filters: any) => {
  currentFilters.value = filters
  // Auto-trigger recommendations load when filters change
  fetchRecommendations()
}

const toggleLock = (recipeId: string) => {
  if (lockedRecipeIds.value.has(recipeId)) {
    lockedRecipeIds.value.delete(recipeId)
  } else {
    lockedRecipeIds.value.add(recipeId)
  }
}

const isLocked = (recipeId: string) => {
  return lockedRecipeIds.value.has(recipeId)
}

const loadingPlaceholders = computed(() => {
  if (!loading.value) return 0
  // Show loading placeholders for the missing slots (up to 8 total)
  return Math.max(0, 8 - recommendations.value.length)
})

// Initial load will be triggered by RecommendationFilters component
// after it loads persisted filters from localStorage
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Filter Component -->
    <div class="mb-8">
      <RecommendationFilters @filters-changed="onFiltersChanged" />
    </div>

    <div
      v-if="recommendations.length || loadingPlaceholders > 0"
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
    >
      <!-- Regular Recipe Cards -->
      <div
        v-for="recipe in recommendations"
        :key="recipe.id"
        class="relative overflow-hidden shadow-lg transition-all duration-300 ease-in-out hover:shadow-2xl"
        :class="{ 'ring-2 ring-gold-light dark:ring-gold ring-opacity-60': isLocked(recipe.id) }"
      >
        <!-- Lock/Unlock Button -->
        <button
          @click="toggleLock(recipe.id)"
          class="absolute top-3 right-3 z-10 p-3 rounded-full transition-all duration-200 hover:scale-110 cursor-pointer"
          :class="
            isLocked(recipe.id)
              ? 'bg-gold-light dark:bg-gold text-white shadow-lg hover:bg-gold-hover-light dark:hover:bg-gold-hover'
              : 'bg-black bg-opacity-40 text-white hover:bg-opacity-70 hover:bg-gold-light dark:hover:bg-gold'
          "
          :title="isLocked(recipe.id) ? 'Rezept entsperren' : 'Rezept sperren'"
        >
          <svg
            v-if="isLocked(recipe.id)"
            class="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
            />
          </svg>
          <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z"
            />
          </svg>
        </button>

        <a
          :href="recipe.sourceUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="block relative recipe-item"
        >
          <!-- Recipe Image -->
          <div class="relative overflow-hidden h-48 w-full">
            <img
              :src="
                recipe.cachedImageUrl ||
                recipe.previewImageUrlTemplate?.replace('<format>', 'crop-360x240') ||
                placeholderImageDark
              "
              :alt="recipe.title"
              class="recipe-image object-cover w-full h-full transition-transform duration-300 ease-in-out"
            />
          </div>

          <!-- Recipe Subsection -->
          <div class="p-4 min-h-[120px]">
            <!-- Recipe Title -->
            <h3
              class="text-dark dark:text-light font-raleway text-lg font-normal tracking-wide text-center mb-3"
            >
              {{ recipe.title.toUpperCase() }}
            </h3>

            <!-- Recipe Rating -->
            <div
              v-if="recipe.rating"
              class="recipe-rating flex items-center justify-center gap-3 text-gold-light dark:text-gold"
            >
              <div class="tracking-wider text-sm flex items-center gap-2">
                <div class="flex">
                  <span v-for="n in Math.floor(getSafeRating(recipe.rating))" :key="n">★</span>
                  <span v-if="getSafeRating(recipe.rating) % 1 >= 0.5" class="opacity-40">★</span>
                </div>
                <span class="font-montserrat text-xs">{{ getSafeRating(recipe.rating).toFixed(1) }}</span>
              </div>
              <span class="text-[8px] text-gold-light dark:text-gold">◆</span>
              <span class="font-montserrat text-xs font-medium tracking-wider">
                {{ recipe.rating?.numVotes || 0 }} BEWERTUNGEN
              </span>
            </div>
          </div>
        </a>
      </div>

      <!-- Loading Placeholder Cards -->
      <div
        v-for="n in loadingPlaceholders"
        :key="'loading-' + n"
        class="relative overflow-hidden shadow-lg transition-all duration-300 ease-in-out border border-gray-300 dark:border-gray-600"
      >
        <!-- Image Area -->
        <div
          class="relative overflow-hidden h-48 w-full bg-transparent flex items-center justify-center"
        >
          <!-- Big Loading Spinner -->
          <svg
            class="animate-spin h-16 w-16 text-dark dark:text-gold-light"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
        </div>

        <!-- Content Area -->
        <div class="p-4 min-h-[120px]">
          <!-- Empty content to match recipe card height -->
        </div>
      </div>
    </div>

    <div
      v-if="!loading && !recommendations.length && loadingPlaceholders === 0"
      class="text-center mt-8"
    >
      <p class="text-dark dark:text-light text-lg">
        Keine Empfehlungen gefunden. Versuchen Sie es später noch einmal!
      </p>
    </div>

    <div class="text-center mt-8">
      <button
        @click="fetchRecommendations"
        :disabled="loading || lockedRecipeIds.size >= 8"
        class="bg-gold-light dark:bg-gold hover:bg-gold-hover-light dark:hover:bg-gold-hover text-white font-montserrat font-medium py-3 px-6 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {{ loading ? 'Lädt...' : 'Neue Empfehlungen holen' }}
      </button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.recipe-item:hover .recipe-image {
  transform: scale(1.05);
}

.recipe-rating:hover {
  @extend .text-gold-hover !optional;
}
</style>
