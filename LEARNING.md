# Learning

Precedence forms equivalence classes: different original strings may compare equal because build metadata is ignored. Literal equality is separate. Optional exercise: explain why 1.0.0+001 and 1.0.0+1 are valid equal-precedence strings, while 1.0.0-01 is invalid.

Canonical decimal strings compare numerically by length then lexical order without conversion, after validating ASCII and leading-zero rules. Text compares ASCII without case folding or locale rules.

Validation order is observable behavior. Malformed right operands and later cases must reject even when an earlier core difference would decide the comparison. All grammar precedes component caps in this profile.

A mutation counts as detected only when its intended expectation assertion fails; a crash proves nothing about the semantic oracle. Algebraic checks supplement hand examples: consistently wrong orders can still be transitive.

The initial non-ASCII expected profile was wrong; original evidence is preserved and correction follows the unchanged contract. Sandbox temporary storage was unavailable, so scratch stays in the workspace. Python shutdown may replace a chosen exit with120 after a buffered broken-pipe flush; actual pipe tests complement I/O seams.

Exact-type checking must itself avoid hooks: `type(obj) in (dict,list)` performs equality and can invoke a custom metaclass. `type(obj) is dict or type(obj) is list` uses identity. A normal subclass/items sentinel test did not expose this; the coordinator's metaclass repro did. The new regression proves rejection before equality/inequality/length behavior for root and nested native values. JSON cannot encode these native classes.
