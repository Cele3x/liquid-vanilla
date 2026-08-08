import { describe, it, expect } from 'vitest'
import { tagImageUrl } from '../tagImage'

describe('tagImageUrl', () => {
  it('lowercases the tag name', () => {
    expect(tagImageUrl('Italien')).toBe('/tag-images/italien.webp')
    expect(tagImageUrl('BACKEN')).toBe('/tag-images/backen.webp')
  })

  it('spells out German umlauts the way the files are named', () => {
    expect(tagImageUrl('Ägypten')).toBe('/tag-images/aegypten.webp')
    expect(tagImageUrl('Österreich')).toBe('/tag-images/oesterreich.webp')
    expect(tagImageUrl('Dünsten')).toBe('/tag-images/duensten.webp')
    expect(tagImageUrl('Süßspeise')).toBe('/tag-images/suessspeise.webp')
  })

  it('drops separators and punctuation', () => {
    expect(tagImageUrl('Brot & Brötchen')).toBe('/tag-images/brotbroetchen.webp')
    expect(tagImageUrl('Nudel- & Reissalat')).toBe('/tag-images/nudelreissalat.webp')
    expect(tagImageUrl('Gewürze, Öl & Essig')).toBe('/tag-images/gewuerzeoelessig.webp')
    expect(tagImageUrl('Cross-Cooking')).toBe('/tag-images/crosscooking.webp')
  })

  it('keeps digits', () => {
    expect(tagImageUrl('Resteverwertung 2')).toBe('/tag-images/resteverwertung2.webp')
  })

  it('returns null when nothing survives normalization', () => {
    expect(tagImageUrl('')).toBeNull()
    expect(tagImageUrl('---')).toBeNull()
    expect(tagImageUrl('   ')).toBeNull()
  })
})
