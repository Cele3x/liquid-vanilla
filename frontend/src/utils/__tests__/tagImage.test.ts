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
    expect(tagImageUrl('Brot oder Brötchen')).toBe('/tag-images/brotoderbroetchen.webp')
    expect(tagImageUrl('Eier oder Käse')).toBe('/tag-images/eieroderkaese.webp')
    expect(tagImageUrl('Cross-Cooking')).toBe('/tag-images/crosscooking.webp')
    expect(tagImageUrl('Raffiniert oder preiswert')).toBe(
      '/tag-images/raffiniertoderpreiswert.webp'
    )
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
