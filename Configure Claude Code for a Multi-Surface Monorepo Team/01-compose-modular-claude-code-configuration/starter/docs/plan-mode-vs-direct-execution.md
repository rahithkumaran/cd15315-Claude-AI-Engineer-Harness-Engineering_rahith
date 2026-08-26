# Plan Mode vs Direct Execution Decision Guide

This guide explains when to use Claude's three interaction modes: **plan mode** (explore + design before implementation), **direct execution** (implement immediately), and **Explore subagent** (isolate discovery).

---

## Plan Mode: Multi-File Architectural Changes

Use plan mode when your task touches **≥3 files** and involves architectural or design decisions. Plan mode prevents costly rework.

### Example: Add User Session Management

**Scenario**: The team decides to implement session-based authentication across the app.

**Files affected** (≥3 files):
1. `.claude/standards/api.md` — reference API design pattern
2. `.claude/standards/database.md` — reference DB layer pattern
3. `.claude/rules/api.md` — add session-specific API rules

**Plan mode investigation**:
- Review `.claude/standards/api.md` to understand handler patterns.
- Check `.claude/standards/database.md` for repository conventions.
- Study existing `.claude/rules/api.md` to see error handling enforcement.
- Design a cohesive approach: where does session data live? How long are sessions valid?

**Why plan mode**: Without upfront design, you might implement session storage with a different approach than the existing patterns. Prevent costly rework by aligning on architecture first.

---

## Direct Execution: Single, Well-Scoped Functions

Use direct execution when implementing a **single well-scoped function** with clear requirements and no cross-cutting architectural implications.

### Example: Implement a Password Strength Validator

**Scenario**: The validation policy is already documented. You need to implement one function.

**Scope**: One function in one file, no dependencies on other modules being changed.

**Direct approach**:
1. Implement the validation function: check length, character types, blacklist.
2. Add unit tests for the function in a co-located test file.
3. Integrate the function into an existing API handler (no structural changes).
4. Done.

**Why direct execution**: Single function, clear requirements, no upstream or downstream architectural questions. No planning overhead needed.

---

## Explore Subagent: Discovery with Isolated Output

Use the Explore subagent when you need to **gather information across multiple files** but don't want verbose discovery output in the main session. This mirrors the **Playbook Scratchpad pattern**: isolate noisy investigation, return clean findings.

### Example: Understand Error Handling Patterns

**Scenario**: You're about to refactor error handling but need to first understand the current pattern across all handlers.

**Without Explore**:
- Ask Claude to search and report on handler files.
- Your main session fills with dozens of code snippets, grep results, and analysis.
- Later context is wasted on discovery output instead of implementation.

**With Explore subagent**:
```
"Use the Explore agent to search the codebase and summarize:
1. What error types are thrown?
2. What HTTP status codes are used?
3. Are there inconsistencies in error handling?

Return a brief summary table and discovery findings."
```
- Explore runs independently, collects findings in a scratchpad.
- Returns a clean one-page summary.
- Your main session stays focused on implementation decisions.

**Why Explore**: You isolate verbose discovery output and preserve main-session context for the actual work.

---

## Combined Workflow: Plan, Explore, Execute

A realistic task often combines all three modes:

### Example: Refactor the Cart System

**Phase 1: Plan Mode**
- Goal: Design how cart state flows through components and API.
- Explore: What files need to change? (components, state, API handlers, tests)
- Design: Should we use Context + local state, Redux, or a different pattern?
- Review: How does the current checkout flow work?

**Phase 2: Explore Subagent**
- Goal: Gather technical debt and risk factors.
- Scan existing code for prop-drilling, state management patterns, and test coverage gaps.
- Return: Clean summary of risks (e.g., "400+ lines, multiple state slices, limited test coverage").

**Phase 3: Direct Execution**
- Now that you've planned and explored, implement the refactor.
- Create new files (context, hooks, tests) and modify existing ones.
- Stay in the main session; you already have the design.

---

## Decision Tree

```
Does your task touch ≥3 files?
├─ Yes, architectural changes?
│  └─ Use PLAN MODE
│     → Explore codebase
│     → Design approach
│     → Get approval before implementing
└─ No, single function/file?
   └─ Use DIRECT EXECUTION
      → Implement immediately
      → Add tests
      → Done

Is discovery noisy / might waste context?
├─ Yes, but you still need to understand the codebase first?
│  └─ Use EXPLORE SUBAGENT
│     → Run discovery in isolation
│     → Return summary findings
│     → Then proceed with Plan or Direct mode
└─ No, keep it simple?
   └─ Plan or Direct (above)
```

---

## Knight-Webb Curriculum Reference

This decision framework is inspired by Knight & Webb's paper **"SWE Is Becoming Plan and Review"** (sourced via the Claude Code curriculum). The core insight: modern software engineering is dominated by high-context decision-making and review, not low-level coding. Matching your tool use (plan mode, direct execution, exploration) to the cognitive demands of the task prevents wasted effort.

---

## Appendix: Tool Allowlist by Mode

### Plan Mode (Read-Heavy)
- ✅ Read, Glob, Grep, WebFetch
- ✅ Bash (for `git log`, `git show`, understanding history)
- ❌ Write, Edit, or any tool that modifies files

### Direct Execution (Full Write Access)
- ✅ All tools, including Write, Edit, Bash
- ✅ Git commit/push (with safety checks)

### Explore Subagent (Isolated Discovery)
- ✅ Read, Glob, Grep, WebFetch, Bash (read-only)
- ❌ Write, Edit (output is scratchpad, not part of repo)
