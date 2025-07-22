import api from './api'

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
      ...(tagFilter.length ? tagFilter.reduce((acc, tag) => ({ ...acc, [`tags`]: tag }), {}) : {})
      // tags: tagFilter.length ? tagFilter : undefined
    }

    const response = await api.get('/recipes/', { params })
    return response.data
  },

  async getRecipe(id: string) {
    const response = await api.get(`/recipes/${id}`)
    return response.data
  },

  async getRecommendations(lockedIds?: string[], filters?: {
    minRating?: number
    minVotes?: number
    maxVotes?: number
    hasImage?: boolean
    tagIds?: string[]
    difficulty?: number[]
  }) {
    const params: any = {}
    
    if (lockedIds && lockedIds.length > 0) {
      params.locked_ids = lockedIds.join(',')
    }
    
    if (filters) {
      if (filters.minRating !== undefined) params.min_rating = filters.minRating
      if (filters.minVotes !== undefined) params.min_votes = filters.minVotes
      if (filters.maxVotes !== undefined) params.max_votes = filters.maxVotes
      if (filters.hasImage !== undefined) params.has_image = filters.hasImage
      if (filters.tagIds && filters.tagIds.length > 0) params.tag_ids = filters.tagIds.join(',')
      if (filters.difficulty && filters.difficulty.length > 0) params.difficulty = filters.difficulty.join(',')
    }

    const response = await api.get('/recipes/recommendations', { params })
    return response.data
  }
}
