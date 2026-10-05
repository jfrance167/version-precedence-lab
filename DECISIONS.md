# Decisions

- Implement one strict bounded SemVer syntax/precedence profile, keeping PEP 440 a research alternative. A string cannot demonstrate package compatibility or security. Original stdlib code explains admitted strings without broad library coercions.
- Preserve originals and report literal equality independently. Build metadata never breaks a precedence tie. Canonical numeric identifiers compare by digit length/text, avoiding floats and arbitrary integer-conversion limits.
- Whole common admission, then ALL grammar, then ALL caps, then comparison. Unknown profiles receive common-only admission. No partial earlier rows when later input is malformed.
- Native traversal counts occurrences, aliases and dictionary keys; only ancestor cycles fail. Exact types and bounded key-path construction prevent hooks and diagnostic amplification.
- Exclusive output with checked write/flush/close; silence failed descriptors before interpreter shutdown so exit5 survives broken sinks. Partial files possible; no atomic durability or hostile-filesystem guarantee.
- Preserve pre-core freeze bytes and the disclosed expected-profile correction. Neither worker output is an oracle. Parent Git and previous labs preserved; no repository creation or publication.
