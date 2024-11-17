import api from './api'

export const recipeService = {
  async getRecipes(page: number = 1, pageSize: number = 20, query: string = '') {
    const response = await api.get('/recipes/', {
      params: { page, page_size: pageSize, search: query }
    })
    return response.data
  },

  async getRecipe(id: string) {
    const response = await api.get(`/recipes/${id}`)
    return response.data
  }
}
