<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
<!--  <header>-->
<!--    <nav>-->
<!--      <RouterLink to="/">Home</RouterLink>-->
<!--      <RouterLink to="/about">About</RouterLink>-->
<!--      <RouterLink to="/recipes">About</RouterLink>-->
<!--    </nav>-->
<!--  </header>-->

  <main>
    <RouterView />
  </main>
</template>

<style scoped>
nav {
  font-size: 12px;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}
</style>
