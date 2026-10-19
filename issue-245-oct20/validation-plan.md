# PR275 update validation
AS_OF: 2026-10-20. Lightweight technical investigation, scoped to the requested fix rather than a general research report. Sources: public upstream code, maintainer comment, actual CI logs, and locally generated test evidence. Domain quotas are not meaningful for this repository-specific diagnosis.

1. Trace CI failure and main fix (independent review: research-review.md).
2. Merge main, confirm intended three-file PR delta, run Rust and web checks.
3. Rebuild actual app, test closing/reopening while a real quote response is held, prove no send request or activity created; then confirm a normal payment and its transaction against the real Regtest chain. Capture screenshots.
4. Counter-review: old green web checks are stale after merge; compilation success does not prove later Rust tests; cancellation before send must not break tracking after send. Revalidate those boundaries.
5. Publish evidence and branch, inspect new CI, then post a factually limited review request tagging megabyte0x.

No fabricated response data or fixture screenshots count as live validation. Existing unit tests may use test seams, reported separately. No additional product changes are planned.
