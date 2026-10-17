# PR 275: main merge and live validation, 2026-10-17

Code commit: `40c4b6d`. Upstream main: `b932d27`. The mounted check follows the fee quote await and preserves #289's submission lock and draft comparison. The diff against main is the mounted condition, six lifecycle tests and a three-line book note.

All 383 web tests passed across 33 files with one worker. Lint, formatting, production build, book links and diff checks passed. Removing the mounted check made four cancellation cases fail while both started-payment cases passed. Restoring it passed all six. The build reports the existing bundle-size warning. Rust tests were not rerun; there are no PR-specific Rust changes.

A fresh Docker image was built from the merged code, including server and frontend: `zakura-275-oct17:local`, manifest `sha256:4d8e9bbdc2169734a0bd47e81914ccd1aedad5c9f4e36847ba400cbebc9fc167`. It ran with Zakura 1.6.0 and lightwalletd 0.3.0 on a dedicated internal network, with the dashboard bound to loopback.

The loopback proxy delays or drops actual upstream responses; it does not invent API data. SSE passes through unchanged.

- Four recorded cancellation cases cover closing the quoting form and closing/reopening Account 3's form, each with delivered and dropped quote responses. The UI showed Checking fee before closure. All four final runs completed their intended response outcome. They created no send request and no new activity. Direct provider replacement remains covered by the automated tests; the browser used the user-accessible close/reopen sequence.
- A 0.03 ZEC send was admitted before closure; its real 202 response was delayed until the form closed. The payment confirmed.
- Real acceptance responses for 0.04 and 0.05 ZEC sends were dropped after closing. Both remained tracked and confirmed. Browser transport retries reused identical bodies and keys; all responses for each key referenced one activity. The live test observed automatic recovery, not a successful manual Resume click. The automated tests cover manual Resume.
- Verified all transaction confirmations and matching block hashes. Final node, lightwalletd and wallet heights were 109, with settled synchronization.

An initial 0.01 ZEC attempt stayed open beyond the quote timeout and submitted before closure could be performed. It is retained in the receipts as setup activity, not counted as a cancellation pass. The final cancellation runs are timestamped separately in `live-cancellation-cases.json`. The first batched trial did not wait between releasing responses and starting the next case; the recorded final cases were rerun with each delivery/drop verified before continuing.

The completed-payment screenshot shows the earlier lost-response notification alongside the later confirmation and confirmed Payments entry. This is actual browser output. Screenshots alone are not proof of absence; the cancellation network receipts and activity snapshot provide that check.
