# Issue 281 verification

## Live Regtest verification

The production dashboard from PR #345 was tested against actual Zakura 1.6.0, lightwalletd 0.3.0 and ths-server. The existing server image includes the independently tested payment timestamp change from PR #341; its dashboard files were replaced with this PR's production build through a read-only mount. No API responses or balances were mocked.

1. Loaded the full dashboard in a sandboxed iframe without `allow-same-origin`. This makes the browser itself deny storage. A loopback proxy forwards real API responses and SSE and supplies CORS headers for the opaque browser origin.
2. The wallet showed its actual 5 ZEC balance at height 103. Mine opened; submitting showed the session-storage error; Close dismissed it. No mining POST reached the server and height remained 103.
3. Opened the same dashboard outside the sandbox, with normal storage access, and requested two blocks through Mine.
4. Exactly one POST returned 202. Job `f8d0489e-e90d-4fb2-9b97-fa0c7b423ace` completed both blocks. Node, lightwalletd and wallet heights reached 105; wallet synchronization was ready and settled. The specific-job GET agreed with the latest-job GET.
5. GET block 105 returned hash `219613db05906a9da07561f3588eac92de2d00ef6cba35ed767855868c3b2d03`, matching status, with one confirmation.

Screenshots and receipts are in `live/`. The denied-storage check exercises actual browser restrictions; successful mining uses the real node. Failed storage-method writes and lost-response retries remain covered by the automated tests, not separate live scenarios.

## Automated tests and earlier fixture

The five added cases fail on upstream ef0cfb2 and pass with the fix. They cover a denied sessionStorage getter, failing getItem/setItem/removeItem, and preserving an existing key across a denied retry and restored storage access.

The full web suite passes with one worker: 296 tests across 27 files. The default parallel run timed out in six tests in RequestDialog, FaucetDialog, WalletPage and SendDialog. Both logs are included. Lint, format, production build and book-link checks passed. The build reported the existing bundle-size warning.

The screenshot uses the actual MineDialog and query/toast providers in the in-app browser, with a throwing sessionStorage getter and mocked GET mining status. Clicking Mine blocks showed the storage error and made zero POST calls; closing the dialog worked. It is a browser regression fixture, not a live Regtest environment or proof of successful mining. No Rust files changed and Rust checks were not rerun.
