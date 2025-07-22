<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRecipeStore } from '@/stores/recipeStore'
import { useTagStore } from '@/stores/tagStore'
import { useCategoryStore } from '@/stores/categoryStore'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { formatNumber } from '@/utils/numberFormatter'

const recipeStore = useRecipeStore()
const tagStore = useTagStore()
const categoryStore = useCategoryStore()
const { tags, loading: tagsLoading } = storeToRefs(tagStore)
const { categories, loading: categoriesLoading } = storeToRefs(categoryStore)
const router = useRouter()

// Group tags by category
const groupedTags = computed(() => {
  if (!tags.value || !categories.value) return []

  // Create category groups with their tags
  const categoryGroups = categories.value.map(category => {
    const categoryTags = tags.value.filter(tag => tag.categoryId === category.id)
    return {
      category,
      tags: categoryTags
    }
  }).filter(group => group.tags.length > 0) // Only show categories that have tags

  // Add uncategorized tags group
  const uncategorizedTags = tags.value.filter(tag => !tag.categoryId || tag.categoryId === null)
  if (uncategorizedTags.length > 0) {
    categoryGroups.push({
      category: { 
        id: 'uncategorized', 
        name: 'Weitere Tags', 
        description: 'Tags ohne Kategorie',
        createdAt: '',
        updatedAt: ''
      },
      tags: uncategorizedTags
    })
  }

  return categoryGroups
})

const loading = computed(() => tagsLoading.value || categoriesLoading.value)

onMounted(async () => {
  await Promise.all([
    tagStore.fetchTags(),
    categoryStore.fetchCategories()
  ])
})

const handleTagClick = (tagId: string) => {
  recipeStore.setTagFilter([tagId])
  router.push('/recipes')
}
</script>

<template>
  <main>
    <section class="categories-section">
      <div v-if="loading" class="text-center mt-4">
        <p class="text-dark dark:text-light">Lade Kategorien...</p>
      </div>
      
      <div v-else>
        <div 
          v-for="group in groupedTags" 
          :key="group.category.id" 
          class="category-group mb-8"
        >
          <div class="category-header mb-4">
            <h2 class="text-2xl font-bold text-dark dark:text-light mb-2">
              {{ group.category.name }}
            </h2>
            <p class="text-gray-600 dark:text-gray-300 text-sm">
              {{ group.category.description }}
            </p>
          </div>
          
          <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
            <div
              v-for="tag in group.tags"
              :key="tag.id"
              class="tag-item cursor-pointer bg-light dark:bg-secondary p-4 transition-all duration-200 hover:bg-gold-light dark:hover:bg-gold"
              @click="handleTagClick(tag.id)"
            >
              <img
                src="https://via.placeholder.com/150"
                :alt="tag.name"
                class="w-full h-24 object-cover mb-2"
              />
              <p class="text-center text-sm font-medium text-dark dark:text-light">
                {{ tag.name }}
              </p>
              <p class="text-center text-xs text-gray-500 dark:text-gray-400 mt-1">
                {{ formatNumber(tag.usage_count) }} Rezepte
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.categories-section {
  margin-top: 2rem;
  padding: 0 1rem;
}

.category-group {
  border-bottom: 1px solid #e5e7eb;
}

.category-group:last-child {
  border-bottom: none;
}

.dark .category-group {
  border-bottom-color: #374151;
}

.category-header h2 {
  font-weight: 700;
  letter-spacing: -0.025em;
}

.tag-item {
  border-radius: 0;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.dark .tag-item {
  border-color: #374151;
}

.tag-item img {
  transition: transform 0.3s ease;
  border-radius: 0;
}

.tag-item:hover img {
  transform: scale(1.05);
}

.tag-item:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

@media (min-width: 768px) {
  .categories-section {
    padding: 0 2rem;
  }
}

@media (min-width: 1024px) {
  .categories-section {
    padding: 0 3rem;
  }
}
</style>
