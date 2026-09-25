#!/usr/bin/env bash
# Host-level guards for the production server (README.md -> Deploying -> Server security).
#
#   ssh root@api.mappafunghi.app bash -s < deploy/harden-server.sh
#
# Idempotent: rerun it on a rebuilt server, or to put the config back. It sets
#   - ufw: deny all incoming except SSH, HTTP and HTTPS (tcp, plus udp/443 for HTTP/3);
#   - sshd: key-only logins, no X11 or agent forwarding, fewer auth tries (a sshd_config.d drop-in);
#   - fail2ban: an sshd jail read from the journal, with longer bans for repeat offenders;
#   - unattended-upgrades: reboot on its own at 02:00 UTC when an update needs it, which is ahead
#     of the daily job (05:00 Europe/Rome, 03:00 or 04:00 UTC).
#
# Docker publishes ports through its own iptables chains, ahead of ufw's, so ufw never sees them:
# the Hetzner Cloud Firewall (set in the Hetzner console) is the layer that filters those. Publish
# nothing but Caddy's 80/443 in compose.yaml, or bind a port to 127.0.0.1.
set -euo pipefail

[ "$(id -u)" = 0 ] || { echo "run as root" >&2; exit 1; }
say() { printf '\n==> %s\n' "$*"; }

export DEBIAN_FRONTEND=noninteractive NEEDRESTART_MODE=a

say "Packages: ufw, fail2ban"
apt-get update -qq
apt-get install -y -qq ufw fail2ban python3-systemd >/dev/null

# --- sshd -----------------------------------------------------------------------------------------
# sshd keeps the first value it reads for each keyword and sshd_config includes sshd_config.d/*.conf
# at its top, so this file wins over sshd_config and over any later drop-in (50-cloud-init.conf).
# Root stays the login user, key only: the deploy scripts connect as root.
say "sshd: key-only"
cat >/etc/ssh/sshd_config.d/10-mushma.conf <<'EOF'
# Written by deploy/harden-server.sh in the mushma repo: edit it there, not here.
PermitRootLogin prohibit-password
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitEmptyPasswords no
AuthenticationMethods publickey
X11Forwarding no
AllowAgentForwarding no
MaxAuthTries 3
LoginGraceTime 20
ClientAliveInterval 300
ClientAliveCountMax 2
EOF
if ! sshd -t; then
  rm -f /etc/ssh/sshd_config.d/10-mushma.conf
  echo "sshd rejected the drop-in: removed it, sshd left as it was" >&2
  exit 1
fi
systemctl reload ssh

# --- ufw ------------------------------------------------------------------------------------------
# SSH is allowed before the firewall goes up, so the session running this survives it. ufw's own
# before-rules keep DHCP (Hetzner's IPv4) and IPv6 neighbour discovery working.
say "ufw: deny incoming except 22, 80, 443"
ufw default deny incoming >/dev/null
ufw default allow outgoing >/dev/null
ufw allow 22/tcp comment ssh >/dev/null
ufw allow 80/tcp comment 'http (caddy)' >/dev/null
ufw allow 443/tcp comment 'https (caddy)' >/dev/null
ufw allow 443/udp comment 'http3 (caddy)' >/dev/null
ufw --force enable >/dev/null

# --- fail2ban -------------------------------------------------------------------------------------
# aggressive mode: with passwords off, a bot guessing them only shows up as "Connection closed by
# authenticating user ... [preauth]", which the default (normal) mode doesn't count. A login that
# gets in never logs a [preauth] disconnect, so it never counts.
say "fail2ban: sshd jail"
cat >/etc/fail2ban/jail.local <<'EOF'
# Written by deploy/harden-server.sh in the mushma repo: edit it there, not here.
[DEFAULT]
backend = systemd
banaction = nftables-multiport
banaction_allports = nftables-allports
findtime = 10m
maxretry = 5
bantime = 1h
bantime.increment = true
bantime.maxtime = 1w
ignoreip = 127.0.0.1/8 ::1

[sshd]
enabled = true
mode = aggressive
EOF
fail2ban-client -t >/dev/null
systemctl enable fail2ban >/dev/null 2>&1
systemctl restart fail2ban

# --- unattended-upgrades --------------------------------------------------------------------------
# Security updates were already automatic; a kernel update just never took effect without a reboot.
# The server clock is UTC. Docker's own apt repo is not an allowed origin, so Docker (whose upgrade
# restarts every container) is only ever upgraded by hand.
say "unattended-upgrades: reboot at 02:00 UTC when needed"
cat >/etc/apt/apt.conf.d/52mushma-reboot <<'EOF'
// Written by deploy/harden-server.sh in the mushma repo: edit it there, not here.
Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-Time "02:00";
EOF

# --- what is now in force -------------------------------------------------------------------------
say "Status"
ufw status verbose
sshd -T | grep -E '^(permitrootlogin|passwordauthentication|kbdinteractiveauthentication|authenticationmethods|x11forwarding|allowagentforwarding|maxauthtries|logingracetime) '
fail2ban-client status sshd
apt-config dump | grep -E 'Unattended-Upgrade::Automatic-Reboot(-Time)? '
