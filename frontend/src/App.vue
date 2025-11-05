<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import NavigationBar from './components/NavigationBar.vue'
import { useDarkMode } from './composables/useDarkMode'

const { initializeDarkMode } = useDarkMode()

onMounted(() => {
  initializeDarkMode()
})
</script>

<template>
  <div class="min-h-screen bg-primary-light dark:bg-primary text-dark dark:text-light">
    <NavigationBar />
    <main class="container mx-auto">
      <RouterView />
    </main>
  </div>
</template>
