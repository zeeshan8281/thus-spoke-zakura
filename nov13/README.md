# Validation after merging current main

PR head cef1017 includes main e89e7a3 (merged #452).
Both directory checks remain: before any downloads and immediately before final launcher mv.

Passed: shell syntax; Docker and native installer fixture suites on macOS ARM64 and Linux ARM64; lock/staging cleanup assertions; native conflict created during doctor preparation; mutation checks proving each suite fails if the final guard is removed; book build and link checks (zero broken links); git diff --check.

Real combined installer installed and replaced published v0.4.1 with image pulls enabled. The installed launcher started isolated verify-318-nov13. Dashboard sent 1 Regtest ZEC from Account 1 to Account 2. Transaction f5d1f6753a007b40d6efc00039a5e14ed284b332eb2fdfc7cb8fdeb8db5fbc35 confirmed in active block 106. Block, transaction and activity agree; node, lightwalletd and wallet settled at 106. Screenshots and API responses are adjacent. Test instance removed through launcher.

Scope: native installer validation uses the repository fixture suite; v0.4.1 has no native runtime archive. Live runtime validation uses actual published Docker images, not a source rebuild or a native process stack. Rust/web source was not edited by this fix; upstream changes came from the merge, and full CI is run on the combined head.
