---
kind: task
title: [sec] upgrade Docker Engine on the prod server
status: To Do
priority: medium
complexity: moderate
---
`mushma-prod-01` still runs Docker CE 27.5.1 (containerd.io 1.7.25, compose 2.32.4), which is out of upstream support. It won't upgrade on its own: the Hetzner "Docker CE" image ships `/etc/apt/preferences.d/docker-ce.pref`, which pins every download.docker.com package at priority 1 except `docker-ce` (500). So apt offers docker-ce 29.x, but that needs containerd.io >= 2.1.5, which the pin blocks, and `docker-ce` is always "kept back". Found during `sec-hetzner-server-security.md` (2026-09-25).

Upgrade the whole Docker set together (docker-ce, docker-ce-cli, containerd.io 2.x, docker-compose-plugin, docker-buildx-plugin, docker-ce-rootless-extras) to the current stable release:

1. Read the Docker 28 and 29 release notes for anything that affects this stack (`deploy/compose.yaml`: Caddy publishing 80/443 tcp and 443/udp, the api/umami/umami-db services, named volumes, json-file logging; the daily job's `docker compose run --rm`). Check that the containerd 1.7 → 2.x move keeps the existing overlay2 images and volumes (`caddy_data` holds the TLS certificates, `umami_db_data` the analytics).
2. Decide whether to delete the pin file or rewrite it (e.g. pin the Docker origin at 500). Keep the Docker origin OUT of unattended-upgrades' allowed origins, because a Docker upgrade restarts every container.
3. Only while nothing else is using the server (no `rsync`, no `-run-` container, `mushma-daily.service` inactive, no other agent deploying): upgrade, then `docker compose up -d` in `/opt/mushma/deploy`, then check `/health`, `/status`, the Umami heartbeat and the HTTPS certificate. Check that ufw and the `mushma-prod` Hetzner firewall still behave (only 22/80/443 reachable from outside).
4. Note the new versions and the pin decision in README → Deploying → Server security.

Do not push. Commit only the files you touch.
