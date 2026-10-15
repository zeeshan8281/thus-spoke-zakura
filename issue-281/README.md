# Issue 281 verification

The five added cases fail on upstream ef0cfb2 and pass with the fix. They cover a denied sessionStorage getter, failing getItem/setItem/removeItem, and preserving an existing key across a denied retry and restored storage access.

The full web suite passes with one worker: 296 tests across 27 files. The default parallel run timed out in six tests in RequestDialog, FaucetDialog, WalletPage and SendDialog. Both logs are included. Lint, format, production build and book-link checks passed. The build reported the existing bundle-size warning.

The screenshot uses the actual MineDialog and query/toast providers in the in-app browser, with a throwing sessionStorage getter and mocked GET mining status. Clicking Mine blocks showed the storage error and made zero POST calls; closing the dialog worked. It is a browser regression fixture, not a live Regtest environment or proof of successful mining. No Rust files changed and Rust checks were not rerun.
