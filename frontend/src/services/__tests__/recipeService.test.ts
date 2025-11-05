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

  describe('getRecommendations', () => {
    it('should call API with correct tag parameters', async () => {
      const mockResponse = {
        data: {
          recommendations: [{ id: '1', title: 'Test Recipe', rating: { rating: 4.5, numVotes: 100 } }]
        }
      }
      vi.mocked(api.get).mockResolvedValue(mockResponse)

      const lockedIds = ['locked1', 'locked2']
      const filters = {
        minRating: 4.0,
        minVotes: 100,
        tags: ['6628c62d9b0fefc37a4de8d9', '6628c62d9b0fefc37a4de8da'],
        hasImage: true,
        difficulty: [1, 2, 3]
      }

      await recipeService.getRecommendations(lockedIds, filters)

      // Verify API was called with correct parameters
      expect(api.get).toHaveBeenCalledWith('/recipes/recommendations', {
        params: {
          locked_ids: 'locked1,locked2',
          min_rating: 4.0,
          min_votes: 100,
          tags: '6628c62d9b0fefc37a4de8d9,6628c62d9b0fefc37a4de8da',
          has_image: true,
          difficulty: '1,2,3'
        }
      })
    })

    it('should not send tags parameter when no tags selected', async () => {
      const mockResponse = { data: { recommendations: [] } }
      vi.mocked(api.get).mockResolvedValue(mockResponse)

      const filters = {
        minRating: 4.0,
        minVotes: 100,
        tags: [], // Empty array
        hasImage: true
      }

      await recipeService.getRecommendations([], filters)

      // Verify API was called without tags parameter
      expect(api.get).toHaveBeenCalledWith('/recipes/recommendations', {
        params: {
          min_rating: 4.0,
          min_votes: 100,
          has_image: true
          // tags should not be present
        }
      })
    })

    it('should handle single tag selection correctly', async () => {
      const mockResponse = { data: { recommendations: [] } }
      vi.mocked(api.get).mockResolvedValue(mockResponse)

      const filters = {
        tags: ['6628c62d9b0fefc37a4de8d9'] // Single tag
      }

      await recipeService.getRecommendations([], filters)

      // Verify single tag is sent correctly (no trailing comma)
      expect(api.get).toHaveBeenCalledWith('/recipes/recommendations', {
        params: {
          tags: '6628c62d9b0fefc37a4de8d9'
        }
      })
    })

  })
})
