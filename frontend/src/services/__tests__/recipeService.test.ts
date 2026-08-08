import { describe, it, expect, beforeEach, vi } from 'vitest'
import { recipeService } from '../recipeService'
import api from '../api'

// Mock the api module
vi.mock('../api', () => ({
  default: {
    get: vi.fn()
  }
}))

describe('recipeService', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('getRecipes', () => {
    it('should send every selected tag, not just the last one', async () => {
      vi.mocked(api.get).mockResolvedValue({ data: { recipes: [] } })

      const tags = ['6628c62d9b0fefc37a4de8d9', '6628c62d9b0fefc37a4de8da']
      await recipeService.getRecipes(1, 20, '', tags)

      const [, config] = vi.mocked(api.get).mock.calls[0]
      expect((config?.params as { tags?: string[] }).tags).toEqual(tags)
    })

    it('should omit the tags parameter when nothing is selected', async () => {
      vi.mocked(api.get).mockResolvedValue({ data: { recipes: [] } })

      await recipeService.getRecipes(1, 20, '', [])

      const [, config] = vi.mocked(api.get).mock.calls[0]
      expect((config?.params as { tags?: string[] }).tags).toBeUndefined()
    })
  })

  describe('getRecommendations', () => {
    it('should call API with correct tag parameters', async () => {
      const mockResponse = {
        data: {
          recommendations: [{ id: '1', title: 'Test Recipe', rating: 4.5, sourceRatingVotes: 100 }]
        }
      }
      vi.mocked(api.get).mockResolvedValue(mockResponse)

      const lockedIds = ['locked1', 'locked2']
      const filters = {
        minScore: 4.0,
        minVotes: 25,
        tagIds: ['6628c62d9b0fefc37a4de8d9', '6628c62d9b0fefc37a4de8da'],
        hasImage: true,
        difficulty: [1, 2, 3],
        sources: ['chefkoch.de', 'kochbar.de']
      }

      await recipeService.getRecommendations(lockedIds, filters)

      // Verify API was called with correct parameters
      expect(api.get).toHaveBeenCalledWith('/recipes/recommendations', {
        params: {
          locked_ids: 'locked1,locked2',
          min_score: 4.0,
          min_votes: 25,
          tag_ids: '6628c62d9b0fefc37a4de8d9,6628c62d9b0fefc37a4de8da',
          has_image: true,
          difficulty: '1,2,3',
          sources: 'chefkoch.de,kochbar.de'
        }
      })
    })

    it('should not send tag_ids parameter when no tags selected', async () => {
      const mockResponse = { data: { recommendations: [] } }
      vi.mocked(api.get).mockResolvedValue(mockResponse)

      const filters = {
        minScore: 4.0,
        minVotes: 25,
        tagIds: [], // Empty array
        hasImage: true
      }

      await recipeService.getRecommendations([], filters)

      // Verify API was called without tag_ids parameter
      expect(api.get).toHaveBeenCalledWith('/recipes/recommendations', {
        params: {
          min_score: 4.0,
          min_votes: 25,
          has_image: true
          // tag_ids should not be present
        }
      })
    })

    it('should omit the sources parameter when no source is excluded', async () => {
      const mockResponse = { data: { recommendations: [] } }
      vi.mocked(api.get).mockResolvedValue(mockResponse)

      await recipeService.getRecommendations([], { minScore: 3.5, sources: [] })

      const [, config] = vi.mocked(api.get).mock.calls[0]
      expect((config?.params as { sources?: string }).sources).toBeUndefined()
    })

    it('should handle single tag selection correctly', async () => {
      const mockResponse = { data: { recommendations: [] } }
      vi.mocked(api.get).mockResolvedValue(mockResponse)

      const filters = {
        tagIds: ['6628c62d9b0fefc37a4de8d9'] // Single tag
      }

      await recipeService.getRecommendations([], filters)

      // Verify single tag is sent correctly (no trailing comma)
      expect(api.get).toHaveBeenCalledWith('/recipes/recommendations', {
        params: {
          tag_ids: '6628c62d9b0fefc37a4de8d9'
        }
      })
    })

    it('should send excluded tags as exclude_tag_ids', async () => {
      const mockResponse = { data: { recommendations: [] } }
      vi.mocked(api.get).mockResolvedValue(mockResponse)

      await recipeService.getRecommendations([], {
        tagIds: ['6628c62d9b0fefc37a4de8d9'],
        excludeTagIds: ['6628c62d9b0fefc37a4de8db', '6628c62d9b0fefc37a4de8dc']
      })

      expect(api.get).toHaveBeenCalledWith('/recipes/recommendations', {
        params: {
          tag_ids: '6628c62d9b0fefc37a4de8d9',
          exclude_tag_ids: '6628c62d9b0fefc37a4de8db,6628c62d9b0fefc37a4de8dc'
        }
      })
    })

    it('should omit exclude_tag_ids when no tag is excluded', async () => {
      const mockResponse = { data: { recommendations: [] } }
      vi.mocked(api.get).mockResolvedValue(mockResponse)

      await recipeService.getRecommendations([], { minScore: 3.5, excludeTagIds: [] })

      const [, config] = vi.mocked(api.get).mock.calls[0]
      expect((config?.params as { exclude_tag_ids?: string }).exclude_tag_ids).toBeUndefined()
    })
  })
})
