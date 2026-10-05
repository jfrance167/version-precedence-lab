# Version precedence research

Research date: October 5, 2026. Research only; implementation awaits concrete plan approval. Sources were read through the connected GitHub integration. Web page retrieval failed, so official repository sources supplied the standards. Source URLs and inspected file blob hashes are in research/source-records.json. No downloaded candidate was installed or executed; no candidate tests, hosted CI, Scorecard or security audit were run.

## Reuse and gap

Read relevant inventory CONTRACT and signed-update README. Inventory deliberately compares opaque version labels without parsing. Signed update metadata version/freshness supports rollback protection; it does not establish package version precedence. Preserve both projects. Their bounded admission, exclusive output, controlled errors and independent oracle/mutation verification patterns are useful to adapt after authorization, with current source inspection rather than blind copying.

Read vault Home.md and Codex Integration.md. Focused Markdown searches for SemVer, semantic version, PEP 440, version precedence and prerelease in research/project notes returned no matching standalone model. This is scoped retrieval, not an exhaustive duplicate audit. No existing verified standalone comparator was found in the relevant local records inspected.

## Standards and semantic distinction

[Semantic Versioning 2.0.0](https://github.com/semver/semver/blob/f99d5485190a47c0863949e7da810a5553e0ed4d/semver.md), sections 9–11 and grammar, requires three core numeric components, excludes leading zeroes there and in numeric prerelease identifiers, compares core numerically and prerelease identifiers by numeric/ASCII rules, and ignores build metadata in precedence. The specification was authored by Tom Preston-Werner and is CC BY 3.0; this plan paraphrases and attributes it rather than copying its implementation or full text. Equal precedence can coexist with different literal strings: 1.0.0+one and 1.0.0+two. A string cannot prove API compatibility or the existence of a release.

[PyPA version specifiers](https://packaging.python.org/en/latest/specifications/version-specifiers/) were inspected via the [official source](https://github.com/pypa/packaging.python.org/blob/main/source/specifications/version-specifiers.rst). PEP 440 has epochs, normalized releases, pre/post/dev forms and local labels. Its local labels participate in comparison, and trailing release zeroes may compare equal. These rules cannot be silently applied to SemVer build metadata or identifiers. Select strict bounded SemVer only; PEP 440 is a documented alternative, not another enabled profile.

## Candidates inspected

### python-semver

Repository [python-semver/python-semver](https://github.com/python-semver/python-semver), inspected commit 1d515915d50b31f23fd1fb0f572ef608453e80e3. Read src/semver/version.py, tests/test_compare.py, pyproject.toml, LICENSE.txt and python-testing.yml. Parsing uses an ASCII grammar; comparison ignores build metadata and contains explicit numeric-versus-text rules. The broad compare API accepts several types, and constructor behavior is broader than strict string parsing. The lab would require a separate admission contract even if adopted.

The manifest has no mandatory runtime dependencies and offers an optional native parser backend. Development tooling is separate. Actual LICENSE.txt contains three BSD conditions including nonendorsement; the manifest's BSD-2-Clause comment differs. Actual license text must control attribution if any code is later adopted. No code is copied here.

Tests include canonical ordering and long numeric prereleases. [PR 488](https://github.com/python-semver/python-semver/pull/488), merged October 1, describes the integer-conversion-limit failure and length/text comparison fix. Its reported checks are upstream author evidence, not our verification. Latest release endpoint returned [3.1.0](https://github.com/python-semver/python-semver/releases/tag/3.1.0), September 12: the inspected October commit is later, so do not claim that published artifact includes this fix. CI defines tox testing; the inspected workflow has a moving checkout version alongside pinned setup-uv. Do not copy its actions into owned repositories. Maintenance evidence is useful, not proof of safety.

### PyPA packaging

Repository [pypa/packaging](https://github.com/pypa/packaging), inspected commit 4a920d632a0e81ef2b06dc94d9048eee9e569c8d. Read src/packaging/version.py, tests/test_version.py, pyproject.toml, LICENSE, LICENSE.BSD and test.yml. Its normalization and comparison keys explicitly implement PEP 440, including release-zero normalization and local-label ordering. Substantial version tests and multi-platform/runtime CI are present; inspected actions are pinned. Manifest declares no runtime dependencies, flit_core build tooling and separate test dependencies. License is Apache-2.0 OR BSD-2-Clause; actual BSD text inspected, Apache alternative not fully inspected because no adoption is proposed.

Latest default-branch commit evidence is October 2; latest release endpoint returned [26.3](https://github.com/pypa/packaging/releases/tag/26.3), August 4. [PR 608](https://github.com/pypa/packaging/pull/608), inspected as an example of artifact-consumption testing, discusses wheel/sdist smoke coverage; this is not a version correctness or security assessment. Appropriate to adopt for a Python packaging feature, but importing it here would introduce the wrong standard and broader normalization.

## Recommendation and tradeoffs

Build a small original standard-library teaching implementation of the bounded SemVer syntax/precedence subset. Adopt the specification's semantics and independently written expectations, not candidate source or tests. Python-semver is the closest maintained reusable option for general SemVer work, but the lab's goal is explaining strict admission, first decisive comparison evidence and literal identity. A fork would add maintenance without solving those teaching requirements. Packaging is appropriate only if a separate PEP 440 project is approved.

Fewer dependencies alone do not prove security. Original code increases parser/comparator review responsibility, addressed by small hard bounds, full-input validation, hand oracles, algebraic checks, mutation controls and ECC review. No claim of exhaustive candidate discovery, complete SemVer package/API conformance or confirmed safety. Worker failures and actual route evidence are in research/worker-review.md.
