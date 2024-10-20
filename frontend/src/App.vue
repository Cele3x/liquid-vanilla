<script setup lang="ts">
import { RouterView } from 'vue-router'
import NavigationBar from './components/NavigationBar.vue'
</script>

<template>
  <div class="min-h-screen bg-primary text-light">
    <NavigationBar />
    <main class="container mx-auto">
      <RouterView />
    </main>
  </div>
</template>