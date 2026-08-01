import { describe, it, expect } from 'vitest'
import { normalizeRating } from '../rating'

describe('normalizeRating', () => {
  it('passes through a plain number', () => {
    expect(normalizeRating(4.25)).toBe(4.25)
    expect(normalizeRating(0)).toBe(0)
  })

  it('unwraps the embedded rating object stored on recipes', () => {
    expect(normalizeRating({ rating: 4.9000916701181065, numVotes: 654 })).toBe(4.9000916701181065)
  })

  it('returns null for missing or unusable values', () => {
    expect(normalizeRating(null)).toBeNull()
    expect(normalizeRating(undefined)).toBeNull()
    expect(normalizeRating(NaN)).toBeNull()
    expect(normalizeRating({})).toBeNull()
    expect(normalizeRating({ rating: null, numVotes: 0 })).toBeNull()
    expect(normalizeRating('4.5')).toBeNull()
  })

  it('always yields a value that is safe to render', () => {
    const raw = [4.5, { rating: 3.2, numVotes: 10 }, null, {}, 'nope']
    for (const value of raw) {
      const rating = normalizeRating(value)
      expect(rating === null || typeof rating.toFixed(1) === 'string').toBe(true)
    }
  })
})
