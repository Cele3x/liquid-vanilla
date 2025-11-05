import { defineStore } from 'pinia'
import { tagService } from '@/services/tagService'

interface Tag {
  id: string
  name: string
  categoryId?: string
  usageCount?: number
  imageUrl?: string // Simple local image URL
  isEssential?: boolean
}

export const useTagStore = defineStore('tag', {
  state: () => ({
    tags: [] as Tag[],
    loading: false
  }),
  actions: {
    async fetchTags(essentialOnly: boolean = true) {
      if (this.loading) return

      this.loading = true
      try {
        const data = await tagService.getTags(essentialOnly)

        this.tags = data.map((tag: any) => ({
          id: tag.id,
          name: tag.name,
          categoryId: tag.categoryId,
          usageCount: tag.usageCount,
          isEssential: tag.isEssential,
          imageUrl: this.getLocalImageUrl(tag.name)
        }))
      } catch (error) {
        console.error('Fehler beim Laden der Kategorien:', error)
        // Use some default tags if API fails
        this.tags = this.getDefaultTags()
      } finally {
        this.loading = false
      }
    },

    getLocalImageUrl(tagName: string): string {
      // Convert tag name to normalized filename (lowercase, no special chars)
      const filename = tagName
        .toLowerCase()
        .replace(/ä/g, 'ae')
        .replace(/ö/g, 'oe')
        .replace(/ü/g, 'ue')
        .replace(/ß/g, 'ss')
        .replace(/[^a-z0-9]/g, '')

      return `/tag-images/${filename}.jpg`
    },

    getDefaultTags(): Tag[] {
      // ALL available tag names based on normalized filenames, organized by category
      const allTagNames = [
        // Popular Main Categories (most used)
        'Italien',
        'Deutschland',
        'Asien',
        'Amerika',
        'Frankreich',

        // Food Types
        'Fleisch',
        'Fisch',
        'Vegetarisch',
        'Vegan',
        'Geflügel',
        'Pasta',
        'Pizza',
        'Nudeln',
        'Reis',
        'Salat',

        // Meal Types
        'Hauptspeise',
        'Vorspeise',
        'Dessert',
        'Beilage',
        'Frühstück',
        'Snack',
        'Suppe',
        'Eintopf',

        // Baking & Sweets
        'Backen',
        'Backen oder Süßspeise',
        'Kuchen',
        'Torte',
        'Kekse',
        'Eis',
        'Süßspeise',

        // Cooking Methods
        'Grillen',
        'Braten',
        'Dünsten',
        'Schmoren',
        'Blanchieren',
        'Flambieren',
        'Frittieren',
        'Gekocht',
        'Gebunden',
        'Marinieren',
        'Überbacken',

        // Regions - Europe
        'Belgien',
        'Dänemark',
        'Finnland',
        'Griechenland',
        'Großbritannien',
        'Luxemburg',
        'Niederlande',
        'Norwegen',
        'Österreich',
        'Polen',
        'Portugal',
        'Russland',
        'Schweden',
        'Schweiz',
        'Skandinavien',
        'Spanien',
        'Tschechien',
        'Ungarn',
        'Weißrussland',

        // Regions - World
        'Afrika',
        'Australien',
        'China',
        'Indien',
        'Japan',
        'Karibik und Exotik',
        'Korea',
        'Latein Amerika',
        'Malta',
        'Marokko',
        'Mexiko',
        'Mittlerer und Naher Osten',
        'Südafrika',
        'Thailand',
        'Türkei',
        'USA oder Kanada',
        'Vietnam',
        'Ägypten',

        // Special Diets & Health
        'Low Carb',
        'Paleo',
        'Ketogen',
        'Gluten',
        'Lactose',
        'Diabetiker',
        'Ernährungskonzepte',
        'Fettarm',
        'Kalorienarm',
        'Trennkost',
        'Vollwert',

        // Occasions & Seasons
        'Party',
        'Festlich',
        'Weihnachten',
        'Ostern',
        'Halloween',
        'Silvester',
        'Sommer',
        'Winter',
        'Frühling',
        'Herbst',

        // Ingredients & Components
        'Käse',
        'Ei',
        'Eier',
        'Eier oder Käse',
        'Gemüse',
        'Kartoffel',
        'Kartoffeln',
        'Pilze',
        'Frucht',
        'Früchte',
        'Getreide',
        'Hülsenfrüchte',
        'Innereien',
        'Klöße',
        'Krustentier oder Fisch',
        'Krustentier oder Muscheln',
        'Lamm oder Ziege',
        'Meeresfrüchte',
        'Reis Getreide',
        'Rind',
        'Schwein',
        'Wild',
        'Wildgeflügel',

        // Preparation & Style
        'Schnell',
        'Einfach',
        'Raffiniert oder preiswert',
        'Spezial',
        'Cross Cooking',
        'Molekularküche',
        'Geheimrezept',
        'Grundrezepte',
        'Basisrezepte',
        'Resteverwertung',

        // Special Categories
        'Kinder',
        'Babynahrung',
        'Studentenküche',
        'Camping',
        'Fingerfood',
        'Mikrowelle',
        'Römertopf',
        'Wok',
        'Fondue',

        // Beverages & Drinks
        'Getränk',
        'Alkoholfrei',
        'Bowle',
        'Cocktail',
        'Kaffee',
        'Kaffee Tee oder Kakao',
        'Kakao',
        'Likör',
        'Longdrink',
        'Punsch',
        'Shake',
        'Tee',

        // Sauces & Sides
        'Aufstrich',
        'Brotspeise',
        'Brot oder Brötchen',
        'Creme',
        'Dips',
        'Einlagen',
        'Pasten',
        'Reis oder Nudelsalat',
        'Salat',
        'Salatdressing',
        'Saucen',
        'Tarte',

        // Preparations & Techniques
        'Auflauf',
        'Essig',
        'Gewürze',
        'Gewürze Öl Essig Pasten',
        'Haltbarmachen',
        'Konfiserie',
        'Mehlspeisen',
        'Öl',
        'Wursten',

        // Temperature & Consistency
        'Kalt',
        'Warm',
        'Klar',
        'Klare',
        'Klare Suppe',
        'Oder'
      ]

      return allTagNames.map((name, index) => ({
        id: (index + 1).toString(),
        name,
        imageUrl: this.getLocalImageUrl(name),
        isEssential: name !== 'Süß' && name !== 'Salzig'
      }))
    }
  }
})
