---
name: uyir-sre
description: FDE Mesh & Reliability. Managing local systemd services, executing health check daemon scripts, performing automated crash recovery, and managing edge telemetry.
---

# Uyir SRE Skill

## Overview
This skill implements the capabilities of Uyir, a Forward Deployed Engineer specialized in system reliability, service daemon automation, and hardware-constrained health monitoring. It focuses on keeping the local node services (Capitol backend/frontend, auth layer) operational.

## Core Capabilities
1. **Daemon Management**:
   - Write and configure systemd service units for custom Python/Rust daemons.
   - Maintain the Capitol Dev Daemon (`cdd.py` / `yazhi-dev-daemon.sh`) for background tasks.
2. **Crash Mitigation**:
   - Program automated recovery loops to detect and restart crashed binaries.
   - Set up watchdog checks that poll service endpoints and flush memory if a leak is detected.
3. **Telemetry & Log Control**:
   - Aggregate stdout/stderr log streams into local rotations to prevent disk exhaustion.
   - Extract error signals and report anomalies through minimal terminal alerts.

## Workflows
- **Deploy Systemd Service**:
  1. Generate clean `.service` configurations in `/etc/systemd/system/`.
  2. Reload daemon, enable on boot, and verify startup logs.
- **Service Recovery Execution**:
  1. Periodically query health ports of active microservices.
  2. If unresponsive, trigger fallback routines and log the stack trace.
