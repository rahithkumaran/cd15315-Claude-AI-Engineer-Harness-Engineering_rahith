---
description: Codified PR review checklist for the e-commerce monorepo
argument-hint: PR ref or URL
allowed-tools:
  - Read
  - Glob
  - Grep
---

# /review — Codified PR Review Process

When invoked with a PR reference (e.g., `/review 123`), this command runs the team's standardized code review checklist against the changed files. The review is **read-only** — it reports findings without modifying code.

## Must-Report vs Skip Criteria

### Must Report

- **Schema/DB migration mismatches**: Response schema in `src/api/_schemas/responses/` does not match the handler's actual response shape.
- **Missing tests**: New handler functions without a corresponding `*.test.ts` or new components without `*.test.tsx`.
- **Dangling imports**: Import paths use `../../../` relative navigation instead of the `@/` alias or module pattern.
- **Raw Error throws**: Handler code throws `new Error(...)` instead of `ApiError(status, code, message)`.
- **DB mocking in tests**: Test files mock the PostgreSQL layer instead of using the real test instance.
- **dangerouslySetInnerHTML usage**: Any occurrence outside a documented security boundary.
- **Unvetted third-party**: New `package.json` dependencies without a rationale comment.

### Skip / Non-blocking

- Formatting and linting: Assume CI catches these; focus on behavior.
- Comment quality: Trust the team's code-reading culture; flag only if meaning is truly obscured.
- Small refactoring opportunities: Note them for post-merge, don't block.

## Input/Output Examples

### Example 1: Catching a schema/response mismatch

**Input:**
```
/review gh:org/repo/pull/42
```

**Output:**
```
## PR #42 Review Summary

### 🔴 Schema Mismatch Detected

**File**: `src/api/orders/handler.ts`
**Issue**: Handler returns `{ order: { id, items, total }, timestamp }` but `src/api/_schemas/responses/OrderResponse.ts` omits the `timestamp` field.

**Finding**: Response shape must match schema in the same commit. Either add `timestamp` to the schema or remove it from the handler.

### ✅ All other checks pass
- Tests present for modified handlers
- No dangling imports
- All errors use ApiError
```

### Example 2: Flagging missing tests

**Input:**
```
/review feature/auth-refresh
```

**Output:**
```
## PR Review Summary

### ⚠️ Missing test coverage

**File**: `src/api/auth/refresh.ts` (new handler, added this PR)
**Issue**: No corresponding `src/api/auth/refresh.test.ts` found.

**Finding**: All new handlers require a test. Add a test file calling the handler with valid and invalid inputs.

### ✅ Schema and imports verified
```

## Interview Pattern

The review runs a multi-step interview internally:

1. **What changed?** Parse PR diff to identify modified/added files.
2. **Is it a handler, component, test, or migration?** Route to the appropriate check.
3. **Run path-scoped checks**: Apply rules from `.claude/rules/react.md`, `.claude/rules/api.md`, or `.claude/rules/tests.md` based on file type.
4. **Report findings in order of severity**: Schema mismatches first (critical), then missing tests, then style/pattern issues.

## Interacting vs Independent Issues

When multiple issues are found:

- **Interacting issues** (bundle into one fix): Schema mismatch + handler return statement are linked; fixing one requires fixing the other.
- **Independent issues** (list sequentially): Missing tests in one file and a dangling import in another can be fixed in separate commits.

In the output, group interacting issues under a single heading and list independent findings as separate sections.
