import { Component, type ReactNode } from 'react'
import { Translation } from 'react-i18next'
import panel from '../panels/panel.module.css'

interface Props {
  children: ReactNode
  /** Changing it (another view, species or area) tries the panel again. */
  resetKey: string
}

interface State {
  failedFor: string | null
}

/** One panel failing (say, a response from an older API) must not blank the map. */
export class PanelBoundary extends Component<Props, State> {
  state: State = { failedFor: null }

  static getDerivedStateFromError(): Partial<State> {
    return { failedFor: '' }
  }

  componentDidCatch() {
    this.setState({ failedFor: this.props.resetKey })
  }

  render() {
    const { failedFor } = this.state
    if (failedFor !== null && (failedFor === '' || failedFor === this.props.resetKey)) {
      return (
        <Translation>
          {(t) => (
            <p className={panel.status} role="alert">
              {t('errors.generic')}
            </p>
          )}
        </Translation>
      )
    }
    return this.props.children
  }
}
