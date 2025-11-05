<template>
  <div class="recommendation-filters">
    <!-- Filter Toggle Button -->
    <button
      @click="showFilters = !showFilters"
      class="w-full mb-4 flex items-center justify-between bg-light dark:bg-secondary hover:bg-gold-light/10 dark:hover:bg-gold/10 px-4 py-3 transition-colors text-dark dark:text-light cursor-pointer border border-transparent hover:border-gold-light dark:hover:border-gold"
      :class="{
        'bg-gold-light/20 dark:bg-gold/20 border-2 border-gold-light dark:border-gold':
          activeFiltersCount > 0
      }"
    >
      <div class="flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707v4.586l-4-2V12a1 1 0 00-.293-.707L3.293 4.707A1 1 0 013 4z"
          />
        </svg>
        <span class="font-medium">Rezept Filter</span>
        <span
          v-if="activeFiltersCount > 0"
          class="bg-gold-light dark:bg-gold text-white text-sm px-2 py-1"
        >
          {{ activeFiltersCount }}
        </span>
      </div>
      <svg
        class="w-5 h-5 transition-transform duration-200"
        :class="{ 'rotate-180': showFilters }"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- Filter Panel -->
    <div v-show="showFilters" class="bg-white dark:bg-secondary border border p-4 space-y-6">
      <!-- Rating Filter -->
      <div class="filter-section">
        <label class="block text-base font-medium text-dark dark:text-light mb-3">
          Mindestbewertung: {{ filters.minRating }}★
        </label>
        <div class="flex items-center gap-2 mb-2">
          <button
            v-for="rating in [0, 3.0, 3.5, 4.0, 4.5]"
            :key="rating"
            @click="filters.minRating = rating"
            class="px-3 py-1 text-sm border transition-colors cursor-pointer"
            :class="
              filters.minRating === rating
                ? 'bg-gold-light dark:bg-gold text-white border-gold-light dark:border-gold'
                : 'bg-gold-light/10 dark:bg-gold/10 hover:bg-gold-light/20 dark:hover:bg-gold/20 border-gray-300 dark:border-gold text-dark dark:text-gold'
            "
          >
            {{ rating === 0 ? 'Alle' : rating + '★' }}
          </button>
        </div>
        <input
          v-model.number="filters.minRating"
          type="range"
          min="0"
          max="5"
          step="0.1"
          class="w-full h-2 bg-gold-light dark:bg-gold appearance-none cursor-pointer slider"
        />
      </div>

      <!-- Votes Filter -->
      <div class="filter-section">
        <label class="block text-base font-medium text-dark dark:text-light mb-3">
          Mindest-Bewertungen: {{ filters.minVotes }}
        </label>
        <div class="flex items-center gap-2 mb-2">
          <button
            v-for="preset in votePresets"
            :key="preset"
            @click="filters.minVotes = preset"
            class="px-3 py-1 text-sm border transition-colors cursor-pointer"
            :class="
              filters.minVotes === preset
                ? 'bg-gold-light dark:bg-gold text-white border-gold-light dark:border-gold'
                : 'bg-gold-light/10 dark:bg-gold/10 hover:bg-gold-light/20 dark:hover:bg-gold/20 border-gray-300 dark:border-gold text-dark dark:text-gold'
            "
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
          class="w-full h-2 bg-gold-light dark:bg-gold appearance-none cursor-pointer slider"
        />
      </div>

      <!-- Has Image Toggle -->
      <div class="filter-section">
        <label class="flex items-center justify-between">
          <span class="text-base font-medium text-dark dark:text-light"
            >Nur Rezepte mit Bildern</span
          >
          <div
            @click="filters.hasImage = !filters.hasImage"
            class="relative inline-flex items-center h-6 w-11 cursor-pointer transition-colors"
            :class="filters.hasImage ? 'bg-gold-light dark:bg-gold' : 'bg-accent'"
          >
            <span
              class="inline-block w-4 h-4 transform bg-white transition-transform"
              :class="filters.hasImage ? 'translate-x-6' : 'translate-x-1'"
            ></span>
          </div>
        </label>
      </div>

      <!-- Tags Filter -->
      <div class="filter-section">
        <label class="block text-base font-medium text-dark dark:text-light mb-3">Kategorien</label>

        <!-- Selected Include Tags -->
        <div v-if="selectedIncludeTags.length > 0" class="mb-3">
          <div class="text-sm text-dark dark:text-light mb-1 flex items-center gap-2">
            <span>Muss diese Kategorien haben:</span>
            <span class="text-xs text-gold-light dark:text-gold"
              >({{ selectedIncludeTags.length }})</span
            >
          </div>
          <div class="flex flex-wrap gap-1">
            <div
              v-for="tag in selectedIncludeTags"
              :key="'include-' + tag.id"
              class="inline-flex items-center gap-1 px-2 py-1 text-sm bg-green-600 dark:bg-green-700 text-white transition-colors group"
            >
              {{ tag.name }}
              <button
                @click="removeTag(tag.id, 'include')"
                class="hover:bg-green-700 dark:hover:bg-green-800 p-0.5 transition-colors cursor-pointer"
                title="Aus Einschluss-Liste entfernen"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Selected Exclude Tags -->
        <div v-if="selectedExcludeTags.length > 0" class="mb-3">
          <div class="text-sm text-dark dark:text-light mb-1 flex items-center gap-2">
            <span>Darf NICHT diese Kategorien haben:</span>
            <span class="text-xs text-red-500 dark:text-red-400"
              >({{ selectedExcludeTags.length }})</span
            >
          </div>
          <div class="flex flex-wrap gap-1">
            <div
              v-for="tag in selectedExcludeTags"
              :key="'exclude-' + tag.id"
              class="inline-flex items-center gap-1 px-2 py-1 text-sm bg-red-800 dark:bg-red-900 text-white transition-colors group"
            >
              {{ tag.name }}
              <button
                @click="removeTag(tag.id, 'exclude')"
                class="hover:bg-red-900 dark:hover:bg-red-950 p-0.5 transition-colors cursor-pointer"
                title="Aus Ausschluss-Liste entfernen"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Include Tags Search -->
        <div class="mb-4">
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg
                class="h-4 w-4 text-gold-light dark:text-gold"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                />
              </svg>
            </div>
            <input
              v-model="searchIncludeTags"
              type="text"
              placeholder="✓ Kategorien hinzufügen die Rezepte haben MÜSSEN (z.B. Hauptspeise, vegetarisch)..."
              class="w-full pl-10 pr-3 py-2 text-sm border border-gray-300 dark:border-gold bg-white dark:bg-secondary text-dark dark:text-light focus:outline-none focus:border-gold dark:focus:border-gold focus:ring-1 focus:ring-gold-light dark:focus:ring-gold"
            />
          </div>

          <!-- Include Search Results -->
          <div
            v-if="searchIncludeTags && includeSearchResults.length > 0"
            class="mt-2 max-h-32 overflow-y-auto space-y-1 border border-gray-300 dark:border-gold bg-white dark:bg-secondary p-2"
          >
            <button
              v-for="tag in includeSearchResults"
              :key="'include-search-' + tag.id"
              @click="addIncludeTag(tag.id)"
              class="flex items-center gap-2 w-full p-2 hover:bg-gold-light/10 dark:hover:bg-gold/10 cursor-pointer transition-colors text-left border border-transparent hover:border-gold-light dark:hover:border-gold"
            >
              <span class="text-sm text-dark dark:text-light font-medium">{{ tag.name }}</span>
              <span class="text-xs text-gray-600 dark:text-gold/70">→ hinzufügen</span>
            </button>
          </div>
          <div
            v-if="searchIncludeTags && includeSearchResults.length === 0"
            class="mt-2 p-2 text-sm text-gold-light dark:text-gold border border-gray-300 dark:border-gold bg-white dark:bg-secondary"
          >
            Keine Kategorien gefunden für "{{ searchIncludeTags }}"
          </div>
        </div>

        <!-- Exclude Tags Search -->
        <div class="mb-4">
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg
                class="h-4 w-4 text-red-500 dark:text-red-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M20 12H4"
                />
              </svg>
            </div>
            <input
              v-model="searchExcludeTags"
              type="text"
              placeholder="✗ Kategorien hinzufügen die Rezepte NICHT haben dürfen (z.B. süß, Fleisch)..."
              class="w-full pl-10 pr-3 py-2 text-sm border border-gray-300 dark:border-gold bg-white dark:bg-secondary text-dark dark:text-light focus:outline-none focus:border-gold dark:focus:border-gold focus:ring-1 focus:ring-gold-light dark:focus:ring-gold"
            />
          </div>

          <!-- Exclude Search Results -->
          <div
            v-if="searchExcludeTags && excludeSearchResults.length > 0"
            class="mt-2 max-h-32 overflow-y-auto space-y-1 border border-gray-300 dark:border-gold bg-white dark:bg-secondary p-2"
          >
            <button
              v-for="tag in excludeSearchResults"
              :key="'exclude-search-' + tag.id"
              @click="addExcludeTag(tag.id)"
              class="flex items-center gap-2 w-full p-2 hover:bg-red-500/10 dark:hover:bg-red-500/10 cursor-pointer transition-colors text-left border border-transparent hover:border-red-500 dark:hover:border-red-400"
            >
              <span class="text-sm text-dark dark:text-light font-medium">{{ tag.name }}</span>
              <span class="text-xs text-gray-600 dark:text-red-400/70">→ ausschließen</span>
            </button>
          </div>
          <div
            v-if="searchExcludeTags && excludeSearchResults.length === 0"
            class="mt-2 p-2 text-sm text-red-500 dark:text-red-400 border border-gray-300 dark:border-gold bg-white dark:bg-secondary"
          >
            Keine Kategorien gefunden für "{{ searchExcludeTags }}"
          </div>
        </div>
      </div>

      <!-- Difficulty Filter -->
      <div class="filter-section">
        <label class="block text-base font-medium text-dark dark:text-light mb-3"
          >Schwierigkeit</label
        >
        <div class="flex gap-2">
          <button
            v-for="level in [1, 2, 3]"
            :key="level"
            @click="toggleDifficulty(level)"
            class="flex-1 py-2 px-3 text-base font-medium border-2 transition-colors cursor-pointer"
            :class="
              filters.difficulty.includes(level)
                ? 'bg-gold-light dark:bg-gold text-white border-gold-light dark:border-gold'
                : 'bg-gold-light/10 dark:bg-gold/10 text-dark dark:text-gold border-gray-300 dark:border-gold hover:bg-gold-light/20 dark:hover:bg-gold/20'
            "
          >
            {{ level === 1 ? 'Einfach' : level === 2 ? 'Mittel' : 'Schwer' }}
          </button>
        </div>
      </div>

      <!-- Time Filters -->
      <div class="filter-section">
        <label class="block text-base font-medium text-dark dark:text-light mb-3"
          >Zeitlimits (Minuten)</label
        >

        <!-- Cooking Time -->
        <div class="mb-4">
          <div class="flex justify-between text-sm text-dark dark:text-light mb-1">
            <span>Kochzeit</span>
            <span>{{ filters.maxCookingTime || 'Kein Limit' }} min</span>
          </div>
          <div class="flex gap-2 mb-2">
            <button
              v-for="preset in timePresets"
              :key="'cooking-' + preset"
              @click="filters.maxCookingTime = preset"
              class="px-2 py-1 text-sm border cursor-pointer"
              :class="
                filters.maxCookingTime === preset
                  ? 'bg-gold-light dark:bg-gold text-white border-gold-light dark:border-gold'
                  : 'bg-gold-light/10 dark:bg-gold/10 hover:bg-gold-light/20 dark:hover:bg-gold/20 text-dark dark:text-gold border-gray-300 dark:border-gold'
              "
            >
              {{ preset }}m
            </button>
            <button
              @click="filters.maxCookingTime = null"
              class="px-2 py-1 text-sm border cursor-pointer"
              :class="
                !filters.maxCookingTime
                  ? 'bg-gold-light dark:bg-gold text-white border-gold-light dark:border-gold'
                  : 'bg-gold-light/10 dark:bg-gold/10 hover:bg-gold-light/20 dark:hover:bg-gold/20 text-dark dark:text-gold border-gray-300 dark:border-gold'
              "
            >
              Kein Limit
            </button>
          </div>
        </div>

        <!-- Preparation Time -->
        <div class="mb-4">
          <div class="flex justify-between text-sm text-dark dark:text-light mb-1">
            <span>Vorbereitungszeit</span>
            <span>{{ filters.maxPrepTime || 'Kein Limit' }} min</span>
          </div>
          <div class="flex gap-2 mb-2">
            <button
              v-for="preset in prepTimePresets"
              :key="'prep-' + preset"
              @click="filters.maxPrepTime = preset"
              class="px-2 py-1 text-sm border cursor-pointer"
              :class="
                filters.maxPrepTime === preset
                  ? 'bg-gold-light dark:bg-gold text-white border-gold-light dark:border-gold'
                  : 'bg-gold-light/10 dark:bg-gold/10 hover:bg-gold-light/20 dark:hover:bg-gold/20 text-dark dark:text-gold border-gray-300 dark:border-gold'
              "
            >
              {{ preset }}m
            </button>
            <button
              @click="filters.maxPrepTime = null"
              class="px-2 py-1 text-sm border cursor-pointer"
              :class="
                !filters.maxPrepTime
                  ? 'bg-gold-light dark:bg-gold text-white border-gold-light dark:border-gold'
                  : 'bg-gold-light/10 dark:bg-gold/10 hover:bg-gold-light/20 dark:hover:bg-gold/20 text-dark dark:text-gold border-gray-300 dark:border-gold'
              "
            >
              Kein Limit
            </button>
          </div>
        </div>

        <!-- Total Time -->
        <div>
          <div class="flex justify-between text-sm text-dark dark:text-light mb-1">
            <span>Gesamtzeit</span>
            <span>{{ filters.maxTotalTime || 'Kein Limit' }} min</span>
          </div>
          <div class="flex gap-2 mb-2">
            <button
              v-for="preset in totalTimePresets"
              :key="'total-' + preset"
              @click="filters.maxTotalTime = preset"
              class="px-2 py-1 text-sm border cursor-pointer"
              :class="
                filters.maxTotalTime === preset
                  ? 'bg-gold-light dark:bg-gold text-white border-gold-light dark:border-gold'
                  : 'bg-gold-light/10 dark:bg-gold/10 hover:bg-gold-light/20 dark:hover:bg-gold/20 text-dark dark:text-gold border-gray-300 dark:border-gold'
              "
            >
              {{ preset }}m
            </button>
            <button
              @click="filters.maxTotalTime = null"
              class="px-2 py-1 text-sm border cursor-pointer"
              :class="
                !filters.maxTotalTime
                  ? 'bg-gold-light dark:bg-gold text-white border-gold-light dark:border-gold'
                  : 'bg-gold-light/10 dark:bg-gold/10 hover:bg-gold-light/20 dark:hover:bg-gold/20 text-dark dark:text-gold border-gray-300 dark:border-gold'
              "
            >
              Kein Limit
            </button>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-2 pt-4 border-t border">
        <button
          @click="resetFilters"
          class="flex-1 py-2 px-4 text-base font-medium text-dark dark:text-gold bg-gold-light/10 dark:bg-gold/10 hover:bg-gold-light/20 dark:hover:bg-gold/20 border border-gray-300 dark:border-gold transition-colors cursor-pointer"
        >
          Zurücksetzen
        </button>
        <button
          @click="applyFilters"
          class="flex-1 py-2 px-4 text-base font-medium text-white bg-gold-light dark:bg-gold hover:bg-gold-hover-light dark:hover:bg-gold-hover border border-gold-light dark:border-gold transition-colors cursor-pointer"
        >
          Filter anwenden
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
  tags: string[]
  excludeTags: string[]
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
const searchIncludeTags = ref('')
const searchExcludeTags = ref('')

// Default filters - more permissive for demo purposes, user can tighten them
const defaultFilters: RecommendationFilters = {
  minRating: 0.0, // Start permissive, user can increase
  minVotes: 0, // Start permissive, user can increase
  maxVotes: null,
  hasImage: true, // Only recipes with images by default
  tags: [],
  excludeTags: [],
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
    console.warn('Fehler beim Laden der Filter aus dem localStorage:', error)
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
const selectedIncludeTags = computed(() => {
  if (!availableTags.value || !filters.value.tags) return []
  return availableTags.value.filter((tag) => filters.value.tags.includes(tag.id))
})

const selectedExcludeTags = computed(() => {
  if (!availableTags.value || !filters.value.excludeTags) return []
  return availableTags.value.filter((tag) => filters.value.excludeTags.includes(tag.id))
})

const includeSearchResults = computed(() => {
  if (!searchIncludeTags.value || !availableTags.value) {
    return []
  }
  return availableTags.value
    .filter(
      (tag) =>
        tag.name.toLowerCase().includes(searchIncludeTags.value.toLowerCase()) &&
        !filters.value.tags.includes(tag.id) // Don't show already selected tags
    )
    .slice(0, 10) // Limit to 10 results per search
})

const excludeSearchResults = computed(() => {
  if (!searchExcludeTags.value || !availableTags.value) {
    return []
  }
  return availableTags.value
    .filter(
      (tag) =>
        tag.name.toLowerCase().includes(searchExcludeTags.value.toLowerCase()) &&
        !filters.value.excludeTags.includes(tag.id) // Don't show already selected tags
    )
    .slice(0, 10) // Limit to 10 results per search
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
  if (filters.value.tags.length > 0 || filters.value.excludeTags.length > 0) {
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

const addIncludeTag = (tagId: string) => {
  if (!filters.value.tags.includes(tagId)) {
    filters.value.tags.push(tagId)
    // Remove from exclude list if it was there to avoid conflicts
    const excludeIndex = filters.value.excludeTags.indexOf(tagId)
    if (excludeIndex > -1) {
      filters.value.excludeTags.splice(excludeIndex, 1)
    }
  }
  // Clear search after adding
  searchIncludeTags.value = ''
}

const addExcludeTag = (tagId: string) => {
  if (!filters.value.excludeTags.includes(tagId)) {
    filters.value.excludeTags.push(tagId)
    // Remove from include list if it was there to avoid conflicts
    const includeIndex = filters.value.tags.indexOf(tagId)
    if (includeIndex > -1) {
      filters.value.tags.splice(includeIndex, 1)
    }
  }
  // Clear search after adding
  searchExcludeTags.value = ''
}

const removeTag = (tagId: string, type: 'include' | 'exclude') => {
  if (type === 'include') {
    const index = filters.value.tags.indexOf(tagId)
    if (index > -1) {
      filters.value.tags.splice(index, 1)
    }
  } else {
    const index = filters.value.excludeTags.indexOf(tagId)
    if (index > -1) {
      filters.value.excludeTags.splice(index, 1)
    }
  }
}

const resetFilters = () => {
  filters.value = {
    ...defaultFilters,
    difficulty: [...defaultFilters.difficulty], // Create a new array copy
    tags: [...defaultFilters.tags], // Also copy tags array
    excludeTags: [...defaultFilters.excludeTags] // Copy excludeTags array
  }
  applyFilters()
}

const isTagSelected = (tagId: string) => {
  return filters.value.tags.includes(tagId) || filters.value.excludeTags.includes(tagId)
}

const applyFilters = () => {
  // Save filters to localStorage
  try {
    localStorage.setItem('recommendationFilters', JSON.stringify(filters.value))
  } catch (error) {
    console.warn('Fehler beim Speichern der Filter im localStorage:', error)
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
    console.warn('Fehler beim Laden der Kategorien:', error)
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
