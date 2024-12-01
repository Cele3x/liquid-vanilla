import api from './api'

export const tagService = {
  async getTags() {
    const response = await api.get('/tags/')
    return response.data
  }
}
