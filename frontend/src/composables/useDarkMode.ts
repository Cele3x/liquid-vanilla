import { ref, watch } from 'vue'

// Function to detect system preference
const getSystemPreference = (): boolean => {
  // Check if window and matchMedia are available (browser environment)
  if (typeof window !== 'undefined' && window.matchMedia) {
    // Return true if system prefers dark mode
    return window.matchMedia('(prefers-color-scheme: dark)').matches
  }
  // Fallback to dark mode if system preference can't be detected
  return true
}

// Create a singleton instance - initialize with system preference
const isDarkMode = ref(getSystemPreference())
let isInitialized = false

const updateDarkMode = (newValue: boolean) => {
  if (newValue) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('darkMode', 'true')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('darkMode', 'false')
  }
}

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
}

// Initialize from localStorage if available, otherwise use system preference
const initializeDarkMode = () => {
  const savedMode = localStorage.getItem('darkMode')
  if (savedMode !== null) {
    // User has previously set a preference
    isDarkMode.value = savedMode === 'true'
  } else {
    // No saved preference, use system preference or fallback to dark
    isDarkMode.value = getSystemPreference()

    // Listen for system preference changes only if no user preference is saved
    if (typeof window !== 'undefined' && window.matchMedia) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
      const handleSystemPreferenceChange = (e: MediaQueryListEvent) => {
        // Only update if user hasn't manually set a preference
        if (localStorage.getItem('darkMode') === null) {
          isDarkMode.value = e.matches
        }
      }

      // Add listener for system preference changes
      mediaQuery.addEventListener('change', handleSystemPreferenceChange)
    }
  }

  // Initialize the watcher only once
  if (!isInitialized) {
    watch(isDarkMode, updateDarkMode, { immediate: true })
    isInitialized = true
  }
}

export const useDarkMode = () => {
  return {
    isDarkMode,
    toggleDarkMode,
    initializeDarkMode
  }
}
