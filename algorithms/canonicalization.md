# JSON Canonicalization (JCS, RFC 8785)

## What it does

Canonicalization produces a unique, byte-stable serialization of any JSON value. Two JSON values that are semantically equal (same keys, same values, regardless of formatting or key order) produce identical canonical bytes. This is what lets us hash a seed and get the same hash on every machine, in every language, forever.

Paradigm uses **JCS** (JSON Canonicalization Scheme) as defined in RFC 8785. JCS was designed exactly for this use case (cryptographic signing of JSON) and is supported by libraries in every major language.

## The Rules

JCS canonicalization performs the following transformations:

1. **Object keys are sorted** in lexicographic order by their UTF-16 code units (not bytes; not collation; not locale-aware).
2. **Whitespace is stripped.** No spaces, tabs, or newlines anywhere.
3. **Numbers are normalized** to a canonical form:
   - Integers in `[-2^53 + 1, 2^53 - 1]` are written without exponent and without trailing decimals.
   - Other numbers use ECMA-262 7.1.12.1 (JavaScript `ToString(Number)`) which produces the shortest round-trip-correct decimal.
   - No leading zeros, no plus sign, no `+0`, `-0` is written as `0`.
4. **Strings are escaped** per RFC 8259 with the minimum-escape rule:
   - `"`, `\`, control chars (U+0000..U+001F) are escaped.
   - All other code points are emitted literally as UTF-8.
   - `\u` escapes use lowercase hex.
5. **Booleans and null** are written as `true`, `false`, `null`.
6. **Arrays preserve their original order** (arrays are ordered).

## Pseudocode

```
fn canonicalize(value: JsonValue) -> string:
    let mut buf = ""
    write_value(value, &mut buf)
    return buf

fn write_value(value: JsonValue, buf: &mut string):
    match value:
        JsonNull        -> buf.append("null")
        JsonBool(b)     -> buf.append(if b { "true" } else { "false" })
        JsonNumber(n)   -> write_number(n, buf)
        JsonString(s)   -> write_string(s, buf)
        JsonArray(arr)  -> write_array(arr, buf)
        JsonObject(obj) -> write_object(obj, buf)

fn write_number(n: f64, buf: &mut string):
    if n == 0.0:
        buf.append("0")
        return
    if n.is_integer() and n.abs() < 2.0.pow(53):
        // Integer fast path
        buf.append((n as i64).to_string())
        return
    // ECMA-262 ToString(Number) — shortest round-trip
    buf.append(ecma_to_string(n))

fn write_string(s: string, buf: &mut string):
    buf.push('"')
    for c in s.chars():
        match c:
            '"'   -> buf.append("\\\"")
            '\\'  -> buf.append("\\\\")
            '\b'  -> buf.append("\\b")
            '\f'  -> buf.append("\\f")
            '\n'  -> buf.append("\\n")
            '\r'  -> buf.append("\\r")
            '\t'  -> buf.append("\\t")
            c if c.is_control() -> {
                buf.append("\\u")
                buf.append(format("{:04x}", c as int))   // lowercase hex
            }
            c -> buf.push(c)
    buf.push('"')

fn write_array(arr: [JsonValue], buf: &mut string):
    buf.push('[')
    for (i, v) in arr.enumerate():
        if i > 0: buf.push(',')
        write_value(v, buf)
    buf.push(']')

fn write_object(obj: Map<string, JsonValue>, buf: &mut string):
    let keys = obj.keys().sorted_by(|a, b| compare_utf16_code_units(a, b))
    buf.push('{')
    for (i, k) in keys.enumerate():
        if i > 0: buf.push(',')
        write_string(k, buf)
        buf.push(':')
        write_value(obj.get(k).unwrap(), buf)
    buf.push('}')
```

## UTF-16 sort, not byte sort

A common pitfall: JCS specifies sort by **UTF-16 code units**, which is what JavaScript's `String.prototype.localeCompare(undefined, { sensitivity: 'variant' })` *almost* gives you (but not quite — use a dedicated UTF-16 comparator).

For ASCII-only keys, byte sort and UTF-16 sort are identical. For keys containing surrogate pairs (e.g., emoji or supplementary plane characters), the order can differ. Use a tested UTF-16 comparator from your JCS library; do not roll your own unless you have a comprehensive test suite.

## Number edge cases

ECMA-262 `ToString(Number)` is precisely defined and corresponds to the shortest round-trip decimal. The most common bug is using `printf("%g", x)` or `String.format("%f", x)` instead — these are *not* canonical and will produce divergent outputs across language standard libraries.

Recommended libraries:

- JavaScript / TypeScript: `Number.prototype.toString()` (already correct).
- Rust: the `ryu` crate, then strip trailing zeros.
- Python: `repr(float(x))` is *almost* right but has historical edge cases — use the `jcs` package.
- Go: `strconv.AppendFloat(b, x, 'g', -1, 64)` then post-process.

## Reference test vectors

```
// Input
{
  "b": 1,
  "a": 2,
  "c": [1, 2, 3]
}

// Canonical output
{"a":2,"b":1,"c":[1,2,3]}

// Input
{
  "name": "héllo",
  "value": 1.5e10
}

// Canonical output
{"name":"héllo","value":15000000000}

// Input (pre-sorted with whitespace)
[
  { "z": 1, "a": 2 },
  { "y": 1, "b": 2 }
]

// Canonical output
[{"a":2,"z":1},{"b":2,"y":1}]
```

The official RFC 8785 test vectors are at https://www.rfc-editor.org/rfc/rfc8785 and any conformant implementation must reproduce them.

## Why JCS specifically

We considered three alternatives:

1. **Custom canonicalization.** Tempting, but every project that's tried this has subtle bugs. Use a standard.
2. **Protobuf canonical form.** Strong, but requires schema; we want schema-flexible JSON.
3. **JCS (RFC 8785).** Standardized, well-tested libraries, designed for crypto. Winner.

JCS is the same canonicalization used by C2PA, COSE_Sign1, and several decentralized identity (DID) specs — it's the de facto standard for "canonical JSON for crypto."

## Where it's used in Paradigm

- **Seed hashing.** `seed.$hash = sha256(canonicalize(seed_minus_hash_field))`.
- **Seed signing.** Sign the canonical bytes, not the JSON string.
- **Seed verification.** Re-canonicalize and re-hash on receipt; reject if different.
- **`.gseed` payload hash.** SHA-256 of the canonicalized payload before MessagePack encoding (for the inner content hash) — though the outer payload hash in the file header is over the MessagePack bytes themselves.

## References

- RFC 8785: JSON Canonicalization Scheme (JCS)
- ECMA-262 §7.1.12.1: ToString applied to the Number type
