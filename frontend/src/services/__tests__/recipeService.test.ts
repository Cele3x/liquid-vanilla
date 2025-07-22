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
          recommendations: [
            { id: '1', title: 'Test Recipe', rating: 4.5, sourceRatingVotes: 100 }
          ] 
        } 
      }
      vi.mocked(api.get).mockResolvedValue(mockResponse)

      const lockedIds = ['locked1', 'locked2']
      const filters = {
        minRating: 4.0,
        minVotes: 100,
        tagIds: ['6628c62d9b0fefc37a4de8d9', '6628c62d9b0fefc37a4de8da'],
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
          tag_ids: '6628c62d9b0fefc37a4de8d9,6628c62d9b0fefc37a4de8da',
          has_image: true,
          difficulty: '1,2,3'
        }
      })
    })

    it('should not send tag_ids parameter when no tags selected', async () => {
      const mockResponse = { data: { recommendations: [] } }
      vi.mocked(api.get).mockResolvedValue(mockResponse)

      const filters = {
        minRating: 4.0,
        minVotes: 100,
        tagIds: [], // Empty array
        hasImage: true
      }

      await recipeService.getRecommendations([], filters)

      // Verify API was called without tag_ids parameter
      expect(api.get).toHaveBeenCalledWith('/recipes/recommendations', {
        params: {
          min_rating: 4.0,
          min_votes: 100,
          has_image: true
          // tag_ids should not be present
        }
      })
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

    it('should log API parameters for debugging', async () => {
      const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {})
      const mockResponse = { data: { recommendations: [] } }
      vi.mocked(api.get).mockResolvedValue(mockResponse)

      const filters = {
        tagIds: ['6628c62d9b0fefc37a4de8d9']
      }

      await recipeService.getRecommendations([], filters)

      // Verify console.log was called with API parameters
      expect(consoleSpy).toHaveBeenCalledWith('API params being sent:', {
        tag_ids: '6628c62d9b0fefc37a4de8d9'
      })

      consoleSpy.mockRestore()
    })
  })
})