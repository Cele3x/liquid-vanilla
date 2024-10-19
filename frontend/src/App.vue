<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navigation from './components/Navigation.vue'
</script>

<template>
  <div class="min-h-screen bg-primary text-light">
    <Navigation />
    <main class="container mx-auto">
      <RouterView />
    </main>
  </div>
</template>