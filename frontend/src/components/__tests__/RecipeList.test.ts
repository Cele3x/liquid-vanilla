import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import RecipeList from '../RecipeList.vue'
import { recipeService } from '@/services/recipeService'
import { tagService } from '@/services/tagService'

vi.mock('@/services/recipeService', () => ({
  recipeService: {
    getRecipes: vi.fn()
  }
}))

vi.mock('@/services/tagService', () => ({
  tagService: {
    getTags: vi.fn()
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
    vi.mocked(tagService.getTags).mockReset()
    vi.mocked(tagService.getTags).mockResolvedValue([
      { id: '6628c62d9b0fefc37a4de8d9', name: 'Hauptspeise', usage_count: 3 }
    ])
  })

  it('shows tag names on the card, never the raw ids the API sends', async () => {
    vi.mocked(recipeService.getRecipes).mockResolvedValue({ recipes: [apiRecipe()] })

    const wrapper = mount(RecipeList)
    await flushPromises()

    expect(wrapper.text()).toContain('HAUPTSPEISE')
    expect(wrapper.text()).not.toContain('6628C62D9B0FEFC37A4DE8D9')
  })

  it('caps the card at three tags so a grid row cannot grow uneven', async () => {
    vi.mocked(tagService.getTags).mockResolvedValue([
      { id: 't1', name: 'Reis', usage_count: 900 },
      { id: 't2', name: 'Snack', usage_count: 800 },
      { id: 't3', name: 'Kinder', usage_count: 700 },
      { id: 't4', name: 'Camping', usage_count: 10 },
      { id: 't5', name: 'Party', usage_count: 5 }
    ])
    vi.mocked(recipeService.getRecipes).mockResolvedValue({
      recipes: [apiRecipe({ tagIds: ['t1', 't2', 't3', 't4', 't5'] })]
    })

    const wrapper = mount(RecipeList)
    await flushPromises()

    expect(wrapper.text()).toContain('REIS')
    expect(wrapper.text()).not.toContain('CAMPING')
    expect(wrapper.text()).toContain('+2')
  })

  it('names every tag in the overflow tooltip', async () => {
    vi.mocked(tagService.getTags).mockResolvedValue([
      { id: 't1', name: 'Hauptspeise', usage_count: 900 },
      { id: 't2', name: 'Europa', usage_count: 800 },
      { id: 't3', name: 'Vegetarisch', usage_count: 700 },
      { id: 't4', name: 'Camping', usage_count: 10 }
    ])
    vi.mocked(recipeService.getRecipes).mockResolvedValue({
      recipes: [apiRecipe({ tagIds: ['t1', 't2', 't3', 't4'] })]
    })

    const wrapper = mount(RecipeList)
    await flushPromises()

    const tooltip = wrapper.find('[title]').attributes('title')
    expect(tooltip).toBe('Hauptspeise · Europa · Vegetarisch · Camping')
  })

  it('hides tags that cannot be resolved instead of falling back to the id', async () => {
    vi.mocked(recipeService.getRecipes).mockResolvedValue({
      recipes: [apiRecipe({ tagIds: ['deadbeefdeadbeefdeadbeef'] })]
    })

    const wrapper = mount(RecipeList)
    await flushPromises()

    expect(wrapper.findAll('.recipe-item')).toHaveLength(1)
    expect(wrapper.text().toUpperCase()).not.toContain('DEADBEEF')
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
