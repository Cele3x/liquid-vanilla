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
  getters: {
    /**
     * Resolve a tag id to its display name.
     *
     * Recipes carry tag ids, so views need the loaded tag list to show names.
     * Returns null when the tags have not loaded yet or the id is unknown, which
     * lets callers hide the tag rather than render a raw object id.
     */
    tagNameById: (state) => {
      const namesById = new Map(state.tags.map((tag) => [tag.id, tag.name]))
      return (id: string): string | null => namesById.get(id) ?? null
    }
  },
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
