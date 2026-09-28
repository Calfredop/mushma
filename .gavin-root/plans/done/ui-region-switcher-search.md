---
title: Region switcher: search + Mostra tutte
status: Done
priority: low
complexity: trivial
---
Add a dropdown header to `RegionSwitcher` (the picker on the region map) with a search field and a "Mostra tutte" link back to the hub.

- [x] Header in the open dropdown: search input that filters the region list by name (current locale)
- [x] "Mostra tutte" / "Show all" link navigates to `/` (hub) and closes the menu
- [x] i18n keys in it + en under `regions.*`
- [x] Tests for search filter and hub navigation
- [x] lint / format / test green
