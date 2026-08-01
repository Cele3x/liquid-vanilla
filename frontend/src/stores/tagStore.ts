import { defineStore } from 'pinia'
import { tagService } from '@/services/tagService'
import { formatNumber } from '@/utils/numberFormatter'

interface Tag {
  id: string
  name: string
  usage_count: number
  categoryId?: string | null
}

/**
 * Most tags a recipe card shows before the rest collapse into a "+n" indicator.
 *
 * Recipes carry up to a dozen tags, which wrapped onto four lines and made the
 * cards in a grid row differ in height. One line per card keeps them even.
 */
export const RECIPE_CARD_TAG_LIMIT = 3

/**
 * Characters that fit on a card's single tag line.
 *
 * The limit above is not enough on its own: three short tags fit where two long
 * ones like STUDENTENKÜCHE already fill the row. The narrowest card is the
 * four-column breakpoint at roughly 280px of content, which holds about 32
 * uppercase characters at text-xs; the budget leaves room for the gaps between
 * tags and for the "+n" indicator itself.
 */
export const RECIPE_CARD_TAG_CHAR_BUDGET = 26

export interface CardTags {
  names: string[]
  hiddenCount: number
  allNames: string[]
}

export const useTagStore = defineStore('tag', {
  state: () => ({
    tags: [] as Tag[],
    loading: false
  }),
  getters: {
    /**
     * Resolve a tag id to its display name.
     *
     * Recipes carry tag ids, so views need the loaded tag list to show names.
     * Returns null when the tags have not loaded yet or the id is unknown, which
     * lets callers hide the tag rather than render a raw object id.
     */
    tagNameById: (state) => {
      const namesById = new Map(state.tags.map((tag) => [tag.id, tag.name]))
      return (id: string): string | null => namesById.get(id) ?? null
    },

    /**
     * Resolve a recipe's tag ids into the few tags a card has room for.
     *
     * The most used tags win, so cards label recipes with the categories readers
     * recognise. Names are taken until either the count or the character budget
     * for one line runs out, which stops two long tags from being squeezed to
     * ellipses on a narrow card; at least one tag always survives. Unresolvable
     * ids are dropped rather than shown as raw object ids, and everything left
     * over is reported as a count the card can show as a "+n" hint. The full
     * list travels along for that hint's hover tooltip.
     *
     * :param ids: tag ids as stored on the recipe
     * :returns: the names to render, how many stayed hidden, and every name
     */
    cardTags: (state) => {
      const tagsById = new Map(state.tags.map((tag) => [tag.id, tag]))
      return (ids: string[]): CardTags => {
        const resolved = ids
          .map((id) => tagsById.get(id))
          .filter((tag): tag is Tag => tag !== undefined)
          .sort((a, b) => (b.usage_count ?? 0) - (a.usage_count ?? 0))

        const allNames = resolved.map((tag) => tag.name)

        const names: string[] = []
        let usedChars = 0
        for (const name of allNames.slice(0, RECIPE_CARD_TAG_LIMIT)) {
          // The first tag goes in regardless: a card with one very long tag
          // should still name it rather than show a bare "+n".
          if (names.length && usedChars + name.length > RECIPE_CARD_TAG_CHAR_BUDGET) break
          names.push(name)
          usedChars += name.length
        }

        return {
          names,
          hiddenCount: allNames.length - names.length,
          allNames
        }
      }
    }
  },
  actions: {
    async fetchTags() {
      if (this.loading) return

      this.loading = true
      try {
        const data = await tagService.getTags()
        this.tags = data
        console.log(
          'Tags fetched:',
          data.slice(0, 3).map((t: Tag) => `${t.name}: ${formatNumber(t.usage_count)} recipes`)
        )
      } catch (error) {
        console.error('Failed to fetch tags:', error)
      } finally {
        this.loading = false
      }
    },

    async forceRefreshTags() {
      this.loading = true
      try {
        const data = await tagService.getTags()
        this.tags = data
        console.log(
          'Tags force refreshed:',
          data.slice(0, 3).map((t: Tag) => `${t.name}: ${formatNumber(t.usage_count)} recipes`)
        )
      } catch (error) {
        console.error('Failed to force refresh tags:', error)
      } finally {
        this.loading = false
      }
    }
  }
})
