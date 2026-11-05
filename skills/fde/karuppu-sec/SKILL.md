---
name: karuppu-sec
description: Use when hardening a Yazhi edge node before it leaves the lab — locking down a WireGuard mesh, writing firewall rules that survive a reboot, or scanning a repo for secrets before it is published. Helps you close the perimeter on air-gapped and peer-to-peer deployments without locking yourself out.
---

Karuppu owns the perimeter on nodes that are physically reachable and often on networks other people control. The two failure modes that matter: a firewall ruleset that works until reboot (then fails open), and a half-committed `.env` that puts credentials into a public repo.

## Workflow

1. **Inventory first.** `ss -ltnp` plus `ip addr` — every listener is attack surface, including the debug server someone started on `0.0.0.0:8000`.
2. **Write the deny-by-default chain.** Default `DROP` on INPUT, allow established/related, then explicitly allow SSH, WireGuard and the app port; confirm with `iptables -S`.
3. **Persist, then prove it.** Save via `iptables-persistent` (or an `nft` ruleset), restart the service, re-run `iptables -S`. A ruleset is not done until it survives a restart.
4. **Bind admin surfaces locally.** Postgres on `127.0.0.1:5432`, not `0.0.0.0`; `PasswordAuthentication no` with a key allowlist.
5. **Harden the mesh.** Per-peer `/32` allowed IPs (not `/0`), keepalive only on NAT'd sides, and a key-rotation note in the runbook.
6. **Scan for secrets.** `git grep -nE '(api_key|secret|password|token)\s*='`, inspect `git log -p` for deleted secrets, confirm `.env` is ignored — then rotate anything found. History rewriting is not a fix.
7. **Record the posture.** Commit the ruleset and a one-page note on what is exposed and why.

## Perimeter checklist

| Surface | Default | Allowed explicitly | Verification |
|---|---|---|---|
| SSH (22) | Drop | Key-only, allowlisted IPs | `sshd -T \| grep passwordauth` |
| WireGuard (51820/udp) | Drop | Known peers only | `wg show` |
| App port | Drop | Node subnet | `ss -ltnp` |
| Database | Drop | Loopback | `pg_hba.conf` |
| Outbound | Allow | — | `iptables -S OUTPUT` |

## Anti-patterns

- **Rules applied but never persisted.** The next reboot fails open or locks you out; test the reboot path.
- **`DROP` with no allow for your own session.** Always stage firewall changes with a second SSH session open.
- **Secrets removed from HEAD but still in history.** The credential is public the moment the repo is pushed — rotate it.
- **WireGuard peers allowed `0.0.0.0/0`.** Any peer becomes a route into everything; scope each peer to its `/32`.
- **Treating an unlisted port as protection.** Obscurity buys minutes against scanners, not safety.

For the threat-model step see `threat-modeling`, for review of perimeter-touching code see `secure-code-review`, and for secrets rotation see `incident-response`.
