# Oracle correction chronology

Original CONTRACT and 41 complete literal reports froze before product source. Initial freeze.json case count typo 42 was corrected to actual41 before code; source fixture/hash did not change. Original accepted freeze receipt and case bytes are preserved in freeze-v1.json and cases-freeze-v1.json.

First checks exposed one expected-report mistake: ascii_invalid expected input_profile semver-precedence/1 even though its non-ASCII value fails tree preflight before common admission completes. CONTRACT specifies null until common validation succeeds. Corrected only that expectation to null, retaining every case input/status/error/row expectation, unchanged contract and original evidence. PowerShell rewrite also changed JSON formatting/encoding; structural comparison is required to corroborate the single semantic correction. No implementation was weakened to satisfy the incorrect expectation.

The same first run had 14 setup/cleanup errors because sandbox temporary directories were not writable. Test scratch now stays under the project's ignored .verification-work with fresh UUID directories retained; no recursive cleanup or approval bypass. These are not product successes. Lexical gate was tightened to reject mismatched closers immediately rather than allowing negative nesting to weaken the predecode bound.
