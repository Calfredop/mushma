---
order: 7168
kind: note
labels: memory
title: Run `uv sync --group cds` in a region checkout before the CDS backfill
status: To Do
---
In a region lane's checkout, run `uv sync --group cds` (from `api/`) before `ingest backfill --source cds`: the rail's "Sync with main" step reinstalls the api deps without the optional `cds` group, so the backfill stops with "cdsapi is not installed".

Why: on 2026-09-28 the Puglia lane's first CDS backfill failed on it after the sync step; `~/.cdsapirc` already held the key, only the packages were missing.
