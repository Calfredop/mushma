---
order: 13312
kind: note
labels: memory
title: The shared data root must hold real folders, never links into a worktree
status: To Do
---
Keep every folder of the shared `DATA_DIR` (`mushma/api/data/{grid,weather,raw,sightings,…}`) a real directory in the root checkout; never symlink one into another worktree.

Why: on 2026-09-26 `grid`, `weather`, `raw` and `sightings` were symlinks into `mushma-backend/api/data`; removing that worktree deleted every region's local grid, weather history, download caches and sightings, unrecoverably.
