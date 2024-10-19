<script setup lang="ts">
import { ref } from 'vue';

const searchQuery = ref('');

const handleSearch = () => {
  console.log('Searching for:', searchQuery.value);
};

const handleNewRecipe = () => {
  console.log('Creating new recipe');
};
</script>

<template>
  <nav class="bg-primary text-light shadow-lg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <div class="flex-shrink-0">
          <img class="h-8 w-8" src="../assets/logo.svg" alt="Logo">
        </div>

        <!-- Search Bar -->
        <div class="flex-grow mx-4">
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-accent" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
              </svg>
            </div>
            <input v-model="searchQuery" @keyup.enter="handleSearch" type="text" name="search" id="search" class="block w-full pl-10 pr-3 py-2 border border-secondary rounded-md leading-5 bg-secondary text-light placeholder-accent focus:outline-none focus:ring-1 focus:ring-accent focus:border-accent sm:text-sm" placeholder="Search" />
          </div>
        </div>

        <!-- Right side items -->
        <div class="flex items-center">
          <!-- Notification Bell -->
          <button class="p-1 rounded-full text-accent hover:text-light focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent">
            <span class="sr-only">View notifications</span>
            <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          </button>

          <!-- User Avatar -->
          <div class="ml-3 relative">
            <div>
              <button type="button" class="bg-secondary rounded-full flex text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent" id="user-menu" aria-expanded="false" aria-haspopup="true">
                <span class="sr-only">Open user menu</span>
                <img class="h-8 w-8 rounded-full" src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" alt="">
              </button>
            </div>
          </div>

          <!-- New Project Button -->
          <div class="ml-4">
            <button @click="handleNewRecipe" type="button" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-primary bg-accent hover:bg-light focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent">
              New Recipe
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>