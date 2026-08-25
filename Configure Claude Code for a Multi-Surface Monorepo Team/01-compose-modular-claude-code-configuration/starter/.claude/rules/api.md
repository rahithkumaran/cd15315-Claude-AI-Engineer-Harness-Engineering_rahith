---
description: Conventions for API handler files
paths:
  - "src/api/**/*"
---

# API handler rules

Loads when editing any file under `src/api/`.

## Handler structure

- Every handler is an `async` function that receives a request object and returns `{ status: number, body: unknown }`.
- The framework adapter is responsible for writing the HTTP response — handlers never call `res.write()`, `res.json()`, etc.
- This isolation makes handlers testable in pure JavaScript without HTTP fixtures or mock response objects.

## Error handling

- Throw `ApiError(status, code, message)` for expected failures (validation, not-found, auth).
- Never throw a raw `Error` from handler code — it obscures the actual error and forces middleware to guess the status code.
- If you need to add context to an existing error, catch and re-throw as `ApiError` with the context in the message.

## Schema and validation

- Request validation happens at the boundary using Zod schemas from `src/api/_schemas/`.
- If you find yourself re-validating downstream in a repository or service, that's a sign the schema should be stricter or the function should not accept raw input.

## Repository imports

- Handler code imports repository functions from `src/db/`, not SQL or the connection pool directly.
- Each table has a single repository module; use that interface rather than writing custom queries in the handler.
- Multi-statement writes use `withTransaction()` — never compose writes across separate `await pool.query` calls.
