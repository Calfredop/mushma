---
order: 2048
kind: note
title: Top-anchored UI starts at --safe-top-clear
status: To Do
labels: memory
---
Anything that must stay legible at the top of the screen is offset by `--safe-top-clear`, not `--safe-top`.

Why: iOS 26+ lays an un-disableable Liquid Glass blur over the top ~100pt of an installed web app, below the safe-area inset; `--safe-top-clear` (web/src/styles/tokens.css) includes it.
