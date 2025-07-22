// stores/recipeStore.ts
import { defineStore } from 'pinia'
import { recipeService } from '@/services/recipeService'

interface Recipe {
  id: string
  title: string
  rating: number
  sourceRatingVotes: number
  previewImageUrlTemplate: string
  cachedImageUrl?: string
  defaultImageUrl: string
  sourceUrl: string
  tagIds: string[]
}

export const useRecipeStore = defineStore('recipe', {
  state: () => ({
    recipes: [] as Recipe[],
    page: 1,
    pageSize: 20,
    loading: false,
    allLoaded: false,
    searchQuery: '',
    tagFilter: [] as string[]
  }),

  actions: {
    async fetchRecipes() {
      if (this.loading || this.allLoaded) return

      this.loading = true
      try {
        const data = await recipeService.getRecipes(
          this.page,
          this.pageSize,
          this.searchQuery,
          this.tagFilter
        )
        const newRecipes = data.recipes.map((recipe: Recipe) => ({
          ...recipe,
          defaultImageUrl:
            recipe.cachedImageUrl ||
            (recipe.previewImageUrlTemplate
              ? recipe.previewImageUrlTemplate.replace('<format>', 'crop-360x240')
              : '')
        }))
        this.recipes.push(...newRecipes)
        this.page++
        if (newRecipes.length < this.pageSize) {
          this.allLoaded = true
        }
      } catch (error) {
        console.error('Failed to fetch recipes:', error)
      } finally {
        this.loading = false
      }
    },

    setSearchQuery(query: string) {
      this.searchQuery = query
      this.recipes = []
      this.page = 1
      this.allLoaded = false
      this.fetchRecipes()
    },

    setTagFilter(tags: string[]) {
      this.tagFilter = tags
      this.recipes = []
      this.page = 1
      this.allLoaded = false
      this.fetchRecipes()
    },

    resetStore() {
      this.recipes = []
      this.page = 1
      this.allLoaded = false
      this.searchQuery = ''
      this.tagFilter = []
    }
  },

  getters: {
    getRecipeById: (state) => {
      return (id: string) => state.recipes.find((recipe) => recipe.id === id)
    },
    hasRecipes: (state) => state.recipes.length > 0
  }
})
