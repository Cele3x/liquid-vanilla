import { defineStore } from 'pinia'
import { categoryService } from '@/services/categoryService'
import { useTagStore } from './tagStore'

interface Category {
  id: string
  name: string
  description?: string
  order: number
}

interface CategoryWithTags extends Category {
  tags: Tag[]
}

interface Tag {
  id: string
  name: string
  categoryId?: string
  usageCount?: number
  imageUrl?: string
}

export const useCategoryStore = defineStore('category', {
  state: () => ({
    categories: [] as Category[],
    categoriesWithTags: [] as CategoryWithTags[],
    loading: false
  }),
  actions: {
    async fetchCategories() {
      if (this.loading) return

      this.loading = true
      try {
        const data = await categoryService.getCategories()
        this.categories = data
      } catch (error) {
        console.error('Fehler beim Laden der Kategorien:', error)
        this.categories = []
      } finally {
        this.loading = false
      }
    },

    async fetchCategoriesWithTags() {
      const tagStore = useTagStore()

      // Fetch both categories and tags
      await Promise.all([this.fetchCategories(), tagStore.fetchTags()])

      // Group tags by category
      this.categoriesWithTags = this.categories.map((category) => {
        const categoryTags = tagStore.tags.filter((tag) => tag.categoryId === category.id)
        return {
          ...category,
          tags: categoryTags
        }
      })
    }
  }
})
