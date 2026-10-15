# Verification for issues 316, 317 and 319

Tested source: upstream ef0cfb2 plus commits abc298e (#316), 7c1784a (#317), and 27f4bda (#319). Screenshots were captured from the combined development image running on a disposable local Regtest chain with Zakura 1.6.0 and lightwalletd 0.3.0. These are after-change screenshots, not before/after comparisons.

## URI parsing

A localhost proxy held a real server parse response while the amount, memo and recipient were edited. Releasing it preserved 0.02 ZEC, “Keep my draft”, and Account 4, with Send disabled. Clearing the URI enabled that manual payment, which confirmed. A second delayed parse preserved an edited 0.03 amount; applying again deliberately restored the URI’s 0.25 ZEC, “URI test”, Account 2. That payment confirmed too.

## Idle activity ages

live-clock.json records the same activity label changing from 29 to 40 seconds ago without timestamp or tooltip changes. The proxy delivered no SSE data events, and its request log showed no activity reads in that interval. Activity data came from the running server. The single wallet screenshot illustrates the display; it is not evidence of elapsed time by itself.

## Payment timestamps

live-payments.json records real send and faucet POSTs, initial 202 responses, GETs, replays and confirmation. Each response used the same nonempty creation timestamp and activity ID. Each key created one activity. All four test payments (two API, two browser) had positive confirmations and matching block hashes through the RPC-backed transaction endpoint; see live-chain-transactions.json.

## Checks

- #316: 297 web tests passed, including six new regressions that failed on main.
- #317: 292 web tests passed, including the new clock regression that failed on main.
- Both web branches passed lint, formatting, production build and book link checks.
- #319: strengthened admission test failed on main and passed with the fix. Rust formatting and clippy passed. Workspace tests: 458 passed, 23 ignored.
- Release-distribution tests: initial parallel run had one timeout in an unchanged CLI child-process test; full serial rerun passed 204 tests, with 4 ignored.
- Combined development image built. Browser console had no captured warnings/errors. Test containers, volumes and network were removed afterward.

This is targeted verification on one macOS/browser environment, not a cross-browser audit. AI assistance was used for implementation and testing.
