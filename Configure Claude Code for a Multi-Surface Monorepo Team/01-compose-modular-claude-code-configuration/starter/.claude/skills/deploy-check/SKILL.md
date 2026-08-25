---
name: deploy-check
description: Pre-deployment validation in an isolated fork session
context: fork
allowed-tools:
  - Read
  - Glob
  - Grep
---

# /deploy-check — Isolated Pre-Deployment Validation

This skill runs a read-only sequence of checks **in a forked session** before merging to main. It keeps verbose discovery output, logs, and intermediate findings out of the main conversation thread.

## Three Pre-Deployment Checks

### ✓ Check 1: Build Integrity

**Detect**: Run `npm run build` and capture exit code and stderr.

**Pass criterion**: Exit code is 0, no TypeScript errors, no unresolved imports.

**Fail criterion**: Build fails, type errors present, or bundle exceeds 500KB growth.

### ✓ Check 2: Test Suite Completeness

**Detect**: Run `npm run test -- --coverage` and parse coverage report.

**Pass criterion**: Overall coverage ≥80%, all handler files have ≥80% line coverage.

**Fail criterion**: Coverage below threshold, any handler untested, or test runs fail.

### ✓ Check 3: Database Migration Safety

**Detect**: Parse migrations from `src/db/migrations/` and check for forward-only safety (no DROP TABLE without corresponding CREATE TABLE in same file).

**Pass criterion**: All migrations are forward-only, no destructive operations detected.

**Fail criterion**: Destructive operations found or migration files reference tables that don't exist.

## Isolation and Branching Reality

The goal of running in a **fork** is to keep verbose pre-deployment output (build logs, test output, migration analysis) isolated from the main session. This follows the **Playbook Branching Reality pattern**: you maintain a main "user-facing" session and fork into a temporary workspace for discovery and validation, then report conclusions back to main without cluttering the primary thread.

## Personal Customization

Team members can extend or override this skill by adding custom checks to `~/.claude/skills/deploy-check/SKILL.md`. Personal skills are not version-controlled, so each engineer can tailor deployment checks to their workflow without affecting teammates.

## Skill vs CLAUDE.md Decision Rubric

### Use a Skill (like `/deploy-check`) when:

- **On-demand only**: You invoke it before specific actions (pre-deployment), not as a default behavior.
- **Forked safety**: You want output isolation and don't mind running in a temporary session.
- **Lower entry barrier**: Teammates can customize via `~/.claude/skills/` without merging git changes.
- **Specific trigger**: The check is not universally relevant to every editing session.

### Use CLAUDE.md when:

- **Always-on**: You want rules and standards loaded in every session (e.g., path-scoped conventions).
- **Shared team standard**: The configuration must be versioned and reviewed collectively.
- **Fast feedback**: You need immediate guidance without invoking a special command.
- **Discovery-friendly**: You want Claude to proactively enforce conventions during normal development.

**Decision**: `/deploy-check` is a skill (not in CLAUDE.md) because it runs on explicit invocation, benefits from fork isolation, and is not universally blocking.
