---
order: 5120
title: [sec] hetzner server security
status: Done
complexity: complex
---
I need you to ssh and use chrome extension mcp to mappafunghi hetzner server, to setup firewall and security guards to the server

## Before (2026-09-25)

No host firewall, SSH still accepting password attempts, no fail2ban, stale authorized keys, and
a patched kernel installed but never booted.

## Checklist

- [x] Codify the host guards in `deploy/harden-server.sh`: idempotent, run from the laptop over
      SSH (ufw, sshd drop-in, fail2ban, unattended-upgrades auto-reboot)
- [x] Host firewall: ufw default deny incoming; allow 22/tcp, 80/tcp, 443/tcp, 443/udp (v4 + v6)
- [x] SSH: key-only (`PasswordAuthentication no`), no X11/agent forwarding, `MaxAuthTries 3`,
      shorter `LoginGraceTime`; validate with `sshd -t` and prove a fresh login before closing
- [x] fail2ban: sshd jail on the systemd journal, nftables bans, longer bans for repeat offenders
- [x] unattended-upgrades: reboot on its own when a kernel needs one, at 02:00 UTC (before the
      daily job at 05:00 Europe/Rome)
- [x] Hetzner Cloud Firewall via Chrome: a dedicated `mushma-prod` (inbound TCP 22/80/443, UDP 443,
      ICMP) on `mushma-prod-01` only, replacing the project's shared firewall there. It is the only
      layer that also filters Docker-published ports
- [x] Server delete/rebuild protection on in the Hetzner console
- [x] Prune authorized_keys to the deploy key `mappafunghi` only
- [x] Apply the pending updates (107 packages) and reboot onto kernel 6.8.0-142, once the other
      session's emilia_romagna rsync had finished (back in ~35 s). Docker stays at 27.5.1: the
      Hetzner image pins its repo, and 29 needs containerd 2.x. Follow-up: `sec-docker-engine-upgrade.md`
- [x] Verify from outside: open ports, site + API + Umami up, default Umami login refused,
      daily timer still scheduled
- [x] README: a "Server security" part under Deploying (both firewall layers, the script, lockout
      recovery); add the script to the first-setup steps
- [x] Commit

<!-- gavin:auto-commit -->
When the implementation is done, commit it. Commit only the files you touched — never `git add -A`. Do not push.
<!-- /gavin:auto-commit -->
