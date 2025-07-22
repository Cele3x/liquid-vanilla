import { defineStore } from 'pinia'
import { tagService } from '@/services/tagService'
import { formatNumber } from '@/utils/numberFormatter'

interface Tag {
  id: string
  name: string
  usage_count: number
  categoryId?: string | null
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
        console.log('Tags fetched:', data.slice(0, 3).map((t: Tag) => `${t.name}: ${formatNumber(t.usage_count)} recipes`))
      } catch (error) {
        console.error('Failed to fetch tags:', error)
      } finally {
        this.loading = false
      }
    },

    async forceRefreshTags() {
      this.loading = true
      try {
        const data = await tagService.getTags()
        this.tags = data
        console.log('Tags force refreshed:', data.slice(0, 3).map((t: Tag) => `${t.name}: ${formatNumber(t.usage_count)} recipes`))
      } catch (error) {
        console.error('Failed to force refresh tags:', error)
      } finally {
        this.loading = false
      }
    }
  }
})
