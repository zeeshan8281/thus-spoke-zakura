# PR #275: main merge and validation, 20 October 2026

Validated commit `8c93ca387cf60c993bb831910becdd01d560fb8e`, merging upstream `c0edfb0585aa868504fa5e5ce330e58df59de8e1`. Upstream commit `91d5710` supplies the missing `false` argument in the updater symlink test. No additional production patch was needed. The PR still changes only SendDialog, its tests and the dashboard documentation.

## Dashboard against real services

Fresh image `zakura-275-oct20:local`, Zakura 1.6.0, lightwalletd 0.3.0, real server and browser. Isolated Docker network; dashboard and response-control proxy bound to loopback. Proxy forwards actual responses and SSE; it only delays or drops selected responses. No fabricated API payloads or fixture screenshots.

Four cancellation cases: close and close/reopen while awaiting a fee quote, each with the real quote response released or dropped. No additional send POST or payment activity resulted. Initial attempt used a cached quote and completed a 0.01 ZEC payment before closure; this is recorded as a warmup, not a cancellation pass. Subsequent cases reloaded the page with quote responses held before opening the form.

Two accepted-payment cases: 0.03 ZEC with acceptance response held until after closure, and 0.04 ZEC with acceptance response dropped after closure. Both stayed tracked and confirmed. The dropped response caused three same-key POST attempts; the server returned the same payment ID for all three attempts, the proxy dropped each response, and only one transaction was produced. Five total send POSTs, three distinct keys including warmup.

Final node/lightwalletd/wallet height 108, settled. Three sends at heights 106/107/108, all positive transaction confirmations and block hashes matching activity. Final Account 1 balance 4.9197 ZEC; Account 2 0.08 ZEC. Raw results and assertions: `live-results.json`, `verify-live.py`, `requests.jsonl`, `cancelled-activity.json`.

Screenshots: `cancelled-live.png`, `confirmed-live.png`. The expected lost-response error toast was dismissed before the final screenshot; the activity and Payments badge confirmed the payment. Manual Resume was not exercised live because automatic recovery confirmed it; existing automated tests cover Resume.

## Automated checks

392 web tests passed (33 files); lint, format check, production web build, book links and whitespace checks passed. Rust fmt and workspace Clippy passed. Workspace tests: 626 passed, zero failed, 26 ignored. Release-distribution tests: 315 passed, zero failed, 4 ignored. Installer tests passed. Ignored tests were not run locally; actual dashboard/Regtest validation is described separately above. Rust results are recorded in rust-checks.log. Tests use the repository's existing test seams; they are reported separately from real service validation above.

## Cleanup

Removed only this run's labeled containers, volumes and network, and stopped its proxy. Retained image and evidence. Removed three older validation images and reclaimable build layers to recover disk space; unrelated resources were preserved.
