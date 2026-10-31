# Engineering change notes

## Structured input should not depend on AI

**Before:** the React form assembled a text prompt and sent it to `/chat/`. A missing model key or an incorrect model interpretation could stop or alter a structured write.

**After:** form fields map directly to the validated `/interaction` contract. The UI reports the persisted record ID and clears notes only after success. The conversational assistant remains a separate feature.

**Evidence:** form payload tests and API CRUD tests run without an AI key.

## Missing-record updates should be predictable

**Before:** updating an unknown interaction returned a message object under an interaction response schema. That shape did not satisfy the schema and could produce a server error.

**After:** missing interactions return HTTP 404. A regression test fixes this behavior as an explicit contract.

## Reject invalid writes before changing stored data

**Before:** API writes did not explicitly check HCP existence. Blank notes and inconsistent follow-up dates could pass input validation. SQLite foreign keys were not enabled.

**After:** routes check HCP existence, schemas enforce positive IDs and valid notes/date order, and SQLite foreign keys are enabled. Tests verify rejected creates do not add rows and a rejected update preserves the original record.

## Make local setup reproducible

**Before:** application import eagerly loaded the AI client and required database configuration. The README did not provide install or run commands.

**After:** core requirements support SQLite and an isolated credential-free demo. AI imports are lazy. API tests replace agent calls when they need to test the chat contract. The Groq client uses its default certificate verification instead of disabling verification.

## What to understand before presenting this work

- Why Pydantic validation produces 422 and missing resources produce 404.
- Why the API checks a foreign key even when the database also enforces it.
- Why optional AI imports improve startup and test independence.
- Why a mocked chat test cannot prove model accuracy.
- Why a prompt saying “call once” is not an idempotency guarantee.
- Why SQLite tests do not replace PostgreSQL integration tests.
- Which changes you made or reviewed with assistance, and how you validated them.

These are project improvements, not claims about production usage or performance gains.
