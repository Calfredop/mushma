/** Stroke icons on a 24px grid, drawn in currentColor. Decorative: label the control, not the icon. */
import type { SVGProps } from 'react'

function Icon({ children, ...props }: SVGProps<SVGSVGElement>) {
  return (
    <svg
      width="22"
      height="22"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      focusable="false"
      {...props}
    >
      {children}
    </svg>
  )
}

export const SearchIcon = () => (
  <Icon>
    <circle cx="10.5" cy="10.5" r="6.5" />
    <path d="m15.5 15.5 5 5" />
  </Icon>
)

export const LocateIcon = () => (
  <Icon>
    <circle cx="12" cy="12" r="7" />
    <circle cx="12" cy="12" r="2.2" fill="currentColor" stroke="none" />
    <path d="M12 2v3M12 19v3M2 12h3M19 12h3" />
  </Icon>
)

export const CloseIcon = () => (
  <Icon>
    <path d="M6 6l12 12M18 6 6 18" />
  </Icon>
)

export const ChevronIcon = ({
  direction,
}: {
  direction: 'up' | 'down' | 'left' | 'right'
}) => {
  const rotate = { up: 180, down: 0, left: 90, right: -90 }[direction]
  return (
    <Icon style={{ transform: `rotate(${rotate}deg)` }}>
      <path d="m6 9 6 6 6-6" />
    </Icon>
  )
}

export const InfoIcon = () => (
  <Icon>
    <circle cx="12" cy="12" r="9" />
    <path d="M12 11v6M12 7.5v.01" />
  </Icon>
)

export const PlusIcon = () => (
  <Icon>
    <path d="M12 5v14M5 12h14" />
  </Icon>
)

export const MinusIcon = () => (
  <Icon>
    <path d="M5 12h14" />
  </Icon>
)

export const CalendarIcon = () => (
  <Icon>
    <rect x="3.5" y="5" width="17" height="15" rx="2" />
    <path d="M3.5 10h17M8 3v4M16 3v4" />
    <path d="M8 14h2M14 14h2M8 17h2" />
  </Icon>
)

export const DownloadIcon = () => (
  <Icon>
    <path d="M12 3v12M7 10.5 12 15.5 17 10.5" />
    <path d="M4.5 19.5h15" />
  </Icon>
)

export const OfflineIcon = () => (
  <Icon>
    <path d="M3 3l18 18" />
    <path d="M8.5 8.7A9.9 9.9 0 0 0 3.5 11" />
    <path d="M12 5c3.2 0 6.2 1.1 8.5 3" />
    <path d="M6.8 12.4a5.9 5.9 0 0 1 3.4-1.8" />
    <path d="M9.5 15.8a2.9 2.9 0 0 1 3-.7" />
    <circle cx="12" cy="19" r="1" fill="currentColor" stroke="none" />
  </Icon>
)

export const PlayIcon = () => (
  <Icon>
    <path d="M8 5.5v13l10.5-6.5z" fill="currentColor" />
  </Icon>
)

export const PauseIcon = () => (
  <Icon>
    <path d="M8.5 5.5v13M15.5 5.5v13" strokeWidth="3" />
  </Icon>
)

/** Stacked sheets: the factors drawn as layers. */
export const LayersIcon = () => (
  <Icon>
    <path d="m12 4 8.5 4.5L12 13 3.5 8.5z" />
    <path d="m3.5 12.5 8.5 4.5 8.5-4.5" />
    <path d="m3.5 16.5 8.5 4.5 8.5-4.5" />
  </Icon>
)
