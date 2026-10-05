# ECC actual-change self-review

Scope: all task-owned production modules/bootstrap, tests, fixtures, verifier/mutation scripts and contract. Applied installed ecc-code-review/pinned reference. Implementing Codex performs self-review, not an independent reviewer/native ECC runtime. Reviewed callers, validation order, immutable parts, report shape, delivery, argv/source receipts and test failure modes. Parent unrelated changes preserved; no commits/publication.

Concrete findings fixed:

1. Native keys validated during reverse child scheduling could reject a later key before an earlier invalid value, violating DFS priority. admission.py:99 now checks marked key nodes when popped; scheduling at123–126 preserves DFS order. test_native_dfs_error_order covers first:float/later nonstring key and single bad-key path.
2. Scheduling copied an unbounded native key into its path before checking text limits. admission.py:123 now bounds exact ASCII key length before path copying; the key node reports text_limit at /key-0. A 10,000-character key regression verifies fixed diagnostics. Not a hard RSS guarantee.
3. Initial lexical signed depth counter allowed mismatched closers to weaken the predecode bound. admission.py:48 now matches a bounded container stack; closer-before-open regression verifies json_invalid.

Oracle/scratch corrections in evidence/oracle-correction.md; no semantics weakened for an incorrect expectation. All affected checks rerun by scripts/verify_project.py.

Bandit production/harness scanned separately without suppressions. Seven LOW harness B404/B603 advisories retained at exact locations in evidence/harness-bandit.json. Reviewed subprocesses use sys.executable, fixed argv, shell=false, owned source copies and timeouts; no unreviewed third-party execution. Verifier rejects unexpected findings/severity.

## Coordinator native hook finding and correction

Coordinator's04:31 benign repro found actual admission.py:110/127 type-membership expressions call untrusted metaclass equality. Self-review had missed this; prior no-hook completion claim was too broad. False equality records4 calls, equality claim enters len behavior, raising equality escapes rejection. Scope is native API, not serialized JSON classes.

Fixed both with identity-only expressions, inspected surrounding preflight/key/common/decode/CLI type checks for the same mechanism. Added test_native_metaclass_hooks_never_called with false/true/raising equality modes, hostile inequality/length sentinels, direct/root/nested/case-operand controls. All require zero hooks and controlled rejection. Preserved actual pre-fix bytes, receipt and failing regression logs in evidence/pre-native-hook-fix; frozen contract/oracles unchanged. See evidence/native-hook-correction.md and refreshed verification for results.

Current VERIFICATION/receipt records exact results/hashes. Limits: no hosted/multiple-runtime/real-package checks, hostile filesystem/hard-resource/durability proof; reduced output-cap seams only. Review does not authorize publication/merge/deployment.

Correction verification:25 normal/optimized/restored tests pass, all3 assertion mutants caught, production SAST0 findings/errors,7 LOW harness advisories unchanged. No remaining known actionable finding from this surrounding-path self-review; coordinator acceptance remains separate. Old source/evidence retained, original/current contract/oracle hashes unchanged. Serialized CLI cannot carry this class/metaclass defect; native rejection controls now exercise it directly.
