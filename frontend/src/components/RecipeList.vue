<script setup lang="ts">
import { computed, onMounted, onUnmounted } from 'vue'
import { useRecipeStore } from '@/stores/recipeStore'
import { useTagStore } from '@/stores/tagStore'
import { storeToRefs } from 'pinia'
import placeholderImageDark from '@/assets/recipe-dark.png'

const recipeStore = useRecipeStore()
const tagStore = useTagStore()
// Using storeToRefs to maintain reactivity
const { recipes, loading, allLoaded } = storeToRefs(recipeStore)

// Recipes carry tag ids; resolve them to the handful of names a card can show.
const cardTags = computed(() => (tagIds: string[]) => tagStore.cardTags(tagIds))

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
  tagStore.fetchTags()
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
            <!-- Recipe Tags -->
            <div
              v-if="cardTags(recipe.tagIds ?? []).names.length"
              class="flex items-center justify-center flex-nowrap gap-3 mb-3"
            >
              <span
                v-for="tag in cardTags(recipe.tagIds ?? []).names"
                :key="tag"
                class="text-gold-light dark:text-gold text-xs font-montserrat font-medium tracking-wider truncate hover:text-gold-hover-light dark:hover:text-gold-hover transition-colors duration-200"
              >
                {{ tag.toUpperCase() }}
              </span>
              <span
                v-if="cardTags(recipe.tagIds ?? []).hiddenCount"
                :title="cardTags(recipe.tagIds ?? []).allNames.join(' · ')"
                class="text-gold-light/70 dark:text-gold/70 text-xs font-montserrat font-medium tracking-wider shrink-0 cursor-pointer hover:text-gold-hover-light dark:hover:text-gold-hover transition-colors duration-200"
              >
                +{{ cardTags(recipe.tagIds ?? []).hiddenCount }}
              </span>
            </div>

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
              <div
                v-if="recipe.rating !== null"
                class="tracking-wider text-sm flex items-center gap-2"
              >
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
    </div>
    <div v-if="loading" class="text-center mt-4">
      <p class="text-dark dark:text-light">Weitere Rezepte werden geladen...</p>
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
