# ECC actual-change self-review

Scope: all task-owned production modules/bootstrap, tests, fixtures, verifier/mutation scripts and contract. Applied installed ecc-code-review/pinned reference. Implementing Codex performs self-review, not an independent reviewer/native ECC runtime. Reviewed callers, validation order, immutable parts, report shape, delivery, argv/source receipts and test failure modes. Parent unrelated changes preserved; no commits/publication.

Concrete findings fixed:

1. Native keys validated during reverse child scheduling could reject a later key before an earlier invalid value, violating DFS priority. admission.py:99 now checks marked key nodes when popped; scheduling at123–126 preserves DFS order. test_native_dfs_error_order covers first:float/later nonstring key and single bad-key path.
2. Scheduling copied an unbounded native key into its path before checking text limits. admission.py:123 now bounds exact ASCII key length before path copying; the key node reports text_limit at /key-0. A 10,000-character key regression verifies fixed diagnostics. Not a hard RSS guarantee.
3. Initial lexical signed depth counter allowed mismatched closers to weaken the predecode bound. admission.py:48 now matches a bounded container stack; closer-before-open regression verifies json_invalid.

Oracle/scratch corrections in evidence/oracle-correction.md; no semantics weakened for an incorrect expectation. All affected checks rerun by scripts/verify_project.py.

Bandit production/harness scanned separately without suppressions. Seven LOW harness B404/B603 advisories retained at exact locations in evidence/harness-bandit.json. Reviewed subprocesses use sys.executable, fixed argv, shell=false, owned source copies and timeouts; no unreviewed third-party execution. Verifier rejects unexpected findings/severity.

Current VERIFICATION/receipt records exact results/hashes. No remaining known actionable finding after review. Limits: no hosted/multiple-runtime/real-package checks, hostile filesystem/hard-resource/durability proof; reduced output-cap seams only. Review does not authorize publication/merge/deployment.
