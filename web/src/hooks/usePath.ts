import { useCallback, useSyncExternalStore } from 'react'

const subscribe = (onChange: () => void) => {
  window.addEventListener('popstate', onChange)
  return () => window.removeEventListener('popstate', onChange)
}

export interface NavigateOptions {
  /** Query string to use instead of the current one. */
  search?: string
  /** `replaceState` instead of `pushState`: no back-button stop, no scroll reset. */
  replace?: boolean
}

export type Navigate = (path: string, options?: NavigateOptions) => void

/** The current pathname, plus in-app navigation that keeps the query string by default. */
export function usePath(): [string, Navigate] {
  const path = useSyncExternalStore(subscribe, () => window.location.pathname)
  const navigate = useCallback((to: string, options: NavigateOptions = {}) => {
    const search = options.search ?? window.location.search
    const href = `${to}${search}`
    if (href === `${window.location.pathname}${window.location.search}`) return
    if (options.replace) {
      window.history.replaceState(window.history.state, '', href)
    } else {
      window.history.pushState(null, '', href)
    }
    window.dispatchEvent(new PopStateEvent('popstate'))
    if (!options.replace) window.scrollTo?.(0, 0)
  }, [])
  return [path, navigate]
}
