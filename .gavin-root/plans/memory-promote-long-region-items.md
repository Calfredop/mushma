---
order: 17408
kind: note
labels: memory
title: A region card's species item is too long to promote
status: To Do
---
To give a region card's species research its own agent, create the child with `gavin_create_plan` (kind task, `parent: region-<slug>.md`, no status, file `region-<slug>-species.md`) and rewrite the item's start to `[Species research](./region-<slug>-species.md)` by hand; `gavin_promote_task` on that item fails.

Why: on 2026-09-27 `gavin_promote_task` on the Friuli-Venezia Giulia species item answered "File name too long (os error 63)": it names the new file after the item's whole text.
