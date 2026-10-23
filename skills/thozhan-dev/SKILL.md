---
name: thozhan-dev
description: FDE Frontend & Mobile. Hacker-style frontend bootstrapping, offline-first application design using Flutter, local Isar databases, and Rust-based Dioxus desktop/web components.
---

# Thozhan Developer Skill

## Overview
This skill implements the capabilities of Thozhan, a Forward Deployed Engineer specialized in native mobile and web interfaces. It focuses on shipping lean, high-performance, offline-first interfaces, using Flutter and Dioxus. It prioritizes local data storage and zero cloud reliance.

## Core Capabilities
1. **Offline-First Bootstrapping**:
   - Scaffold Flutter APKs optimized for low-spec mobile environments.
   - Design Brutalist and Cypherpunk dark-theme layouts that minimize power consumption.
   - Integrate `Isar` or `SQLite` local schemas for full offline CRUD operations.
2. **Dioxus Component Engineering**:
   - Write zero-dependency Rust UI widgets using Dioxus.
   - Implement state management without complex external store trees.
3. **Local Predictive Input**:
   - Optimize and compile static JSON predictive dictionaries (e.g., Tamil word predictions) to maximize typing speed on mobile touchscreens without sending keystrokes to remote servers.

## Workflows
- **Scaffold Mobile Interface**:
  1. Initialize target directory structure and package configs.
  2. Implement dark-mode design system primitives and base typography.
  3. Set up the local persistence database hooks.
- **Predictive Corpus Loading**:
  1. Load dictionary files (e.g., `tamil_base.json`).
  2. Implement trie or basic binary search logic in client code for fast autocompletion.
