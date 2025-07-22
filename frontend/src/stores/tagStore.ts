import { defineStore } from 'pinia'
import { tagService } from '@/services/tagService'

interface Tag {
  id: string
  name: string
}

export const useTagStore = defineStore('tag', {
  state: () => ({
    tags: [] as Tag[],
    loading: false
  }),
  actions: {
    async fetchTags() {
      if (this.loading) return

      this.loading = true
      try {
        const data = await tagService.getTags()
        this.tags = data
      } catch (error) {
        console.error('Failed to fetch tags:', error)
      } finally {
        this.loading = false
      }
    }
  }
})
