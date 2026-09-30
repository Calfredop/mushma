---
order: 18432
labels: memory
kind: note
title: Give a region's CDS backfill a background timeout of about two hours
status: To Do
---
When an agent runs `api.weather.ingest backfill --source cds` as a background command, set its timeout to about two hours (7,200,000 ms): the default 30-minute background limit kills it before a 50-node region is fetched, and it writes nothing to the weather store until every node is in.

Why: on 2026-09-30 Basilicata's backfill was killed at 36 of 51 nodes after 30 minutes; the node downloads were cached under `raw/cds/`, so a rerun resumed and finished in 13 minutes.
