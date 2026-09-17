/** Helpers behind the locale completeness check (locales.test.ts). */

type Messages = { [key: string]: string | Messages }

export function flattenKeys(messages: Messages, prefix = ''): string[] {
  return Object.entries(messages).flatMap(([key, value]) => {
    const path = prefix ? `${prefix}.${key}` : key
    return typeof value === 'string' ? [path] : flattenKeys(value, path)
  })
}

function leaf(messages: Messages, path: string): string | undefined {
  let node: string | Messages | undefined = messages
  for (const part of path.split('.')) {
    if (node === undefined || typeof node === 'string') return undefined
    node = node[part]
  }
  return typeof node === 'string' ? node : undefined
}

export function placeholders(text: string): string[] {
  const names = [...text.matchAll(/\{\{\s*([\w.]+)\s*(?:,[^}]*)?\}\}/g)].map((m) => m[1])
  return [...new Set(names)].sort()
}

export interface LocaleComparison {
  /** In `base` but not in `other`. */
  missing: string[]
  /** In `other` but not in `base`. */
  extra: string[]
  /** Blank in `other`. */
  empty: string[]
  /** Present in both but with different `{{variables}}`. */
  placeholderMismatches: string[]
}

export function compareLocales(base: Messages, other: Messages): LocaleComparison {
  const baseKeys = flattenKeys(base)
  const otherKeys = flattenKeys(other)
  const otherSet = new Set(otherKeys)
  const baseSet = new Set(baseKeys)
  const shared = baseKeys.filter((key) => otherSet.has(key))

  return {
    missing: baseKeys.filter((key) => !otherSet.has(key)),
    extra: otherKeys.filter((key) => !baseSet.has(key)),
    empty: otherKeys.filter((key) => leaf(other, key)?.trim() === ''),
    placeholderMismatches: shared.filter(
      (key) =>
        placeholders(leaf(base, key) ?? '').join() !==
        placeholders(leaf(other, key) ?? '').join(),
    ),
  }
}
