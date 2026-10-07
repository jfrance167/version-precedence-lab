# Version Precedence Lab

A local SemVer 2.0.0 teaching tool distinguishes precedence equality from literal equality and explains the decisive rule. `1.0.0+one` and `1.0.0+two` compare equal but differ literally. Build metadata stays in the report and never breaks a tie.

- [Plan](PLAN.md): exact scope, bounds, threat model, examples, stages and verification.
- [Research](RESEARCH.md): primary standards, inspected candidates and build recommendation.
- [State](STATE.md): authorization, completed research and next step.
- [Tasks](tasks/todo.md): staged checklist.
- [Draft review](research/worker-review.md): rejected local and empty free-remote attempts.

## Run

No install/external runtime dependency. Python3.11+ is the intended source target; only the runtime in VERIFICATION.md was tested. From this directory:

```powershell
python -I lab.py examples/build-equality.json
python -I lab.py examples/prerelease-numeric.json --output fresh-report.json
python -I lab.py --help
```

Input is exact {profile:semver-precedence/1,synthetic:true,cases:[{id,left,right}]}; see examples for JSON. Every report keeps package existence/authenticity/compatibility/security unknown. Use invented strings only. No PEP440 conversion/ranges/resolution/registry/latest-version/real inventory. Exit0 complete/help,2 invalid/usage,3 unsupported,4 limit,5 transport/delivery. Existing/empty output path fails without stdout fallback. Partial bytes/files may remain on I/O failure.

## Architecture and bounds

admission.py gates bytes/lexical depth/numbers/exact native trees/common fields; version.py supplies strict grammar/caps/immutable parts/comparison; model.py validates ALL grammar then ALL caps before results; cli.py checks transport/diagnostics/delivery. API: semver_lab.evaluate(value), evaluate_bytes(exact_bytes), serialize(model_report). Serialize accepts trusted reports produced by the model, not arbitrary untrusted documents.

Raw65,536 bytes/depth8/nodes4,096/64 cases/version256 ASCII chars; numeric32 digits/16 identifiers/list/64 chars/identifier/output1MiB. These are lab bounds rather than universal SemVer rules. Repeated aliases count per occurrence, ancestor cycles fail, no coercion/normalization/build tie-break. See CONTRACT.md.

## Verify and learn

```powershell
python -I scripts/run_tests.py
python -I -O scripts/run_tests.py
python -I scripts/verify_mutations.py
python -I scripts/verify_project.py
```

Complete verifier requires already-installed Bandit on that interpreter; no installs/network. Fresh raw logs/scratch retained in ignored .verification-work, accepted current-byte receipts in evidence. VERIFICATION.md gives exact outcomes/limits; REVIEW.md gives ECC self-review fixes and retained harness advisories. DECISIONS.md, LEARNING.md, SECURITY.md and NOTICE.md record tradeoffs, concepts, threat model and attribution. Original code MIT, AI assistance disclosed; no repository/publication or independent external audit claimed.

Current corrected verification:25 normal/optimized tests,41 actual CLI cases per mode,3 assertion-detected mutants, zero production Bandit findings. Native API exotic types are rejected by identity before caller hooks; the coordinator's metaclass defect and preserved pre-fix evidence are disclosed in REVIEW/VERIFICATION. Serialized JSON cannot carry those Python classes.

## Publication status

See [publication review](PUBLICATION.md) for the October 5 source snapshot, fresh local checks, evidence boundaries and current hosted-check distinction.
