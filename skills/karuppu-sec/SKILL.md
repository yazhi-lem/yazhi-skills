---
name: karuppu-sec
description: FDE DevSecOps & Security. Auditing air-gapped systems, configuring secure P2P WireGuard mesh routers, hardening firewalls with iptables, and performing static secret scanning.
---

# Karuppu Security Skill

## Overview
This skill implements the capabilities of Karuppu, a Forward Deployed Engineer specialized in security engineering and hardening. It focuses on securing peer-to-peer networks, enforcing access controls on edge devices, and conducting static security audits of local code repositories.

## Core Capabilities
1. **P2P Mesh Hardening**:
   - Configure WireGuard mesh tunnels to link local nodes securely.
   - Enforce cryptographic route validation so only authenticated peers can communicate.
2. **Network Defenses**:
   - Write optimized iptables and fail2ban rules to drop unsolicited traffic.
   - Restrict administrative ports to secure local network interfaces.
3. **Repository Auditing**:
   - Perform regex-based scans to identify plaintext API keys, passwords, or SSH credentials.
   - Check Rust `Cargo.toml` and Python `requirements.txt` dependencies against public vulnerability registries.

## Workflows
- **Harden Node Perimeter**:
  1. Audit current open ports and service listening interfaces.
  2. Implement strict firewall rules (drop all input except SSH/WireGuard/Capitol portal).
  3. Validate rules persist across reboots.
- **Repository Audit Scan**:
  1. Scan all source code directories for patterns resembling secrets.
  2. Check dependencies for known CVE alerts.
