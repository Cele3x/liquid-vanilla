import { describe, it, expect, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useTagStore } from '../tagStore'

describe('tagStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  describe('tagNameById', () => {
    it('resolves a tag id to its display name', () => {
      const store = useTagStore()
      store.tags = [
        { id: 'a1', name: 'Hauptspeise', usage_count: 3 },
        { id: 'b2', name: 'Vegetarisch', usage_count: 2 }
      ]

      expect(store.tagNameById('a1')).toBe('Hauptspeise')
      expect(store.tagNameById('b2')).toBe('Vegetarisch')
    })

    it('returns null for an unknown id so cards hide it instead of showing the raw id', () => {
      const store = useTagStore()
      store.tags = [{ id: 'a1', name: 'Hauptspeise', usage_count: 3 }]

      expect(store.tagNameById('6628c62d9b0fefc37a4de8d9')).toBeNull()
    })

    it('returns null for every id before the tags have loaded', () => {
      const store = useTagStore()

      expect(store.tags).toEqual([])
      expect(store.tagNameById('a1')).toBeNull()
    })
  })

  describe('cardTags', () => {
    const manyTags = [
      { id: 'a1', name: 'Reis', usage_count: 900 },
      { id: 'b2', name: 'Kinder', usage_count: 700 },
      { id: 'c3', name: 'Snack', usage_count: 800 },
      { id: 'd4', name: 'Camping', usage_count: 5 },
      { id: 'e5', name: 'Party', usage_count: 10 }
    ]

    it('keeps the three most used tags and counts the rest as hidden', () => {
      const store = useTagStore()
      store.tags = manyTags

      const tags = store.cardTags(['d4', 'b2', 'e5', 'a1', 'c3'])

      expect(tags.names).toEqual(['Reis', 'Snack', 'Kinder'])
      expect(tags.hiddenCount).toBe(2)
    })

    it('lists every resolved tag for the hover tooltip on the overflow hint', () => {
      const store = useTagStore()
      store.tags = manyTags

      const tags = store.cardTags(['d4', 'b2', 'e5', 'a1', 'c3'])

      expect(tags.allNames).toEqual(['Reis', 'Snack', 'Kinder', 'Party', 'Camping'])
    })

    it('stops early when long tags already fill the line, rather than truncating', () => {
      const store = useTagStore()
      store.tags = [
        { id: 'x1', name: 'Studentenküche', usage_count: 900 },
        { id: 'x2', name: 'Hauptspeise', usage_count: 800 },
        { id: 'x3', name: 'Vegetarisch', usage_count: 700 }
      ]

      const tags = store.cardTags(['x1', 'x2', 'x3'])

      expect(tags.names).toEqual(['Studentenküche', 'Hauptspeise'])
      expect(tags.hiddenCount).toBe(1)
    })

    it('still shows three tags when they are short enough to fit', () => {
      const store = useTagStore()
      store.tags = [
        { id: 'y1', name: 'Reis', usage_count: 900 },
        { id: 'y2', name: 'Snack', usage_count: 800 },
        { id: 'y3', name: 'Kinder', usage_count: 700 },
        { id: 'y4', name: 'Party', usage_count: 600 }
      ]

      const tags = store.cardTags(['y1', 'y2', 'y3', 'y4'])

      expect(tags.names).toEqual(['Reis', 'Snack', 'Kinder'])
      expect(tags.hiddenCount).toBe(1)
    })

    it('always shows the first tag even when it alone exceeds the budget', () => {
      const store = useTagStore()
      store.tags = [
        { id: 'z1', name: 'Hauptspeise mit Beilage und Sauce', usage_count: 900 },
        { id: 'z2', name: 'Snack', usage_count: 800 }
      ]

      const tags = store.cardTags(['z1', 'z2'])

      expect(tags.names).toEqual(['Hauptspeise mit Beilage und Sauce'])
      expect(tags.hiddenCount).toBe(1)
    })

    it('reports no overflow when a recipe has at most three tags', () => {
      const store = useTagStore()
      store.tags = manyTags

      const tags = store.cardTags(['a1', 'b2'])

      expect(tags.names).toEqual(['Reis', 'Kinder'])
      expect(tags.hiddenCount).toBe(0)
    })

    it('drops unresolvable ids rather than counting them towards the overflow', () => {
      const store = useTagStore()
      store.tags = manyTags

      const tags = store.cardTags(['a1', 'deadbeefdeadbeefdeadbeef', 'b2', 'c3', 'e5'])

      expect(tags.names).toEqual(['Reis', 'Snack', 'Kinder'])
      expect(tags.hiddenCount).toBe(1)
      expect(tags.allNames).not.toContain('deadbeefdeadbeefdeadbeef')
    })

    it('returns nothing before the tags have loaded', () => {
      const store = useTagStore()

      expect(store.cardTags(['a1'])).toEqual({ names: [], hiddenCount: 0, allNames: [] })
    })
  })
})
