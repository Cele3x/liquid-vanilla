<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRecipeStore } from '@/stores/recipeStore'
import { categoryService } from '@/services/categoryService'
import { tagService } from '@/services/tagService'
import { useRouter } from 'vue-router'

interface Category {
  id: string
  name: string
  description?: string
  order: number
}

interface Tag {
  id: string
  name: string
  categoryId?: string
  imageUrl?: string
  isEssential?: boolean
}

interface CategoryWithTags {
  category: Category
  tags: Tag[]
}

const recipeStore = useRecipeStore()
const router = useRouter()
const categories = ref<Category[]>([])
const tags = ref<Tag[]>([])
const loading = ref(false)

const getLocalImageUrl = (categoryName: string): string => {
  // Convert category name to normalized filename (lowercase, no special chars)
  const filename = categoryName
    .toLowerCase()
    .replace(/ä/g, 'ae')
    .replace(/ö/g, 'oe')
    .replace(/ü/g, 'ue')
    .replace(/ß/g, 'ss')
    .replace(/[^a-z0-9]/g, '')

  return `/tag-images/${filename}.jpg`
}

// Computed property to group tags by categories
const categorizedTags = computed(() => {
  const categoryMap: { [key: string]: CategoryWithTags } = {}

  // Initialize categories
  categories.value.forEach((category) => {
    categoryMap[category.id] = {
      category,
      tags: []
    }
  })

  // Group tags by category
  tags.value.forEach((tag) => {
    if (tag.categoryId && categoryMap[tag.categoryId]) {
      categoryMap[tag.categoryId].tags.push(tag)
    }
  })

  // Return categories sorted by order, only including those with tags
  return Object.values(categoryMap)
    .filter((item) => item.tags.length > 0)
    .sort((a, b) => a.category.order - b.category.order)
})

onMounted(async () => {
  loading.value = true
  try {
    // Fetch both categories and essential tags only
    const [categoriesData, tagsData] = await Promise.all([
      categoryService.getCategories(),
      tagService.getTags(true) // Get only essential tags
    ])

    categories.value = categoriesData

    tags.value = tagsData.map((tag: any) => ({
      ...tag,
      imageUrl: getLocalImageUrl(tag.name)
    }))
  } catch (error) {
    console.error('Failed to fetch categories and tags:', error)
    // Use default data if API fails
    const defaultData = getDefaultCategoriesWithTags()
    categories.value = defaultData.categories
    tags.value = defaultData.tags
  } finally {
    loading.value = false
  }
})

const getDefaultCategoriesWithTags = () => {
  // Create default categories and tags for fallback
  const defaultCategories: Category[] = [
    { id: '1', name: 'Regionale Küche', order: 1 },
    { id: '2', name: 'Speisen-Arten', order: 2 },
    { id: '3', name: 'Mahlzeiten-Typen', order: 3 },
    { id: '4', name: 'Backen & Süßes', order: 4 },
    { id: '5', name: 'Zubereitungsarten', order: 5 },
    { id: '6', name: 'Spezielle Ernährung', order: 6 },
    { id: '7', name: 'Anlässe & Jahreszeiten', order: 7 }
  ]

  const defaultTags: Tag[] = [
    // Regional cuisine
    { id: 't1', name: 'Italien', categoryId: '1', imageUrl: getLocalImageUrl('Italien'), isEssential: true },
    { id: 't2', name: 'Deutschland', categoryId: '1', imageUrl: getLocalImageUrl('Deutschland'), isEssential: true },
    { id: 't3', name: 'Asien', categoryId: '1', imageUrl: getLocalImageUrl('Asien'), isEssential: true },
    { id: 't4', name: 'Amerika', categoryId: '1', imageUrl: getLocalImageUrl('Amerika'), isEssential: true },
    { id: 't5', name: 'Frankreich', categoryId: '1', imageUrl: getLocalImageUrl('Frankreich'), isEssential: true },

    // Food types
    { id: 't6', name: 'Fleisch', categoryId: '2', imageUrl: getLocalImageUrl('Fleisch'), isEssential: true },
    { id: 't7', name: 'Fisch', categoryId: '2', imageUrl: getLocalImageUrl('Fisch'), isEssential: true },
    { id: 't8', name: 'Vegetarisch', categoryId: '2', imageUrl: getLocalImageUrl('Vegetarisch'), isEssential: true },
    { id: 't9', name: 'Vegan', categoryId: '2', imageUrl: getLocalImageUrl('Vegan'), isEssential: true },
    { id: 't10', name: 'Pasta', categoryId: '2', imageUrl: getLocalImageUrl('Pasta'), isEssential: true },
    { id: 't11', name: 'Pizza', categoryId: '2', imageUrl: getLocalImageUrl('Pizza'), isEssential: true },

    // Meal types
    { id: 't12', name: 'Hauptspeise', categoryId: '3', imageUrl: getLocalImageUrl('Hauptspeise'), isEssential: true },
    { id: 't13', name: 'Vorspeise', categoryId: '3', imageUrl: getLocalImageUrl('Vorspeise'), isEssential: true },
    { id: 't14', name: 'Dessert', categoryId: '3', imageUrl: getLocalImageUrl('Dessert'), isEssential: true },
    { id: 't15', name: 'Frühstück', categoryId: '3', imageUrl: getLocalImageUrl('Frühstück'), isEssential: true },

    // Baking
    { id: 't16', name: 'Backen', categoryId: '4', imageUrl: getLocalImageUrl('Backen'), isEssential: true },
    { id: 't17', name: 'Kuchen', categoryId: '4', imageUrl: getLocalImageUrl('Kuchen'), isEssential: true },
    { id: 't18', name: 'Torte', categoryId: '4', imageUrl: getLocalImageUrl('Torte'), isEssential: true },

    // Cooking methods
    { id: 't19', name: 'Grillen', categoryId: '5', imageUrl: getLocalImageUrl('Grillen'), isEssential: true },
    { id: 't20', name: 'Braten', categoryId: '5', imageUrl: getLocalImageUrl('Braten'), isEssential: true },

    // Special diets
    { id: 't21', name: 'Low Carb', categoryId: '6', imageUrl: getLocalImageUrl('Low Carb'), isEssential: true },
    { id: 't22', name: 'Paleo', categoryId: '6', imageUrl: getLocalImageUrl('Paleo'), isEssential: true },

    // Occasions
    { id: 't23', name: 'Party', categoryId: '7', imageUrl: getLocalImageUrl('Party'), isEssential: true },
    { id: 't24', name: 'Weihnachten', categoryId: '7', imageUrl: getLocalImageUrl('Weihnachten'), isEssential: true }
  ]

  return { categories: defaultCategories, tags: defaultTags }
}

const handleClick = (tagId: string) => {
  recipeStore.setTagFilter([tagId])
  router.push('/recipes')
}

const createPlaceholderImage = (text: string) => {
  // Create a simple colored placeholder using canvas data URL
  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')
  canvas.width = 300
  canvas.height = 200

  if (ctx) {
    // Background
    ctx.fillStyle = '#e5e7eb'
    ctx.fillRect(0, 0, 300, 200)

    // Text
    ctx.fillStyle = '#6b7280'
    ctx.font = '16px Arial'
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.fillText(text || 'No Image', 150, 100)
  }

  return canvas.toDataURL()
}

const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  const tagName = img.alt || 'No Image'
  img.src = createPlaceholderImage(tagName)
}
</script>

<template>
  <main>
    <section class="categories-section">
      <!-- Show loading state -->
      <div v-if="loading" class="text-center mt-4">
        <p class="text-dark dark:text-light">Lade Kategorien...</p>
      </div>

      <!-- Show categorized tags -->
      <div v-else>
        <div
          v-for="categoryWithTags in categorizedTags"
          :key="categoryWithTags.category.id"
          class="category-section mb-8"
        >
          <!-- Category Header (no image, just title) -->
          <h2 class="text-2xl font-bold text-dark dark:text-light mb-4">
            {{ categoryWithTags.category.name }}
          </h2>

          <!-- Tags Grid for this category -->
          <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
            <div
              v-for="tag in categoryWithTags.tags"
              :key="tag.id"
              class="tag-item cursor-pointer"
              @click="handleClick(tag.id)"
            >
              <img
                :src="tag.imageUrl"
                :alt="tag.name"
                class="w-full h-48 object-cover mb-2"
                @error="handleImageError"
                loading="lazy"
              />
              <p class="text-center text-lg text-dark dark:text-light">{{ tag.name.toUpperCase() }}</p>
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
  padding: 1rem;
}

.category-section {
  margin-bottom: 3rem;
}

.category-section h2 {
  padding-left: 0.5rem;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 0.5rem;
}

.dark .category-section h2 {
  border-bottom-color: #374151;
}

.tag-item img {
  transition: transform 0.3s ease;
}

.tag-item:hover img {
  transform: scale(1.05);
}
</style>
