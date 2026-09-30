---
order: 14336
kind: note
title: Hetzner Docker CE pin
labels: memory
status: To Do
---
Hetzner's "Docker CE" image ships `/etc/apt/preferences.d/docker-ce.pref` that pins every download.docker.com package at priority 1 except `docker-ce` (500); rewrite it to pin the whole origin at 500 so upgrades can move together, and keep that origin out of unattended-upgrades.

Why: otherwise apt offers docker-ce 29.x but blocks containerd.io 2.x, and docker-ce stays "kept back" forever.
