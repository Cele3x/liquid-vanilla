<script setup lang="ts">
import { onMounted } from 'vue'
import { useRecipeStore } from '@/stores/recipeStore'
import { useTagStore } from '@/stores/tagStore'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'

const recipeStore = useRecipeStore()
const tagStore = useTagStore()
const { tags, loading } = storeToRefs(tagStore)
const router = useRouter()

onMounted(async () => {
  tagStore.fetchTags()
})

const handleClick = (tagId: String) => {
  recipeStore.setTagFilter([tagId.toString()])
  router.push('/recipes')
}
</script>

<template>
  <main>
    <section class="tags-section">
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
        <div
          v-for="tag in tags"
          :key="tag.id"
          class="tag-item cursor-pointer"
          @click="handleClick(tag.id)"
        >
          <img
            src="https://via.placeholder.com/150"
            :alt="tag.name"
            class="w-full h-32 object-cover mb-2"
          />
          <p class="text-center text-lg">{{ tag.name }}</p>
        </div>
      </div>
      <div v-if="loading" class="text-center mt-4">
        <p class="text-light">Loading tags...</p>
      </div>
    </section>
  </main>
</template>

<style scoped>
.tags-section {
  margin-top: 2rem;
}
.tag-item img {
  transition: transform 0.3s ease;
}
.tag-item:hover img {
  transform: scale(1.05);
}
</style>
