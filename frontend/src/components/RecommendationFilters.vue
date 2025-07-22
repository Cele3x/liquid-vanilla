<template>
  <div class="recommendation-filters">
    <!-- Filter Toggle Button -->
    <button
      @click="showFilters = !showFilters"
      class="w-full mb-4 flex items-center justify-between bg-light dark:bg-secondary hover:bg-accent dark:hover:bg-accent px-4 py-3 transition-colors text-dark dark:text-light cursor-pointer"
      :class="{ 'bg-gold-light/20 dark:bg-gold/20 border-2 border': activeFiltersCount > 0 }"
    >
      <div class="flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707v4.586l-4-2V12a1 1 0 00-.293-.707L3.293 4.707A1 1 0 013 4z" />
        </svg>
        <span class="font-medium">Recipe Filters</span>
        <span v-if="activeFiltersCount > 0" class="bg-gold-light dark:bg-gold text-white text-sm px-2 py-1 ">
          {{ activeFiltersCount }}
        </span>
      </div>
      <svg 
        class="w-5 h-5 transition-transform duration-200" 
        :class="{ 'rotate-180': showFilters }"
        fill="none" stroke="currentColor" viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- Filter Panel -->
    <div v-show="showFilters" class="bg-white dark:bg-secondary border border p-4 space-y-6">
      <!-- Rating Filter -->
      <div class="filter-section">
        <label class="block text-base font-medium text-dark dark:text-light mb-3">
          Minimum Rating: {{ filters.minRating }}★
        </label>
        <div class="flex items-center gap-2 mb-2">
          <button
            v-for="rating in [0, 3.0, 3.5, 4.0, 4.5]"
            :key="rating"
            @click="filters.minRating = rating"
            class="px-3 py-1 text-sm  border transition-colors cursor-pointer"
            :class="filters.minRating === rating ? 'bg-gold-light dark:bg-gold text-white border' : 'bg-light dark:bg-accent hover:bg-accent dark:hover:bg-secondary border text-dark dark:text-light'"
          >
            {{ rating === 0 ? 'Any' : rating + '★' }}
          </button>
        </div>
        <input
          v-model.number="filters.minRating"
          type="range"
          min="0"
          max="5"
          step="0.1"
          class="w-full h-2 bg-gold-light dark:bg-gold  appearance-none cursor-pointer slider"
        />
      </div>

      <!-- Votes Filter -->
      <div class="filter-section">
        <label class="block text-base font-medium text-dark dark:text-light mb-3">
          Minimum Votes: {{ filters.minVotes }}
        </label>
        <div class="flex items-center gap-2 mb-2">
          <button
            v-for="preset in votePresets"
            :key="preset"
            @click="filters.minVotes = preset"
            class="px-3 py-1 text-sm  border transition-colors cursor-pointer"
            :class="filters.minVotes === preset ? 'bg-gold-light dark:bg-gold text-white border' : 'bg-light dark:bg-accent hover:bg-accent dark:hover:bg-secondary border text-dark dark:text-light'"
          >
            {{ preset }}+
          </button>
        </div>
        <input
          v-model.number="filters.minVotes"
          type="range"
          min="0"
          max="5000"
          step="50"
          class="w-full h-2 bg-gold-light dark:bg-gold  appearance-none cursor-pointer slider"
        />
      </div>

      <!-- Has Image Toggle -->
      <div class="filter-section">
        <label class="flex items-center justify-between">
          <span class="text-base font-medium text-dark dark:text-light">Only recipes with images</span>
          <div 
            @click="filters.hasImage = !filters.hasImage"
            class="relative inline-flex items-center h-6 w-11  cursor-pointer transition-colors"
            :class="filters.hasImage ? 'bg-gold-light dark:bg-gold' : 'bg-accent'"
          >
            <span 
              class="inline-block w-4 h-4 transform bg-white  transition-transform"
              :class="filters.hasImage ? 'translate-x-6' : 'translate-x-1'"
            ></span>
          </div>
        </label>
      </div>

      <!-- Tags Filter -->
      <div class="filter-section">
        <label class="block text-base font-medium text-dark dark:text-light mb-3">Tags</label>
        
        <!-- Selected Tags (always visible) -->
        <div v-if="selectedTags.length > 0" class="mb-3">
          <div class="flex flex-wrap gap-1">
            <button
              v-for="tag in selectedTags"
              :key="tag.id"
              @click="removeTag(tag.id)"
              class="inline-flex items-center gap-1 px-2 py-1 text-sm bg-gold-light dark:bg-gold text-white hover:bg-gold-hover-light dark:hover:bg-gold-hover transition-colors cursor-pointer"
            >
              {{ tag.name }}
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Search Input -->
        <div class="mb-3">
          <input
            v-model="searchTags"
            type="text"
            placeholder="Search tags to add..."
            class="w-full px-3 py-2 text-sm border border bg-white dark:bg-secondary text-dark dark:text-light focus:outline-none focus:border dark:focus:border-gold"
          />
        </div>

        <!-- Search Results (only when searching) -->
        <div v-if="searchTags" class="max-h-32 overflow-y-auto space-y-1">
          <button
            v-for="tag in searchResults"
            :key="tag.id"
            @click="addTag(tag.id)"
            class="flex items-center gap-2 w-full p-1 hover:bg-light dark:hover:bg-accent cursor-pointer transition-colors text-left"
            :class="{ 'opacity-50': filters.tagIds.includes(tag.id) }"
            :disabled="filters.tagIds.includes(tag.id)"
          >
            <span class="text-sm text-dark dark:text-light">{{ tag.name }}</span>
            <span v-if="filters.tagIds.includes(tag.id)" class="text-sm text-gold-light dark:text-gold">(selected)</span>
          </button>
          <div v-if="searchResults.length === 0" class="p-2 text-sm text-gold-light dark:text-gold">
            No tags found for "{{ searchTags }}"
          </div>
        </div>
      </div>

      <!-- Difficulty Filter -->
      <div class="filter-section">
        <label class="block text-base font-medium text-dark dark:text-light mb-3">Difficulty</label>
        <div class="flex gap-2">
          <button
            v-for="level in [1, 2, 3]"
            :key="level"
            @click="toggleDifficulty(level)"
            class="flex-1 py-2 px-3 text-base font-medium  border-2 transition-colors cursor-pointer"
            :class="filters.difficulty.includes(level) 
              ? 'bg-gold-light dark:bg-gold text-white border' 
              : 'bg-light dark:bg-accent text-dark dark:text-light border hover:bg-accent dark:hover:bg-secondary'"
          >
            {{ level === 1 ? 'Easy' : level === 2 ? 'Medium' : 'Hard' }}
          </button>
        </div>
      </div>

      <!-- Time Filters -->
      <div class="filter-section">
        <label class="block text-base font-medium text-dark dark:text-light mb-3">Time Limits (minutes)</label>
        
        <!-- Cooking Time -->
        <div class="mb-4">
          <div class="flex justify-between text-sm text-dark dark:text-light mb-1">
            <span>Cooking Time</span>
            <span>{{ filters.maxCookingTime || 'No limit' }} min</span>
          </div>
          <div class="flex gap-2 mb-2">
            <button
              v-for="preset in timePresets"
              :key="'cooking-' + preset"
              @click="filters.maxCookingTime = preset"
              class="px-2 py-1 text-sm  border cursor-pointer"
              :class="filters.maxCookingTime === preset ? 'bg-gold-light dark:bg-gold text-white border' : 'bg-light dark:bg-accent hover:bg-accent dark:hover:bg-secondary text-dark dark:text-light border'"
            >
              {{ preset }}m
            </button>
            <button
              @click="filters.maxCookingTime = null"
              class="px-2 py-1 text-sm  border cursor-pointer"
              :class="!filters.maxCookingTime ? 'bg-gold-light dark:bg-gold text-white border' : 'bg-light dark:bg-accent hover:bg-accent dark:hover:bg-secondary text-dark dark:text-light border'"
            >
              No limit
            </button>
          </div>
        </div>

        <!-- Preparation Time -->
        <div class="mb-4">
          <div class="flex justify-between text-sm text-dark dark:text-light mb-1">
            <span>Prep Time</span>
            <span>{{ filters.maxPrepTime || 'No limit' }} min</span>
          </div>
          <div class="flex gap-2 mb-2">
            <button
              v-for="preset in prepTimePresets"
              :key="'prep-' + preset"
              @click="filters.maxPrepTime = preset"
              class="px-2 py-1 text-sm  border cursor-pointer"
              :class="filters.maxPrepTime === preset ? 'bg-gold-light dark:bg-gold text-white border' : 'bg-light dark:bg-accent hover:bg-accent dark:hover:bg-secondary text-dark dark:text-light border'"
            >
              {{ preset }}m
            </button>
            <button
              @click="filters.maxPrepTime = null"
              class="px-2 py-1 text-sm  border cursor-pointer"
              :class="!filters.maxPrepTime ? 'bg-gold-light dark:bg-gold text-white border' : 'bg-light dark:bg-accent hover:bg-accent dark:hover:bg-secondary text-dark dark:text-light border'"
            >
              No limit
            </button>
          </div>
        </div>

        <!-- Total Time -->
        <div>
          <div class="flex justify-between text-sm text-dark dark:text-light mb-1">
            <span>Total Time</span>
            <span>{{ filters.maxTotalTime || 'No limit' }} min</span>
          </div>
          <div class="flex gap-2 mb-2">
            <button
              v-for="preset in totalTimePresets"
              :key="'total-' + preset"
              @click="filters.maxTotalTime = preset"
              class="px-2 py-1 text-sm  border cursor-pointer"
              :class="filters.maxTotalTime === preset ? 'bg-gold-light dark:bg-gold text-white border' : 'bg-light dark:bg-accent hover:bg-accent dark:hover:bg-secondary text-dark dark:text-light border'"
            >
              {{ preset }}m
            </button>
            <button
              @click="filters.maxTotalTime = null"
              class="px-2 py-1 text-sm  border cursor-pointer"
              :class="!filters.maxTotalTime ? 'bg-gold-light dark:bg-gold text-white border' : 'bg-light dark:bg-accent hover:bg-accent dark:hover:bg-secondary text-dark dark:text-light border'"
            >
              No limit
            </button>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-2 pt-4 border-t border">
        <button
          @click="resetFilters"
          class="flex-1 py-2 px-4 text-base font-medium text-dark dark:text-light bg-light dark:bg-accent hover:bg-accent dark:hover:bg-secondary  transition-colors cursor-pointer"
        >
          Reset to Defaults
        </button>
        <button
          @click="applyFilters"
          class="flex-1 py-2 px-4 text-base font-medium text-white bg-gold-light dark:bg-gold hover:bg-gold-hover-light dark:hover:bg-gold-hover  transition-colors cursor-pointer"
        >
          Apply Filters
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { tagService } from '@/services/tagService'

interface RecommendationFilters {
  minRating: number
  minVotes: number
  maxVotes: number | null
  hasImage: boolean
  tagIds: string[]
  difficulty: number[]
  minCookingTime: number | null
  maxCookingTime: number | null
  minPrepTime: number | null
  maxPrepTime: number | null
  minTotalTime: number | null
  maxTotalTime: number | null
}

const emit = defineEmits<{
  'filters-changed': [filters: RecommendationFilters]
}>()

const showFilters = ref(false)
const availableTags = ref<Array<{ id: string; name: string }>>([])
const searchTags = ref('')

// Default filters - more permissive for demo purposes, user can tighten them
const defaultFilters: RecommendationFilters = {
  minRating: 0.0,  // Start permissive, user can increase
  minVotes: 0,     // Start permissive, user can increase  
  maxVotes: null,
  hasImage: true,  // Only recipes with images by default
  tagIds: [],
  difficulty: [1, 2, 3], // All difficulties allowed by default
  minCookingTime: null,
  maxCookingTime: null,
  minPrepTime: null,
  maxPrepTime: null,
  minTotalTime: null,
  maxTotalTime: null
}

// Load filters from localStorage or use defaults
const loadFiltersFromStorage = (): RecommendationFilters => {
  try {
    const stored = localStorage.getItem('recommendationFilters')
    if (stored) {
      const parsed = JSON.parse(stored)
      // Merge with defaults to handle any missing properties
      return { ...defaultFilters, ...parsed }
    }
  } catch (error) {
    console.warn('Failed to load filters from localStorage:', error)
  }
  return { ...defaultFilters }
}

const filters = ref<RecommendationFilters>(loadFiltersFromStorage())

// Preset values
const votePresets = [0, 100, 500, 1000, 2000]
const timePresets = [15, 30, 60, 120]
const prepTimePresets = [15, 30, 45, 60]
const totalTimePresets = [30, 60, 120, 180]

// Computed properties
const selectedTags = computed(() => {
  if (!availableTags.value || !filters.value.tagIds) return []
  return availableTags.value.filter(tag => filters.value.tagIds.includes(tag.id))
})

const searchResults = computed(() => {
  if (!searchTags.value || !availableTags.value) {
    return []
  }
  return availableTags.value.filter(tag => 
    tag.name.toLowerCase().includes(searchTags.value.toLowerCase())
  ).slice(0, 20) // Limit to 20 results
})

const activeFiltersCount = computed(() => {
  let count = 0
  
  // Check if rating is different from default
  if (filters.value.minRating !== defaultFilters.minRating) {
    count++
  }
  
  // Check if votes is different from default
  if (filters.value.minVotes !== defaultFilters.minVotes) {
    count++
  }
  
  // Check if has image is different from default
  if (filters.value.hasImage !== defaultFilters.hasImage) {
    count++
  }
  
  // Check if difficulty is different from default
  if (filters.value.difficulty.length !== 3) {
    count++
  }
  
  // Check if tags are selected
  if (filters.value.tagIds.length > 0) {
    count++
  }
  
  // Check time filters
  if (filters.value.maxCookingTime !== null) count++
  if (filters.value.maxPrepTime !== null) count++
  if (filters.value.maxTotalTime !== null) count++
  
  return count
})

// Methods
const toggleDifficulty = (level: number) => {
  const index = filters.value.difficulty.indexOf(level)
  if (index > -1) {
    filters.value.difficulty.splice(index, 1)
  } else {
    filters.value.difficulty.push(level)
  }
  filters.value.difficulty.sort()
}

const addTag = (tagId: string) => {
  if (!filters.value.tagIds.includes(tagId)) {
    filters.value.tagIds.push(tagId)
  }
  // Clear search after adding
  searchTags.value = ''
}

const removeTag = (tagId: string) => {
  const index = filters.value.tagIds.indexOf(tagId)
  if (index > -1) {
    filters.value.tagIds.splice(index, 1)
  }
}

const resetFilters = () => {
  filters.value = {
    ...defaultFilters,
    difficulty: [...defaultFilters.difficulty], // Create a new array copy
    tagIds: [...defaultFilters.tagIds] // Also copy tagIds array
  }
  applyFilters()
}

const applyFilters = () => {
  // Save filters to localStorage
  try {
    localStorage.setItem('recommendationFilters', JSON.stringify(filters.value))
  } catch (error) {
    console.warn('Failed to save filters to localStorage:', error)
  }
  
  // Collapse the filter panel after applying
  showFilters.value = false
  
  emit('filters-changed', { ...filters.value })
}

// Fetch available tags on component mount
onMounted(async () => {
  try {
    const tagsResponse = await tagService.getTags()
    availableTags.value = tagsResponse || []
  } catch (error) {
    console.warn('Failed to fetch tags:', error)
  }
  
  // Emit the initial filters after component is mounted and tags are loaded
  // This ensures the parent gets the persisted filters for the initial load
  emit('filters-changed', { ...filters.value })
})
</script>

<style scoped>
.filter-section {
  border-bottom: 1px solid var(--color-accent);
  padding-bottom: 1rem;
}

.filter-section:last-of-type {
  border-bottom: none;
  padding-bottom: 0;
}

/* Custom slider styling */
.slider::-webkit-slider-thumb {
  appearance: none;
  width: 1rem;
  height: 1rem;
  background-color: var(--color-gold-light);
  cursor: pointer;
}

.slider::-moz-range-thumb {
  width: 1rem;
  height: 1rem;
  background-color: var(--color-gold-light);
  cursor: pointer;
  border: none;
}
</style>