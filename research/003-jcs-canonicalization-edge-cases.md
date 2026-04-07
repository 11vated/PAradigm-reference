# 003 — JCS canonicalization edge cases

## Question
What edge cases in RFC 8785 (JSON Canonicalization Scheme) does the GSPL seed serializer need to handle correctly so that two implementations of the spec on different platforms produce identical canonical bytes for identical seeds?

## Why it matters (blast radius)
The seed canonical form is the input to the content hash and to the RFC 6979 ECDSA signature. Any divergence between two JCS implementations breaks both. JCS is the bridge between "human-authored seed JSON" and "bit-stable hash input"; if the bridge wobbles, the entire proof system loses cross-platform reproducibility. This brief gates `formats/seed.md`, `proof/canonicalization.md`, and `proof/signature.md`.

## What we know from the spec
- `formats/seed.md` mandates RFC 8785 JCS for seed canonicalization.
- `proof/canonicalization.md` cites JCS as the only allowed canonicalizer.
- The seed schema includes string fields (with potential Unicode), numeric fields (currently constrained to integers in the spec, but the schema does not yet enforce this), and nested objects.

## Findings

1. **NaN, Infinity, and -Infinity MUST cause the canonicalizer to terminate with an error.** RFC 8785 §3.2.2.2 [1] is explicit: these are not valid JSON numbers and the canonicalizer must refuse to emit them. Any implementation that silently passes them through is non-conformant.

2. **Unicode normalization MUST NOT be applied to string values.** RFC 8785 §3.2.3 [1] mandates that string values are preserved "as is" — no NFC/NFD/NFKC/NFKD transformation. The escape rules specified by RFC 8259 are applied (control characters, `"`, `\`), and the rest of the Unicode codepoints are emitted as raw UTF-8 bytes.

3. **Property name sorting is by UTF-16 code units interpreted as unsigned integers, lexicographically, locale-independent.** RFC 8785 §3.2.3 [1]. **This is not the same as UTF-8 byte sorting.** The two coincide for ASCII but diverge above U+007F. For example, the BMP character U+FF21 ("FULLWIDTH LATIN CAPITAL LETTER A") is one UTF-16 code unit (0xFF21) but three UTF-8 bytes (0xEF 0xBC 0xA1). UTF-16 sort puts it before any non-BMP character; UTF-8 byte sort places it differently. **Implementations that sort by UTF-8 bytes are non-conformant.**

4. **Surrogate pairs sort by their UTF-16 representation, not by codepoint.** Non-BMP characters (U+10000 and above) are encoded as a high surrogate (0xD800–0xDBFF) followed by a low surrogate (0xDC00–0xDFFF). When sorting, the high surrogate compares as a single 16-bit unsigned integer in the 0xD800–0xDBFF range, which is *higher* than any BMP character below 0xD800 but *lower* than BMP characters above 0xDFFF. This ordering is well-defined but counter-intuitive for naive implementations.

5. **Number serialization uses ECMAScript `Number.prototype.toString` semantics.** RFC 8785 §3.2.2 [1]. For integers in the safe-integer range (±2^53−1), this is straightforward. For non-integer doubles, the algorithm requires producing the *shortest* decimal string that round-trips back to the same IEEE-754 double, with specific rules for exponent notation (used iff the magnitude is ≥1e21 or <1e−6). This is the well-known "Grisu" / "Ryū" / "Dragon4" problem.

6. **Object property name uniqueness MUST be enforced before sorting.** RFC 8785 implicitly assumes input JSON has unique property names per object (this is a SHOULD in RFC 8259 but not a MUST). JCS implementations must reject inputs with duplicate keys to avoid ambiguous output.

7. **Whitespace, comments, and trailing commas are stripped/forbidden.** Standard JSON only — no JSON5, no JSONC.

8. **Empty objects and empty arrays canonicalize to `{}` and `[]` exactly.**

## Risks identified

- **The UTF-16 vs UTF-8 sort distinction is the single most common JCS conformance bug.** Any non-trivial JCS test suite must include property names with non-BMP characters (e.g., emoji, CJK extensions).
- **Allowing floats in seeds at all** opens the door to the Number.toString round-trip subtleties. Brief recommends restricting seed numbers to integers.
- **A mismatched Rust JCS crate** could ship with UTF-8 byte sorting and pass all-ASCII tests in CI while silently failing on real-world inputs.
- **Duplicate-key handling differs across naive serde wrappers.** Some accept the last value silently; the canonicalizer must reject.
- **String escapes** (especially U+007F DEL, U+2028 LINE SEPARATOR, U+2029 PARAGRAPH SEPARATOR) have implementation-defined handling in some JSON libraries; JCS pins this to RFC 8259.

## Recommendation

**Adopt these v1 rules:**

1. **Use a JCS crate that has explicit RFC 8785 conformance tests.** As of this brief, the Rust ecosystem options are limited; the recommendation is to either (a) use an existing crate after auditing it against the JCS test vectors below or (b) write a thin canonicalizer over `serde_json::Value` that the spec controls. Given the small surface area (a few hundred lines), option (b) is preferred for total control.
2. **Restrict seed numeric fields to integers in the safe-integer range.** This eliminates the Number.toString round-trip class of bugs entirely. If a future seed feature genuinely needs a float, gate it behind a fixed-point representation or a string-encoded decimal.
3. **Ship a JCS conformance test suite with at least these vectors:**
   - All-ASCII property names (sanity)
   - Property names containing BMP non-ASCII (e.g., `é`, `中`, `Ω`)
   - Property names containing non-BMP characters via surrogate pairs (e.g., emoji `😀` U+1F600, CJK Extension B `𠀀` U+20000)
   - Property names that differ only by case
   - Empty object, empty array, deeply nested
   - Strings containing control characters (U+0000 through U+001F), U+007F, U+2028, U+2029
   - Strings containing escape sequences (`\\`, `\"`, `\/`, `\b`, `\f`, `\n`, `\r`, `\t`, `\uXXXX`)
   - Strings containing unpaired surrogates → MUST error
   - Numbers: 0, -0, integer max/min, integers requiring scientific notation if floats were allowed
   - Inputs containing duplicate property names → MUST error
   - Inputs containing NaN or Infinity → MUST error (these can only arise if input parser allows non-standard JSON; reject at parse time)
4. **Pin the JCS implementation version** in `infrastructure/library-canon.md`. Bumping requires re-running the conformance suite.
5. **The canonicalizer is fed `serde_json::Value` (or equivalent), not raw bytes.** Parsing and canonicalization are separated; parse errors and canonicalization errors are distinct.

## Confidence
**4/5.** RFC 8785 is short, precise, and well-tested in production by other systems (notably some signed-credential ecosystems). The risks are all implementation risks, not specification risks. Confidence would be 5/5 once we have a passing conformance suite against a chosen implementation.

## Spec impact

- `formats/seed.md` — add a "Numeric fields are integers in the safe-integer range" constraint, with rationale referencing this brief.
- `proof/canonicalization.md` — add the conformance vector list as the normative test set; require any implementation to pass it.
- `proof/canonicalization.md` — add an explicit subsection on the UTF-16 sort rule with a worked example.
- `infrastructure/library-canon.md` — pin the chosen JCS implementation (or note "in-tree implementation, see `proof/canonicalization.md`").
- New ADR: `adr/00NN-jcs-implementation.md` — capture the build vs buy decision.

## Open follow-ups

- Audit the Rust JCS crate ecosystem (search crates.io for `jcs`, `rfc8785`, `json-canonicalization`) and either pick one or commit to an in-tree implementation. Phase 1 task.
- Decide whether the seed schema should be tightened to forbid floats at the schema layer (preferred) or whether the canonicalizer is the only enforcement point (riskier).
- Build the conformance suite as a separate test crate or test directory; cross-validate against any other independent JCS implementation we can find.

## Sources

1. RFC 8785: JSON Canonicalization Scheme (JCS). https://www.rfc-editor.org/rfc/rfc8785
2. RFC 8259: The JavaScript Object Notation (JSON) Data Interchange Format. https://www.rfc-editor.org/rfc/rfc8259
3. ECMA-262 (ECMAScript Language Specification), Number.prototype.toString. https://tc39.es/ecma262/
