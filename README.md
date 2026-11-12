# Issue 318 validation — 2026-11-12

Source: /Users/zeeshan/zakura-fix-318, branch fix/318-installer-directory.
Base b6a296f56fc0ea69e894d66050d8b8c54325d04c; fix 3153e4b.

- Before fix: added regression failed because installer accepted directory target (before.log).
- macOS ARM64 and Linux ARM64 (python:3.12-slim): existing installer fixture suite passed (mac-tests.log, linux-tests.log). These are fixture tests, not live-service validation.
- Removing only the final guard makes the late-directory test fail (mutation.log).
- Actual installer rejects pre-existing directory and directory symlink without changing sentinels or leaving staging (real-conflict-*.log).
- Actual repeat installation over the existing executable passed, with runtime pulls enabled; installed executable still reports ths 0.4.1 and no staging directory remains (real-replacement.log).
- Actual GitHub v0.4.1 archive/checksum and matching runtime image pulls succeeded (real-install.log).
- Real installed launcher started isolated verify-318-nov12 on loopback. Dashboard submitted 1 Regtest ZEC from Account 1 to Account 2. Transaction 7f906114a1d9f771e1918c3866b04e5e527e5c70e6e9e7dcfe9dc72f648e5065 confirmed in active block 106. Node, lightwalletd and wallet all settled at 106. API evidence and screenshots are adjacent.
- Final balances: Account 1 3.9999 ZEC, Account 2 1 ZEC; fee 0.0001 ZEC.
- Named instance stopped and removed through launcher; no matching containers remain (cleanup.log).
- mdbook build, tools/build_site.py and tests/book_links.py passed; zero broken links.
- Shell syntax and git diff --check passed.

Scope limits: runtime smoke test used actual published v0.4.1 images, not a source rebuild. No Rust/web source changed, so their suites were not run. PR #452 also rewrites install.sh and still has the unguarded final move; reviewed its installer diff, but did not run its native runtime or test a combined merge. The final type check is not an atomic filesystem operation against an adversarial replacement immediately before mv. Evidence published separately from the fix branch for PR review.
