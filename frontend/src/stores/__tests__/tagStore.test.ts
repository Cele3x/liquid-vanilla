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
})
