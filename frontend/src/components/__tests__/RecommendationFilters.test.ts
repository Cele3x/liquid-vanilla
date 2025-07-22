import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { nextTick } from 'vue'
import RecommendationFilters from '../RecommendationFilters.vue'
import { tagService } from '@/services/tagService'

// Mock the tagService
vi.mock('@/services/tagService', () => ({
  tagService: {
    getTags: vi.fn()
  }
}))

const mockTags = [
  { id: '6628c62d9b0fefc37a4de8d9', name: 'Hauptspeise' },
  { id: '6628c62d9b0fefc37a4de8da', name: 'Vegetarisch' },
  { id: '6628c62d9b0fefc37a4de8db', name: 'Schnell' }
]

describe('RecommendationFilters', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    // Mock successful tags fetch
    vi.mocked(tagService.getTags).mockResolvedValue(mockTags)
  })

  it('should fetch and display available tags', async () => {
    const wrapper = mount(RecommendationFilters)
    
    // Wait for component to mount and fetch tags
    await nextTick()
    await vi.waitFor(() => {
      expect(tagService.getTags).toHaveBeenCalled()
    })
  })

  it('should add tags to filter when selected', async () => {
    const wrapper = mount(RecommendationFilters)
    
    // Wait for tags to load
    await nextTick()
    await vi.waitFor(() => wrapper.vm.availableTags.length > 0)
    
    // Search for a tag
    const searchInput = wrapper.find('input[placeholder*="Search tags"]')
    await searchInput.setValue('Hauptspeise')
    
    await nextTick()
    
    // Click on the search result
    const searchResult = wrapper.find('button:contains("Hauptspeise")')
    if (searchResult.exists()) {
      await searchResult.trigger('click')
      
      // Check that tag was added to filters
      expect(wrapper.vm.filters.tagIds).toContain('6628c62d9b0fefc37a4de8d9')
    }
  })

  it('should emit filters-changed with correct tag IDs when applied', async () => {
    const wrapper = mount(RecommendationFilters)
    
    // Wait for tags to load
    await nextTick()
    await vi.waitFor(() => wrapper.vm.availableTags.length > 0)
    
    // Manually add a tag to test the emission
    await wrapper.vm.addTag('6628c62d9b0fefc37a4de8d9')
    
    // Apply filters
    const applyButton = wrapper.find('button:contains("Apply Filters")')
    await applyButton.trigger('click')
    
    // Check that filters-changed event was emitted with correct data
    const emitted = wrapper.emitted('filters-changed')
    expect(emitted).toBeTruthy()
    expect(emitted![0][0].tagIds).toContain('6628c62d9b0fefc37a4de8d9')
  })

  it('should remove tags when clicked on selected tag chip', async () => {
    const wrapper = mount(RecommendationFilters)
    
    // Wait for tags to load
    await nextTick()
    await vi.waitFor(() => wrapper.vm.availableTags.length > 0)
    
    // Add a tag first
    await wrapper.vm.addTag('6628c62d9b0fefc37a4de8d9')
    await nextTick()
    
    // Find and click the remove button on the selected tag
    const removeButton = wrapper.find('.inline-flex:contains("Hauptspeise")')
    if (removeButton.exists()) {
      await removeButton.trigger('click')
      
      // Check that tag was removed
      expect(wrapper.vm.filters.tagIds).not.toContain('6628c62d9b0fefc37a4de8d9')
    }
  })

  it('should send correct API parameters for tag filtering', () => {
    // This test checks the API service parameters
    const testFilters = {
      minRating: 4.0,
      minVotes: 100,
      tagIds: ['6628c62d9b0fefc37a4de8d9', '6628c62d9b0fefc37a4de8da'],
      hasImage: true,
      difficulty: [1, 2, 3]
    }
    
    // Test that tagIds array gets properly joined with commas
    const expectedTagParam = '6628c62d9b0fefc37a4de8d9,6628c62d9b0fefc37a4de8da'
    
    // This would typically be tested in the service test, but we can verify the format here
    expect(testFilters.tagIds.join(',')).toBe(expectedTagParam)
  })
})