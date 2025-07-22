<script setup lang="ts">
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { recipeService } from '@/services/recipeService'
import placeholderImageDark from '@/assets/recipe-dark.png'
import RecommendationFilters from '@/components/RecommendationFilters.vue'

interface Recipe {
  id: string
  title: string
  rating: number | null
  sourceRatingVotes: number | null
  previewImageUrlTemplate: string | null
  cachedImageUrl?: string | null
  sourceUrl: string
  tagIds: string[]
}

const recommendations = ref<Recipe[]>([])
const loading = ref(false)
const lockedRecipeIds = ref<Set<string>>(new Set())
const currentFilters = ref<any>(null)

// Pull-to-refresh variables
const pullToRefresh = ref(false)
const startY = ref(0)
const currentY = ref(0)
const pullDistance = ref(0)
const isPulling = ref(false)
const refreshThreshold = 80

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
    console.error('Error fetching recommendations:', error)
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

// Pull-to-refresh functionality
const handleTouchStart = (event: TouchEvent) => {
  if (window.scrollY > 0 || loading.value) return
  startY.value = event.touches[0].clientY
  isPulling.value = true
}

const handleTouchMove = (event: TouchEvent) => {
  if (!isPulling.value || loading.value) return
  
  currentY.value = event.touches[0].clientY
  pullDistance.value = Math.max(0, currentY.value - startY.value)
  
  if (pullDistance.value > 0) {
    pullToRefresh.value = true
    // Prevent default scrolling when pulling down from top
    if (window.scrollY === 0) {
      event.preventDefault()
    }
  }
}

const handleTouchEnd = () => {
  if (!isPulling.value) return
  
  isPulling.value = false
  
  if (pullDistance.value >= refreshThreshold) {
    // Trigger refresh
    fetchRecommendations()
  }
  
  // Reset pull state
  pullToRefresh.value = false
  pullDistance.value = 0
  startY.value = 0
  currentY.value = 0
}

// Add event listeners for mobile devices only
onMounted(() => {
  const isMobile = window.matchMedia('(max-width: 768px)').matches
  if (isMobile) {
    document.addEventListener('touchstart', handleTouchStart, { passive: false })
    document.addEventListener('touchmove', handleTouchMove, { passive: false })
    document.addEventListener('touchend', handleTouchEnd)
  }
})

onUnmounted(() => {
  document.removeEventListener('touchstart', handleTouchStart)
  document.removeEventListener('touchmove', handleTouchMove)
  document.removeEventListener('touchend', handleTouchEnd)
})

// Initial load will be triggered by RecommendationFilters component
// after it loads persisted filters from localStorage
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Pull-to-refresh indicator (mobile only) -->
    <div 
      v-if="pullToRefresh && isPulling"
      class="fixed top-0 left-0 right-0 z-50 flex justify-center pt-4 md:hidden transition-opacity duration-200"
      :style="{ transform: `translateY(${Math.min(pullDistance * 0.5, 40)}px)` }"
    >
      <div class="bg-gold-light dark:bg-gold text-white px-4 py-2 flex items-center gap-2 shadow-lg">
        <svg 
          class="w-4 h-4 animate-spin" 
          :class="{ 'text-white': pullDistance >= refreshThreshold }"
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <span class="text-sm font-medium">
          {{ pullDistance >= refreshThreshold ? 'Loslassen zum Aktualisieren' : 'Herunterziehen zum Aktualisieren' }}
        </span>
      </div>
    </div>

    <!-- Filter Component -->
    <div class="mb-8">
      <RecommendationFilters @filters-changed="onFiltersChanged" />
    </div>

    <div class="text-center mb-8 hidden md:block">
      <button
        @click="fetchRecommendations"
        :disabled="loading || lockedRecipeIds.size >= 8"
        class="bg-gold-light dark:bg-gold hover:bg-gold-hover-light dark:hover:bg-gold-hover text-white font-montserrat font-medium py-3 px-6 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {{ loading ? 'Lädt...' : 'Neue Empfehlungen holen' }}
      </button>
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
            <!-- Recipe Tags -->
            <div
              v-if="recipe.tagIds?.length"
              class="flex items-center justify-center flex-wrap gap-3 mb-3"
            >
              <span
                v-for="tag in recipe.tagIds"
                :key="tag"
                class="text-gold-light dark:text-gold text-xs font-montserrat font-medium tracking-wider hover:text-gold-hover-light dark:hover:text-gold-hover transition-colors duration-200"
              >
                {{ tag.toUpperCase() }}
              </span>
              <span
                v-if="recipe.tagIds.length > 1"
                class="text-gold-light dark:text-gold text-[8px]"
                >◆</span
              >
            </div>

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
                  <span v-for="n in Math.floor(recipe.rating)" :key="n">★</span>
                  <span v-if="recipe.rating % 1 >= 0.5" class="opacity-40">★</span>
                </div>
                <span class="font-montserrat text-xs">{{ recipe.rating.toFixed(1) }}</span>
              </div>
              <span class="text-[8px] text-gold-light dark:text-gold">◆</span>
              <span class="font-montserrat text-xs font-medium tracking-wider">
                {{ recipe.sourceRatingVotes || 0 }} STIMMEN
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
      <p class="text-dark dark:text-light text-lg">Keine Empfehlungen gefunden. Versuche es später noch einmal!</p>
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
