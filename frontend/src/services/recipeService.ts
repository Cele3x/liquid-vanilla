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

  async getRecommendations() {
    const response = await api.get('/recipes/recommendations')
    return response.data
  }
}
