import api from './api'
import type { RecommendationFilters } from '@/types/recommendations'

interface GetRecipesParams {
  page?: number
  page_size?: number
  search?: string
  tags?: string[]
}

export const recipeService = {
  async getRecipes(
    page: number = 1,
    pageSize: number = 20,
    query: string = '',
    tagFilter: string[] = []
  ) {
    const params: GetRecipesParams = {
      page,
      page_size: pageSize,
      search: query || undefined,
      tags: tagFilter.length ? tagFilter : undefined
    }

    const response = await api.get('/recipes/', { params })
    return response.data
  },

  async getRecipe(id: string) {
    const response = await api.get(`/recipes/${id}`)
    return response.data
  },

  async getRecommendations(lockedIds?: string[], filters?: Partial<RecommendationFilters>) {
    const params: Record<string, string | number | boolean> = {}

    if (lockedIds && lockedIds.length > 0) {
      params.locked_ids = lockedIds.join(',')
    }

    if (filters) {
      if (filters.minScore !== undefined) params.min_score = filters.minScore
      if (filters.minVotes !== undefined) params.min_votes = filters.minVotes
      // maxVotes is nullable: null means "no upper bound", so it is left off
      if (filters.maxVotes !== undefined && filters.maxVotes !== null)
        params.max_votes = filters.maxVotes
      if (filters.hasImage !== undefined) params.has_image = filters.hasImage
      if (filters.tagIds && filters.tagIds.length > 0) params.tag_ids = filters.tagIds.join(',')
      if (filters.difficulty && filters.difficulty.length > 0)
        params.difficulty = filters.difficulty.join(',')
      if (filters.sources && filters.sources.length > 0) params.sources = filters.sources.join(',')
    }

    const response = await api.get('/recipes/recommendations', { params })
    return response.data
  },

  async getSources(): Promise<string[]> {
    const response = await api.get('/recipes/sources')
    return response.data.sources ?? []
  }
}
