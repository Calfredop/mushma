/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL?: string
  readonly VITE_BASEMAP_URL?: string
  readonly VITE_TERRAIN_URL?: string
  /** Self-hosted Umami (feat-umami-integration.md); unset means analytics never loads. */
  readonly VITE_UMAMI_SRC?: string
  readonly VITE_UMAMI_WEBSITE_ID?: string
  readonly VITE_UMAMI_DOMAINS?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
