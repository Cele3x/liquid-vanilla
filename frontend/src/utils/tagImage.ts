/**
 * Resolve the illustration shown on a tag card.
 *
 * Tag images are shipped as static files under `public/tag-images/` and matched to a
 * tag by its name, because tags carry no image reference of their own. The name is
 * folded to the filename convention the files were stored under: lowercase, German
 * umlauts spelled out, and everything that is not a letter or digit removed, so
 * "Räucherfisch & Co." and "raeucherfischco" name the same file. Filenames are matched
 * exactly rather than case-insensitively - the production server's filesystem is case
 * sensitive even though a Mac's is not.
 *
 * Not every tag has an image; callers should handle the file being absent rather than
 * assume the returned URL resolves.
 *
 * @param tagName - Tag name as stored in the database
 * @returns Absolute URL of the tag image, or null when the name normalizes to nothing
 */
export function tagImageUrl(tagName: string): string | null {
  const filename = tagName
    .toLowerCase()
    .replace(/ä/g, 'ae')
    .replace(/ö/g, 'oe')
    .replace(/ü/g, 'ue')
    .replace(/ß/g, 'ss')
    .replace(/[^a-z0-9]/g, '')

  if (!filename) return null

  return `/tag-images/${filename}.webp`
}
