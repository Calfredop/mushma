---
kind: task
title: [bug] deploy-api.sh --run-job hangs after the job finishes: the silent ssh session dies
status: Done
priority: medium
complexity: simple
---
On 2026-10-01 a `Deploy API` run with `run_job=yes` sat at "running the daily job now" for over 30 minutes. On the server the job had finished at 07:57:35 UTC (`Result=success`, 885.6 s, API restarted by `ExecStartPost`). By 08:15 the server had no session left for the deploy, but the laptop's `ssh … bash -s` (deploy-api.sh line 68) was still waiting. Steps 4+ (health wait, smoke test, rules_version check) never ran. They were checked by hand: every route returned 200 and `/status` rules_version `0ff46e6bb2ba` matched the code.

Cause: `systemctl start mushma-daily.service` is `Type=oneshot`, so it blocks and prints nothing for about 15 minutes. The server's sshd has `ClientAliveInterval 300` / `ClientAliveCountMax 2` (deploy/harden-server.sh), and the client sends no keepalives. The connection died during the silence (the server closed it, or a NAT on the way dropped it), and the client never noticed.

Steps:
1. Add `-o ServerAliveInterval=30 -o ServerAliveCountMax=6` to the ssh in `deploy/deploy-api.sh`. Keepalives hold any NAT mapping open, and a dead link then fails within about 3 minutes instead of hanging.
2. Consider streaming progress while the job runs (e.g. `journalctl -fu mushma-daily` in the background until `systemctl start` returns), so a long run shows it is alive.
3. Check with a real `--run-job` deploy, which should end in "server: done" and the smoke test.

<!-- gavin:auto-commit -->
When the implementation is done, commit it. Commit only the files you touched — never `git add -A`. Do not push.
<!-- /gavin:auto-commit -->

- [ ] Human test: Push main (commit 03ef252), then run the "Deploy API" gavin tool with run_job=yes: the daily job's step-log lines should stream while it runs, and the run should end in "server: done", the smoke test and the rules_version check (the job can take up to an hour).
