<script setup lang="ts">
import { onUnmounted, ref, watch } from 'vue'
import { useRecipeStore } from '@/stores/recipeStore'

const props = defineProps<{
  isVisible: boolean
}>()

const emit = defineEmits<{
  (e: 'update:isVisible', value: boolean): void
}>()

const recipeStore = useRecipeStore()
const searchQuery = ref('')

// Watch for changes in searchQuery and update store after a delay (debounce)
let timeout: ReturnType<typeof setTimeout>
watch(searchQuery, (newQuery) => {
  clearTimeout(timeout)
  timeout = setTimeout(() => {
    if (newQuery.trim()) {
      recipeStore.setSearchQuery(newQuery.trim())
    } else {
      recipeStore.resetStore()
      recipeStore.fetchRecipes()
    }
  }, 300) // 300ms delay
})

const handleSearch = async () => {
  if (searchQuery.value.trim()) {
    try {
      recipeStore.setSearchQuery(searchQuery.value.trim())
    } catch (error) {
      console.error('Failed to search recipes:', error)
    }
  }
}

const handleSearchBlur = () => {
  if (!searchQuery.value.trim()) {
    emit('update:isVisible', false)
  }
}

const clearSearch = () => {
  searchQuery.value = ''
  recipeStore.resetStore()
  recipeStore.fetchRecipes()
  document.getElementById('search')?.focus()
}

// Clean up timeout on component unmount
onUnmounted(() => {
  clearTimeout(timeout)
})
</script>

<template>
  <div
    class="absolute inset-0 transition-all duration-300 ease-in-out flex items-center"
    :class="{
      'opacity-100 translate-x-0': isVisible,
      'opacity-0 translate-x-4 invisible': !isVisible
    }"
  >
    <div class="relative w-full">
      <input
        v-model="searchQuery"
        @keyup.enter="handleSearch"
        @keyup.esc="emit('update:isVisible', false)"
        @blur="handleSearchBlur"
        type="text"
        name="search"
        id="search"
        class="w-full h-9 pl-3 pr-10 border border-secondary leading-5 bg-secondary text-light placeholder-accent focus:outline-none focus:ring-1 focus:ring-accent focus:border-accent sm:text-sm"
        placeholder="Search"
      />
      <button
        v-if="searchQuery"
        @click="clearSearch"
        class="absolute right-2 top-1/2 -translate-y-1/2 text-accent hover:text-light focus:outline-none"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
            clip-rule="evenodd"
          />
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.invisible {
  visibility: hidden;
}
</style>