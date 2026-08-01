import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import RecipeList from '../RecipeList.vue'
import { recipeService } from '@/services/recipeService'

vi.mock('@/services/recipeService', () => ({
  recipeService: {
    getRecipes: vi.fn()
  }
}))

/**
 * Builds a recipe in the exact shape the API serves, including a null rating for
 * the unrated recipes that make up part of the collection.
 */
function apiRecipe(overrides: Record<string, unknown> = {}) {
  return {
    id: '6620d08db5eda9af25bb225b',
    title: 'Köstliche BBQ Spareribs',
    rating: 4.9000916701181065,
    sourceRatingVotes: 654,
    previewImageUrlTemplate: 'https://img.example.com/<format>/ribs.jpg',
    sourceUrl: 'https://www.chefkoch.de/rezepte/1',
    tagIds: ['6628c62d9b0fefc37a4de8d9'],
    ...overrides
  }
}

describe('RecipeList', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.mocked(recipeService.getRecipes).mockReset()
  })

  it('renders a card per recipe returned by the API', async () => {
    vi.mocked(recipeService.getRecipes).mockResolvedValue({
      recipes: [apiRecipe(), apiRecipe({ id: 'b2', title: 'Grießbrei', rating: 4.88 })]
    })

    const wrapper = mount(RecipeList)
    await flushPromises()

    expect(wrapper.findAll('.recipe-item')).toHaveLength(2)
    expect(wrapper.text()).toContain('KÖSTLICHE BBQ SPARERIBS')
    expect(wrapper.text()).toContain('4.9')
    expect(wrapper.text()).toContain('654 STIMMEN')
  })

  it('renders recipes whose rating is missing without breaking the list', async () => {
    vi.mocked(recipeService.getRecipes).mockResolvedValue({
      recipes: [
        apiRecipe({
          id: 'unrated',
          title: 'Ohne Bewertung',
          rating: null,
          sourceRatingVotes: null
        }),
        apiRecipe()
      ]
    })

    const wrapper = mount(RecipeList)
    await flushPromises()

    expect(wrapper.findAll('.recipe-item')).toHaveLength(2)
    expect(wrapper.text()).toContain('OHNE BEWERTUNG')
  })

  it('survives a rating still delivered as the embedded database object', async () => {
    vi.mocked(recipeService.getRecipes).mockResolvedValue({
      recipes: [apiRecipe({ rating: { rating: 4.5, numVotes: 654 } })]
    })

    const wrapper = mount(RecipeList)
    await flushPromises()

    expect(wrapper.findAll('.recipe-item')).toHaveLength(1)
    expect(wrapper.text()).toContain('4.5')
  })
})
