# Version precedence lab — approved plan

Tier 3 portfolio teaching tool, local synthetic inputs only. Stages 1–4 approved by the coordinator's October 5 03:51 decision under Jake's direct delegation. Sole writer: this existing chat. Separate directory, preserve previous labs and shared parent Git. No new repository, installs, publication or spending. Delegated work cutoff: October 6, 2026 at 08:00 Eastern.

## Problem and success criteria

Demonstrate why SemVer precedence equality is different from literal equality. Given bounded invented version pairs, validate the whole input, preserve every spelling, then report less/equal/greater and the first decisive rule. Equal precedence must never imply equal identifiers, compatibility, security, latest release or authentic packages. An unsupported/malformed/over-limit input releases no comparison rows.

Success: frozen contract and independent expectations before code; correct numeric/prerelease/build rules; meaningful normal/optimized/API/actual-CLI checks; intended assertion failures for mutants; review and source/fixture receipts; usable README, license, attribution, AI disclosure, learning and vault milestone. No real package input or ecosystem resolver.

## Scope and alternatives

Enable exactly `semver-precedence/1`, a bounded SemVer 2.0.0 syntax and precedence teaching profile. PEP 440 remains an explicit documented alternative in RESEARCH.md. No coercion, trimming, normalization, optional core fields, v prefix, epochs, ranges, wildcard syntax, sorting/ranking packages, registries, downloads, inventory scanning, artifact execution or dependency resolution. Inputs are invented strings, and synthetic=true is a declaration rather than a provenance proof.

Recommendation is original stdlib Python implementation. General python-semver adoption would still need strict admission and explanation wrappers; packaging implements another standard. No external runtime dependency needed for this scope. Proposed Python 3.11+ support is a target, not evidence of multiple runtimes tested. No environment/model/provider installations.

## Proposed frozen input and bounds

Input JSON exact root fields: profile (bounded ASCII string), synthetic (exact true), cases (list). Each case has exact id, left, right fields; unique id is 1–32 ASCII alphanumeric/underscore/hyphen characters, left/right exact strings. At most 64 cases. Empty cases completes with zero rows and no package claim. No bool-as-number or arbitrary object/coercion acceptance.

Raw input at most 64 KiB, depth 8, total nodes 4,096. Duplicate JSON object keys, nonfinite values, non-JSON native types/cycles, wrong fields/types and synthetic false fail admission. Exact bytes API; exact builtin containers for native API. Common shape/types/string/count bounds over every case precede supported-profile evaluation. A bounded unknown profile is unsupported only after common admission succeeds; its opaque version strings are not subjected to SemVer grammar. Unknown/malformed profile types are invalid.

Each version is at most 256 ASCII characters. Supported grammar: exactly three nonnegative decimal core components with no leading zeroes except literal 0; optional nonempty dot-separated prerelease; optional nonempty dot-separated build. Identifiers contain ASCII letters, digits or hyphen only. Numeric prerelease identifiers prohibit leading zeroes; build identifiers permit them. Each core component and numeric prerelease has at most 32 digits. Each prerelease/build list has at most 16 identifiers and each identifier at most 64 characters. These caps are lab limits, not SemVer validity rules.

Freeze priority: raw/tree/common admission first in deterministic input order; supported grammar validation for all versions next; supported per-component/list caps next; comparisons only after all pass. A syntactically malformed later version blocks earlier rows. Grammar-invalid leading zeroes take invalid precedence over per-component caps after common bounds; total text bounds remain earlier. Contract must enumerate fixed error codes/paths, no raw diagnostic echoes. Wrong standard grammar (for example 1.0, 1!1.0.0) is invalid in this supported profile, never converted to PEP 440.

## Architecture and evidence

Thin layers: bounded bytes/native admission; immutable parsed versions retaining originals; pure pair comparator; deterministic report serialization; CLI transport. No dynamic plugins/eval/subprocess/network in production. Trusted source bootstrap mirrors prior lab pattern after source review, no packaging installation.

Avoid converting arbitrary digit strings to float or integer: after canonical-digit validation, compare digit counts then ASCII digit text. Compare major/minor/patch in order. Equal core: release exceeds prerelease; numeric prerelease compares numerically, numeric is below nonnumeric, nonnumeric compares ASCII lexically, and a longer list exceeds an equal prefix. Build metadata never breaks a tie. Parse both operands and every case before taking a decisive comparison shortcut.

Output case row retains id/index/original strings, parsed core digit strings/prerelease identifiers with numeric/text classification/build identifiers, relation less/equal/greater, literal_equal, and fixed decisive-rule evidence with relevant positions/values. Equal original strings imply equal precedence; the converse does not hold. Every row declares build metadata ignored for precedence. These are observed syntax/model relations, not release/security/compatibility judgments.

Report exact schema `semver-precedence-report/1`, input_profile, status complete/invalid/unsupported/limit, evaluation complete/incomplete, limits, assumptions, cases or null, error or null. Complete empty rows are valid. Assumptions explicitly name strict bounded SemVer and unknown package existence/authenticity/compatibility/security. No numeric safety/quality score. Freeze exact fields and deterministic error priority in CONTRACT before code.

Serialize ASCII-safe JSON plus LF and enforce 1 MiB before delivery. CLI `python -I lab.py INPUT [--output FRESH_FILE]`: exclusive output, empty output argument is a file failure, no stdout fallback. Exit 0 complete regardless of relation, 2 invalid/usage, 3 unsupported, 4 limit/incomplete, 5 transport/delivery failure. Bounded fixed stderr diagnostics, no paths/exceptions/tracebacks. Check short writes, flush and close errors. Partial bytes/file may remain on failure; no atomic durability or hostile-filesystem containment claim. An output-cap seam test must be labeled if documented bounds make the real cap unreachable.

## Threat model and limits

Untrusted fixture structure/strings may consume CPU/memory, trigger parser ambiguity or output amplification. Admit whole bounded input, reject duplicate keys/cycles, avoid recursive unbounded traversal, cap serialized output, and keep production pure. Mixing standards or build tie-breaks can produce plausible but false judgments; freeze one grammar and independent negative controls. Never echo unchecked filenames/string diagnostics to terminals.

Source bootstrap, interpreter, local filesystem and reviewed transport are trusted. Input bounds are not hard time/RSS limits; ordinary sandboxing is not malware isolation. No hostile symlink/junction race, crash durability, concurrent writer or real package provenance guarantee. No external commands, target testing, registry access or actual binaries.

## Stages and definitions of done

1. Freeze CONTRACT and at least 30 independent literal case expectations, source/spec references and oracle hashes before implementation. Include malformed-late and resource/equality boundary controls. Stage done when contract fields/priorities/limits and expected explanations are reviewable without code.
2. Implement bounded admission, parser and comparator in thin modules. Stage done when all frozen API cases pass, invalid/unsupported/limit rows stay absent, exact spellings retained and input remains unmodified. Add native-cycle/type/duplicate-key tests and boundaries.
3. Implement CLI and delivery. Stage done when every frozen case runs through actual CLI with exact exit/output expectations and fresh/existing/empty/unwritable output plus input/short/flush/close/diagnostic failure controls pass. No install or implicit output fallback.
4. Verify and document. Normal and optimized unittest, finite antisymmetry/transitivity checks, build-invariance and identity implication; compile and available installed Bandit with production/harness findings separate; at least three isolated source-copy mutants caught by intended assertions, original hashes unchanged. ECC actual-change self-review and affected rechecks. Create reproducible stdlib verifier using existing reviewed patterns, exact source/test/contract/oracle receipts, useful README/demo examples/MIT for original code/NOTICE with sources/AI disclosure/SECURITY/STATE/DECISIONS/LEARNING, and hash-verified vault milestone. Do not imply independence for self-review or claim unrun checks. No GitHub baseline workflows until repository creation is separately authorized.

## Independent hand expectations (planning examples)

These are Codex source-checked handwritten expectations; neither worker is an oracle. Freeze expanded literal cases independently before production code.

| Left | Right | Expected | Decisive rule |
|---|---|---|---|
| 1.0.0+one | 1.0.0+two | equal, literal false | build ignored |
| 1.0.0+001 | 1.0.0+1 | equal, literal false | build numeric zeroes valid, ignored |
| 1.0.0-alpha.2 | 1.0.0-alpha.10 | less | numeric prerelease |
| 1.0.0-9 | 1.0.0-alpha | less | numeric below text |
| 1.0.0-A | 1.0.0-a | less | ASCII text |
| 1.0.0-alpha | 1.0.0-alpha.1 | less | equal prefix, shorter list |
| 1.0.0-rc.1 | 1.0.0 | less | prerelease below release |
| 9.0.0 | 10.0.0 | less | numeric major |
| 1.0.0 | 1.0.1-0 | less | patch precedes prerelease |
| 1.0.0-01 | 1.0.0 | invalid | numeric prerelease leading zero |
| 01.0.0 | 1.0.0 | invalid | core leading zero |
| 1.0.0-01a | 1.0.0-1 | greater | nonnumeric above numeric |
| 1.0.0-- | 1.0.0-0 | greater | hyphen identifier is text |
| 1.0.0 | 1.0.0 | equal, literal true | all parts equal |
| 0.0.0 | 9.0.0-01 | invalid | validate right before core shortcut |

Also freeze the specification chain, invalid empty/dotted suffixes/non-ASCII/whitespace/v-prefix/PEP forms, exact and one-past caps, malformed behind unknown profile, empty cases/duplicate ids, builds appended without relation change, and native/API limits. Mutants: compare build metadata, lexically compare numeric prerelease, reverse release/prerelease. Require the intended oracle assertion, not a mutant crash/import failure.

## Pending review

Stages 1–4 approved. Addendum: freeze full independent cases/status/error precedence before code; deterministic all-cases grammar-before-component-cap ordering; common-only validation on unknown profile; explicit tree/node/alias and predecode depth/numeric bounds; actual normal/optimized CLI checks for empty/fresh/existing/help/dirty/short/flush/both-failed sinks; label unreachable cap seams. Original assignment, approval and active authority remain in .private/coordination/2026-10-05/SUCCESSORS.md; this record does not broaden them.
