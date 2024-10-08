import api from './api'

export const recipeService = {
  async getRecipes(page = 1, pageSize = 20) {
    const response = await api.get('/recipes/', {
      params: { page, page_size: pageSize }
    })
    return response.data
  },

  async getRecipe(id: string) {
    const response = await api.get(`/recipes/${id}`)
    return response.data
  }

  // Add more methods for other API endpoints
}
