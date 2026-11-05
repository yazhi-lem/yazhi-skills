---
name: uyir-sre
description: Use when a Yazhi edge node's background services have died, are looping, or are quietly filling the disk — the Capitol backend, frontend or auth daemon misbehaving on a box you cannot easily reach. Helps you deploy, watchdog and recover systemd-managed daemons on hardware-constrained nodes without turning an outage into a disk-full incident.
---

Uyir keeps the local node services (Capitol backend, frontend, auth layer) alive on machines with no cloud fallback and no on-call rotation. The failure that hurts is rarely a crash you notice — it is a daemon that restarts 4,000 times overnight and silently fills the disk with logs.

## Workflow

1. **Audit before writing a unit.** List what is listening (`ss -ltnp`) and what is enabled (`systemctl list-unit-files --state=enabled`). A unit duplicating an existing listener fails at boot in a way that looks like a code bug.
2. **Write the unit with restart limits.** `Restart=on-failure`, `RestartSec=3`, plus `StartLimitIntervalSec=300` and `StartLimitBurst=5` so a crash loop ends in `failed` instead of spinning forever.
3. **Cap logs at the unit.** `StandardOutput=journal` with a rate limit; never let an app write unbounded files into `/var/log`.
4. **Deploy and verify readback.** `systemctl daemon-reload`, `enable --now`, then read `journalctl -u <unit> -n 50` and confirm the port is bound.
5. **Probe behaviour, not liveness.** A `/health` returning 200 while the database is disconnected is worse than none — assert a real read.
6. **Recover deliberately.** On watchdog failure capture `systemctl status`, the last 100 journal lines, and `systemctl show -p MemoryCurrent` *before* restarting; the evidence dies with the restart.

## Service posture by role

| Service | Restart policy | Health signal | Disk risk |
|---|---|---|---|
| Capitol API | `on-failure`, burst 5 | DB read + HTTP 200 | Request logs |
| Frontend | `on-failure`, burst 5 | Static asset fetch | Build cache |
| Auth layer | `always` (security-critical) | Token issuance round-trip | Audit log |
| Scrape/cron daemon | `no` (exit is normal) | Last-run timestamp | Raw corpus |

## Defaults

- `RestartSec=3`, burst 5 in 300s; anything faster is a deployment bug.
- Log rotation: 50 MB per service, keep 3 — sized for an 8 GB SD card.
- Alert on more than 3 restarts in 10 minutes, or RSS growth over 20% in an hour.

## Anti-patterns

- **`Restart=always` on a crash-looping unit.** It hides the error and burns CPU on a weak node; bound the burst instead.
- **Unbounded log capture.** An error loop writes gigabytes in minutes on an edge device.
- **Health checks that only prove the process is alive.** A 200 from a dead-database service is a false green.
- **Restarting before capturing state.** You destroy the only evidence of the failure.
- **Editing a unit already on disk without `daemon-reload`.** systemd keeps the old definition and the fix silently does nothing.

For deploy sequencing see `deployment-runbook`, for incident process see `incident-response`, and for node hardening see `karuppu-sec`.
