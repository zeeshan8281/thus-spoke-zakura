# PR #340 validation — 19 October 2026

Commit `360717e70d6a14540cf257271d9607ffb7a7ec4f` merges main `c0edfb0585aa868504fa5e5ce330e58df59de8e1`, including #361. The list clock now leaves the block-height and unknown-time fallbacks intact. The regression renders a timed row beside two null-timestamp rows, checks both fallbacks before and after timer ticks, stable timestamp attributes, no fetches, and cleanup. It fails when the null fallback is removed and passes with the fix.

The real dashboard and server were rebuilt from this branch. Zakura 1.6.0 and lightwalletd 0.3.0 ran on an internal Docker network; only the dashboard was published on loopback.

## Live mixed-timestamp check

After startup funding confirmed, copied the stopped wallet's actual data volume as a backup. Submitted 0.02 ZEC from Account 1 to Account 2 through the original dashboard and waited for confirmation. Stopped that app and started the restored backup against the same chain. Its wallet discovered the later transaction at block 106 with `created_at: null`; the older startup funding retained its timestamp. No database values or API responses were fabricated or edited.

Submitted another 0.01 ZEC payment through the restored dashboard, producing a fresh timed row. A loopback proxy forwarded real API responses unchanged while withholding SSE data to isolate idle rendering. The timed row advanced from 10 to 38 seconds ago; its datetime and tooltip stayed identical. The null-timestamp row stayed at `Block 106`. No activity GET occurred between observations. See `live-results.json`, `requests.jsonl`, and the before/after screenshots.

All three activity transactions (startup funding and the two sends) have positive chain confirmations and matching block hashes. Node, lightwalletd, and wallet settled at height 107. The verification script asserts these facts.

## Checks and limits

Web lint, formatting, production build, book links, and whitespace checks passed. The focused component suite passed all 8 tests. The final full web suite passed all 387 tests in 33 files, with none skipped.

The no-height `Time unknown` fallback is covered by the automated mixed-row test. The live null-timestamp transaction had a known mined height. Rust suites were not rerun: this PR changes the frontend and documentation, while the fresh image compiled the merged server and exercised it live.

## Setup issues

Docker filled its 24 GiB disk during export and later during node startup. Reclaimed rebuildable non-Cargo build cache, then rebuilt with debug symbols stripped from the runtime binary (no source or behavior change). Once space was available, generated a real Regtest block before restarting lightwalletd, which had exited before the node had a block.

An initial attempt to start a completely fresh wallet on this chain failed treasury discovery. The successful test instead restored a genuine pre-payment wallet backup as described above. Temporary labeled containers, volumes, network, browser tab, and proxy were removed/stopped after capturing evidence. Unrelated resources were retained.
