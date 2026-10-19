# PR 275 CI and merge counter-review

AS_OF: 2026-10-20. Narrow technical research; repository source and actual GitHub CI logs, not a general multi-domain literature survey. No repository mutations performed by this reviewer. Parent merged while review was in progress; immutable before SHA and final local SHA are recorded below.

## Sources

1. GitHub failed Rust job, run 39052099608, job 117665972665. https://github.com/zcashlabs/thus-spoke-zakura/actions/runs/39052099608/job/117665972665 . Source-Type: official; Accessibility: public repository / authenticated log retrieval; date 2026-10-18; authority 10. Read via gh run view --log-failed.
2. Main commit 91d5710a91ca55610d37264eaed96a4e6331bc45, `test(cli): pass output mode to installer test`, dated 2026-10-17. Source-Type: official; Accessibility: public; authority 10. Read local Git object, reachable from origin/main c0edfb0585aa868504fa5e5ce330e58df59de8e1.
3. PR original head 40c4b6d0cdea8079847037f6ba365570702f96ef, updater test and signature. Source-Type: official repository source; Accessibility: public; authority 10. Read with git show at immutable SHA.
4. Updated local merge 8c93ca387cf60c993bb831910becdd01d560fb8e, SendDialog.tsx, SendDialog.test.tsx, WalletActions.tsx, and .github/workflows/ci.yml. Source-Type: official upstream source plus pending contribution; Accessibility: local checkout (pending contribution), upstream code public; authority 9. Read directly and diffed against main.

## Findings

- High confidence: Rust CI fails at Clippy compilation with E0061 in the symlink updater test, updater/tests.rs:117. It passes three arguments to the four-argument run_installer function. [1][3]
- High confidence: main already fixes this exact call by adding `false` in commit 91d5710. The boolean controls installer stdout routing for JSON mode. The symlink test uses ordinary output, consistent with the other updater test. No new production updater change is necessary. [2][3]
- High confidence: updated local merge includes that upstream fix. Its PR delta against main remains only the lifecycle guard, six parameterized regression cases, and dashboard documentation. [4]
- GitHub status at review: rust failed; activity-recovery, book, web and both Linux launcher compatibility jobs passed. These are the old run's results, NOT validation of the new merge. [1]

## Counter-review: three concrete validation risks

1. **CI failure can mask later failures.** This Rust job stopped during Clippy, before workspace tests, release-distribution tests and installer tests. A fixed call alone does not establish all these subsequent steps pass. Check the new head's full CI run and local feasible tests. [1][4]
2. **Closed form versus already-submitted payment.** The guard must only stop a new send after awaiting a fee quote. It must not clear retained payment recovery after the server has already accepted a send. Code preserves submission lock, URI revision, current-draft comparison and existing send callbacks; the six added cases cover closed/replaced × resolved/rejected quote, plus accepted/lost-response sends. Execute these and real Regtest paths again for the merged head. [4]
3. **Unmount is the relevant lifecycle boundary.** mounted.current checks unmount, not the open prop directly. Production WalletActions conditionally renders SendDialog and keys it by formVersion, so closing/replacing unmounts the old form. A future caller that merely sets open=false while preserving the component would not satisfy the same lifecycle assumption. Current production caller is correct; verify production UI close/reopen and don't misrepresent direct test harnesses as live validation. [4]

## Scope and limitations

No new defect found in the merged lifecycle guard by this targeted source review. No tests or live services were run by this reviewer; those belong to the parent validation task. No GitHub comment or push performed. No claim that ordinary unit tests satisfy the required actual node/lightwalletd/server/dashboard validation. Three review risks above are checks/assumptions, not invented bugs. Single repository domain is intentional for this specific source-level repair.
