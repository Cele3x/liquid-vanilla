import api from './api'

export const categoryService = {
  async getCategories() {
    const response = await api.get('/categories/')
    return response.data
  },

  async getCategory(id: string) {
    const response = await api.get(`/categories/${id}`)
    return response.data
  },

  async createCategory(category: { name: string; description: string }) {
    const response = await api.post('/categories/', category)
    return response.data
  },

  async updateCategory(id: string, category: { name: string; description: string }) {
    const response = await api.put(`/categories/${id}`, category)
    return response.data
  },

  async deleteCategory(id: string) {
    const response = await api.delete(`/categories/${id}`)
    return response.data
  }
}