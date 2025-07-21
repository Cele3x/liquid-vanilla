<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { recipeService } from '@/services/recipeService'
import placeholderImageDark from '@/assets/recipe-dark.png'

interface Recipe {
  id: string
  title: string
  rating: number | null
  sourceRatingVotes: number | null
  previewImageUrlTemplate: string | null
  sourceUrl: string
  tagIds: string[]
}

const recommendations = ref<Recipe[]>([])
const loading = ref(false)

const fetchRecommendations = async () => {
  loading.value = true
  try {
    const response = await recipeService.getRecommendations()
    recommendations.value = response.recommendations
  } catch (error) {
    console.error('Error fetching recommendations:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRecommendations()
})
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div class="text-center mb-8">
      <button
        @click="fetchRecommendations"
        :disabled="loading"
        class="bg-gold-light dark:bg-gold hover:bg-gold-hover-light dark:hover:bg-gold-hover text-white font-montserrat font-medium py-3 px-6 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {{ loading ? 'Loading...' : 'Get New Recommendations' }}
      </button>
    </div>

    <div
      v-if="recommendations.length"
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
    >
      <div
        v-for="recipe in recommendations"
        :key="recipe.id"
        class="relative overflow-hidden shadow-lg transition-all duration-300 ease-in-out hover:shadow-2xl"
      >
        <a
          :href="recipe.sourceUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="block relative recipe-item"
        >
          <!-- Recipe Image -->
          <div class="relative overflow-hidden aspect-w-16 aspect-h-9">
            <img
              :src="recipe.previewImageUrlTemplate?.replace('<format>', 'crop-360x240') || placeholderImageDark"
              :alt="recipe.title"
              class="recipe-image object-cover w-full h-full transition-transform duration-300 ease-in-out"
            />
          </div>

          <!-- Recipe Subsection -->
          <div class="p-4">
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
              <span v-if="recipe.tagIds.length > 1" class="text-gold-light dark:text-gold text-[8px]">◆</span>
            </div>

            <!-- Recipe Title -->
            <h3 class="text-dark dark:text-light font-raleway text-lg font-normal tracking-wide text-center mb-3">
              {{ recipe.title.toUpperCase() }}
            </h3>

            <!-- Recipe Rating -->
            <div v-if="recipe.rating" class="recipe-rating flex items-center justify-center gap-3 text-gold-light dark:text-gold">
              <div class="tracking-wider text-sm flex items-center gap-2">
                <div class="flex">
                  <span v-for="n in Math.floor(recipe.rating)" :key="n">★</span>
                  <span v-if="recipe.rating % 1 >= 0.5" class="opacity-40">★</span>
                </div>
                <span class="font-montserrat text-xs">{{ recipe.rating.toFixed(1) }}</span>
              </div>
              <span class="text-[8px] text-gold-light dark:text-gold">◆</span>
              <span class="font-montserrat text-xs font-medium tracking-wider">
                {{ recipe.sourceRatingVotes || 0 }} VOTES
              </span>
            </div>
          </div>
        </a>
      </div>
    </div>

    <div v-if="loading" class="text-center mt-8">
      <p class="text-dark dark:text-light text-lg">Loading recommendations...</p>
    </div>

    <div v-if="!loading && !recommendations.length" class="text-center mt-8">
      <p class="text-dark dark:text-light text-lg">No recommendations found. Try again later!</p>
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