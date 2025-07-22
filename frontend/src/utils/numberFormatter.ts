/**
 * Utility functions for formatting numbers with locale-specific delimiters
 */

/**
 * Format a number with German locale delimiters (dots for thousands, commas for decimals)
 * @param num - The number to format
 * @returns Formatted string with delimiters (e.g., 223.315)
 */
export const formatNumber = (num: number): string => {
  return num.toLocaleString('de-DE')
}

/**
 * Format a number for compact display (with K, M, B suffixes)
 * @param num - The number to format
 * @returns Compact formatted string (e.g., 223K, 1.5M)
 */
export const formatCompactNumber = (num: number): string => {
  if (num >= 1000000000) {
    return (num / 1000000000).toFixed(1).replace('.0', '') + 'B'
  } else if (num >= 1000000) {
    return (num / 1000000).toFixed(1).replace('.0', '') + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1).replace('.0', '') + 'K'
  }
  return num.toString()
}

/**
 * Format a number with custom decimal places
 * @param num - The number to format
 * @param decimals - Number of decimal places (default: 0)
 * @returns Formatted number string
 */
export const formatNumberWithDecimals = (num: number, decimals: number = 0): string => {
  return num.toLocaleString('de-DE', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  })
}