# PR #341 merge validation — 18 October 2026 (IST)

Tested merge commit `7857d935cda09aca5d6f459240bf4ad60b1ea8d3` against main `b932d270a80cf25f55398e052b075c8f135f7cfd`. The conflict was confined to two adjacent rows in the book. Kept main's `unconfirmed` status and this PR's initial-response timestamp clarification. The server and test changes merged without manual changes.

Built the actual dashboard and server in `zakura-341-oct18:local`. Started Zakura 1.6.0 and lightwalletd 0.3.0 on an internal Docker network, with only the dashboard published on loopback. No fabricated API responses, balances, transactions, or screenshots.

`live-payments.json` records a real 0.01 ZEC send and a real 0.01 ZEC account faucet. Each initial POST returned 202 and a nonempty `created_at` matching immediate GET and replay. Each key produced one activity, and both transactions confirmed. A separate 0.02 ZEC send was entered and submitted through the real dashboard. `chain-results.json` verifies all three transactions have positive confirmations and matching block hashes. Node, lightwalletd, and wallet settled at height 108. The remaining five-ZEC faucet activity is automatic startup funding.

`live-activity.png` and `live-confirmed.png` show this environment. The screenshot establishes UI and confirmation behavior; the JSON responses establish timestamp equality.

Formatting, book links, whitespace checks, runtime build, and server Clippy passed. Full workspace Clippy encountered an existing CLI test compilation error: `crates/ths-cli/tests/unit/updater/tests.rs:117` supplies three arguments to the four-argument `run_installer`. Both CLI files are unchanged from main. The workspace/release-distribution suites are not claimed as passing. Web tests were not rerun for this server/documentation PR; its production frontend was rebuilt and exercised live.

During setup, Docker filled its 24 GiB disk and Zakura could not open its state database. Pruning rebuildable build cache (preserving images, volumes, and Cargo cache mounts) freed 5.8 GB. Restarted this test's node and lightwalletd before performing the successful live validation. A first test-context archive was rejected before compilation and rebuilt with the correct archive format.

The first server test build was killed with SIGKILL while compiling the test crate. Docker reported 2.4 GiB total memory. After saving live evidence and removing only the labeled validation stack, retried with one compiler job, incremental compilation disabled, and debug output disabled for the server test package. Cleared only the rebuildable ths-server Cargo artifacts before that retry.

Final server suite: 286 passed, 0 failed, 20 ignored (253 library tests, 31 integration tests, 2 CLI-entry tests). The ignored opt-in integration scenarios were not run. Separate real Regtest validation is described above. Server Clippy passed with all targets and features.
