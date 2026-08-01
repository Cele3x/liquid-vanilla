/**
 * Coerce a recipe rating into a plain number.
 *
 * Recipes are stored with an embedded rating object ({ rating, numVotes }) and the API
 * flattens it before serving. Guarding here keeps an unexpected shape from throwing
 * inside a render function, which would otherwise blank the whole recipe list.
 *
 * @param rating - Raw rating value as delivered by the API
 * @returns The rating as a number, or null when no usable value is present
 */
export function normalizeRating(rating: unknown): number | null {
  if (typeof rating === 'number' && !Number.isNaN(rating)) return rating
  if (rating && typeof rating === 'object' && 'rating' in rating) {
    return normalizeRating((rating as { rating: unknown }).rating)
  }
  return null
}
