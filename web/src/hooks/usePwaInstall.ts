import { useCallback, useEffect, useState } from 'react'

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>
}

function standalone(): boolean {
  return (
    window.matchMedia?.('(display-mode: standalone)').matches ||
    // iOS Safari has no `beforeinstallprompt`; this is its own way to say "already installed".
    (window.navigator as { standalone?: boolean }).standalone === true
  )
}

/** Chromium's install prompt (Safari/iOS never fires it — there's no install UI to offer there). */
export function usePwaInstall(): { available: boolean; install: () => void } {
  const [deferred, setDeferred] = useState<BeforeInstallPromptEvent | null>(null)
  const [installed, setInstalled] = useState(standalone)

  useEffect(() => {
    const onPrompt = (event: Event) => {
      event.preventDefault()
      setDeferred(event as BeforeInstallPromptEvent)
    }
    const onInstalled = () => {
      setInstalled(true)
      setDeferred(null)
    }
    window.addEventListener('beforeinstallprompt', onPrompt)
    window.addEventListener('appinstalled', onInstalled)
    return () => {
      window.removeEventListener('beforeinstallprompt', onPrompt)
      window.removeEventListener('appinstalled', onInstalled)
    }
  }, [])

  const install = useCallback(() => {
    if (!deferred) return
    void deferred.prompt()
    void deferred.userChoice.finally(() => setDeferred(null))
  }, [deferred])

  return { available: !installed && deferred !== null, install }
}
