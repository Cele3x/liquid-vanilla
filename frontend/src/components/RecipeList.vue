<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { useRecipeStore } from '@/stores/recipeStore'
import { storeToRefs } from 'pinia'
import placeholderImageDark from '@/assets/recipe-dark.png'

const recipeStore = useRecipeStore()
// Using storeToRefs to maintain reactivity
const { recipes, loading, allLoaded } = storeToRefs(recipeStore)

// Helper function to safely get a valid rating value from nested structure
const getSafeRating = (rating: any): number => {
  if (!rating || typeof rating !== 'object' || !('rating' in rating)) {
    return 0
  }
  
  const ratingValue = Number(rating.rating)
  return isNaN(ratingValue) || ratingValue < 0 || ratingValue > 5 ? 0 : ratingValue
}

const handleScroll = () => {
  const scrollPosition = window.innerHeight + window.scrollY
  const bodyHeight = document.body.offsetHeight
  const scrollThreshold = bodyHeight - window.innerHeight * 2

  if (scrollPosition >= scrollThreshold && !loading.value && !allLoaded.value) {
    recipeStore.fetchRecipes()
  }
}

onMounted(() => {
  recipeStore.fetchRecipes()
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div
      v-if="recipes.length"
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
    >
      <div
        v-for="recipe in recipes"
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
              :src="recipe.defaultImageUrl || placeholderImageDark"
              :alt="recipe.title"
              class="recipe-image object-cover w-full h-full transition-transform duration-300 ease-in-out"
            />
          </div>

          <!-- Recipe Subsection -->
          <div class="p-4">
            <!-- Recipe Title -->
            <h3
              class="text-dark dark:text-light font-raleway text-lg font-normal tracking-wide text-center mb-3"
            >
              {{ recipe.title.toUpperCase() }}
            </h3>

            <!-- Recipe Rating -->
            <div
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
    </div>
    <div v-if="loading" class="text-center mt-4">
      <p class="text-dark dark:text-light">Lade weitere Rezepte...</p>
    </div>
    <div v-if="allLoaded" class="text-center mt-4">
      <p class="text-dark dark:text-light">Alle Rezepte geladen</p>
    </div>
    <div class="h-screen"></div>
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
