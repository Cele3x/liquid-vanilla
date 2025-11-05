import api from './api'

export const tagService = {
  async getTags(essentialOnly: boolean = false) {
    const params = essentialOnly ? { essential_only: true } : {}
    const response = await api.get('/tags/', { params })
    return response.data
  }
}
