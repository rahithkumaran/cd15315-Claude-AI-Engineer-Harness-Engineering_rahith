---
description: Conventions for test files (co-located with source)
paths:
  - "**/*.test.tsx"
  - "**/*.test.ts"
---

# Test file rules

Loads when editing any co-located test file (`*.test.tsx` or `*.test.ts`).

## What to test

- **Component tests**: Assert on rendered output and user-visible behavior via `render()` and `screen` queries. Never inspect hook state directly.
- **Handler tests**: Call the handler function with a request object directly. Do not spin up the HTTP framework or mock the response object.
- **Repository tests**: Use a real PostgreSQL test instance (Docker Compose configures one). Mocking the database layer hides broken migrations and schema issues.

## What not to test

- **Generated code**: Prisma client, OpenAPI types, or other build artifacts.
- **External libraries**: Trust the library or wrap it if you need different behavior. Testing library internals is usually wasted effort.
- **Implementation details**: Test behavior, not hook calls, function call counts, or how components are composed.

## Test data and setup

- Prefer inline test data over factory functions for simple cases. Name variables clearly: `const validOrder = { ... }`.
- For complex scenarios with many shared fixtures, create a `testData.ts` in the same directory.
- Do not mock timestamps; always use `new Date()` or let utilities inject it. Hardcoded mocked times cause test fragility.

## Forbidden patterns

- **Snapshots**: Snapshots are rarely updated, rot quickly, and obscure actual behavior. Avoid them.
- **setTimeout in tests**: If you need to wait for async behavior, use `waitFor()` or structured async/await patterns.
- **Database mocking**: Queries must hit a real test DB. Mocks hide schema mismatches and broken migrations.
