---
order: 4096
kind: task
title: Time bar overflows the map on narrow desktops
status: Done
priority: medium
complexity: simple
---
At a 1280 px wide window the desktop time bar (14 days plus the calendar button, 792 px, `flex: none`) is wider than its column in `.bottom` (656 px). It pokes 120 px past the map area's right edge, and once the date strip scrolls the selected day into view the whole `.app` container ends up scrolled sideways by 120 px: the wordmark and the panel are cut off on the left. It fits from about 1416 px up.

Found while adding the center-on-my-position button; it is there without that button (measured with the button removed and the old grid restored).

Reproduce: open the app in a 1280×800 window and look at the left edge, or read `document.querySelector('[class*="_app_"]').scrollLeft` (120, should be 0).

Fix it in `web/src/App.module.css` / `web/src/components/TimeBar`: let the bar shrink and scroll inside its column below the width where it fits (as it does on a phone) rather than overflow, and make sure nothing scrolls `.app` sideways. Check 900, 1024, 1280 and 1440 px, and that the center-on-my-position button above the row's end stays clear.
