import { defineStore } from 'pinia'
import { categoryService } from '@/services/categoryService'

interface Category {
  id: string
  name: string
  description: string
  createdAt: string
  updatedAt: string
}

export const useCategoryStore = defineStore('category', {
  state: () => ({
    categories: [] as Category[],
    loading: false,
    error: null as string | null
  }),

  getters: {
    getCategoryById: (state) => (id: string) => {
      return state.categories.find(category => category.id === id)
    },

    getCategoryByName: (state) => (name: string) => {
      return state.categories.find(category => category.name === name)
    }
  },

  actions: {
    async fetchCategories() {
      if (this.loading) return

      this.loading = true
      this.error = null
      
      try {
        const data = await categoryService.getCategories()
        this.categories = data
      } catch (error) {
        console.error('Failed to fetch categories:', error)
        this.error = 'Failed to load categories'
      } finally {
        this.loading = false
      }
    },

    async createCategory(categoryData: { name: string; description: string }) {
      try {
        const newCategory = await categoryService.createCategory(categoryData)
        await this.fetchCategories() // Refresh the list
        return newCategory
      } catch (error) {
        console.error('Failed to create category:', error)
        this.error = 'Failed to create category'
        throw error
      }
    },

    async updateCategory(id: string, categoryData: { name: string; description: string }) {
      try {
        const updatedCategory = await categoryService.updateCategory(id, categoryData)
        await this.fetchCategories() // Refresh the list
        return updatedCategory
      } catch (error) {
        console.error('Failed to update category:', error)
        this.error = 'Failed to update category'
        throw error
      }
    },

    async deleteCategory(id: string) {
      try {
        await categoryService.deleteCategory(id)
        await this.fetchCategories() // Refresh the list
      } catch (error) {
        console.error('Failed to delete category:', error)
        this.error = 'Failed to delete category'
        throw error
      }
    }
  }
})