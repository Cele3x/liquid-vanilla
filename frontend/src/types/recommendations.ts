/**
 * Filter selection driving the recommendation query.
 *
 * Shared by the filter panel that produces it, the view that holds it and the
 * service that serialises it, so the three cannot drift apart.
 */
export interface RecommendationFilters {
  minScore: number
  minVotes: number
  maxVotes: number | null
  hasImage: boolean
  tagIds: string[]
  excludeTagIds: string[]
  difficulty: number[]
  sources: string[]
}
