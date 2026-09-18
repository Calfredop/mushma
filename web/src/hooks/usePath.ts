import { useCallback, useSyncExternalStore } from 'react'

const subscribe = (onChange: () => void) => {
  window.addEventListener('popstate', onChange)
  return () => window.removeEventListener('popstate', onChange)
}

/** The current pathname, plus in-app navigation that keeps the query string. */
export function usePath(): [string, (path: string) => void] {
  const path = useSyncExternalStore(subscribe, () => window.location.pathname)
  const navigate = useCallback((to: string) => {
    if (to === window.location.pathname) return
    window.history.pushState(null, '', `${to}${window.location.search}`)
    window.dispatchEvent(new PopStateEvent('popstate'))
    window.scrollTo?.(0, 0)
  }, [])
  return [path, navigate]
}
