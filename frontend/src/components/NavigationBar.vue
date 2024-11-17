<script setup lang="ts">
import { ref } from 'vue';
import { RouterLink } from 'vue-router';
import SearchBar from './SearchBar.vue';

const isSearchVisible = ref(false);

const toggleSearch = () => {
  isSearchVisible.value = !isSearchVisible.value;
  if (isSearchVisible.value) {
    setTimeout(() => {
      document.getElementById('search')?.focus();
    }, 100);
  }
};
</script>

<template>
  <nav class="bg-primary text-light shadow-lg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <RouterLink to="/" class="flex-shrink-0">
          <img class="h-8 w-8" src="../assets/liquid-vanilla-logo.png" alt="Logo">
        </RouterLink>

        <!-- Navigation Links and Search Bar Container -->
        <div class="flex-grow mx-8 relative">
          <!-- Navigation Links -->
          <div
            class="transition-all duration-300 ease-in-out flex space-x-6 h-9 items-center"
            :class="{
              'opacity-100 translate-x-0': !isSearchVisible,
              'opacity-0 -translate-x-4 invisible': isSearchVisible
            }"
          >
            <RouterLink
              to="/about"
              class="text-light hover:text-accent transition-colors"
            >
              About
            </RouterLink>
            <!-- Add more navigation links here -->
          </div>

          <!-- Search Bar -->
          <SearchBar v-model:isVisible="isSearchVisible" />
        </div>

        <!-- Right side items -->
        <div class="flex items-center space-x-4">
          <!-- Search Button -->
          <button
            @click="toggleSearch"
            class="p-1 text-accent hover:text-light focus:outline-none h-9 w-9 flex items-center justify-center"
            :class="{ 'text-light': isSearchVisible }"
          >
            <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
            </svg>
          </button>

          <!-- Notification Bell -->
          <button class="p-1 text-accent hover:text-light focus:outline-none h-9 w-9 flex items-center justify-center">
            <span class="sr-only">View notifications</span>
            <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          </button>

          <!-- User Avatar -->
          <div class="relative">
            <button type="button" class="bg-secondary rounded-full flex text-sm focus:outline-none h-9 w-9" id="user-menu" aria-expanded="false" aria-haspopup="true">
              <span class="sr-only">Open user menu</span>
              <img class="rounded-full object-cover object-center" src="../assets/user.jpg" alt="avatar">
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>