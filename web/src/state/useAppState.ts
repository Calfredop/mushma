import { useContext } from 'react'
import { AppStateContext, type AppStateValue } from './AppState'

export function useAppState(): AppStateValue {
  const value = useContext(AppStateContext)
  if (!value) throw new Error('useAppState needs <AppStateProvider>')
  return value
}
