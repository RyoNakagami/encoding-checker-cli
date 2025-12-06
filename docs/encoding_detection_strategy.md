# Encoding Detection Strategy

This document describes the encoding detection strategy used in **encoding-checker-cli**, with a focus on reliable handling of Japanese text, UTF-8 with emoji, and UTF-16 endianness. The strategy emphasizes **safety**, **predictability**, and **correctness**, avoiding misclassification whenever possible.

---

## 1. Objectives

The encoding detection algorithm aims to:

1. **Reliably identify common Japanese encodings** (UTF-8, UTF-16 LE/BE, Shift_JIS, CP932, EUC-JP).
2. **Correctly handle UTF-8 with emoji**, which often breaks CP932/Shift_JIS detection.
3. **Determine UTF-16 endianess using BOM and structural validation**.
4. **Use chardet for fallback only**, never blindly trusting its guess.
5. **Fail safely** — return `None` when uncertain, rather than outputting a wrong encoding.

---

## 2. Design Philosophy

### 2.1 Prioritization Rules

1. **UTF-16 with BOM** → Most reliable → check first
2. **UTF-8 direct decode** → Ensures emoji-safe detection
3. **chardet fallback** → Only provide hints
4. **Japanese legacy encoding heuristics**
5. **Fail-safe** detection instead of guessing incorrectly

---

## 3. Detection Flow Overview

### Step 1. Read file bytes

All reading errors (IOError/OSError) are caught and reported.

---

### Step 2. UTF-16 BOM Detection

UTF-16 LE BOM: `FF FE`
UTF-16 BE BOM: `FE FF`

If BOM is present, encoding is determined directly.

---

### Step 3. UTF-8 Direct Decode

- Attempt to decode as UTF-8.
- If success:
  - **Return "utf-8"**
  - **Why:**
    - Modern standard encoding
    - Emoji-safe
    - Prevents CP932/Shift_JIS misclassification

---

### Step 4. chardet Fallback

- Chardet is used only after UTF-8 fails.
- Chunked feed improves accuracy:

  ```python
  detector.feed(raw_bytes[i:i+1024])
  ```

- **Normalization:**
  - `"ascii"` → treat as `"utf-8"` (UTF-8 superset rule)
- If no encoding is produced → return `None`.

---

### Step 5. Windows-125x Corrections for Japanese Encodings

- Chardet frequently misdetects Japanese text as `"Windows-1252"`.
- When this occurs:
  - Test decodability using:
    - `shift_jis`
    - `cp932`
    - `euc-jp`
  - Return the first one that decodes successfully.

---

### Step 6. UTF-16 Without BOM

- If chardet reports:
  - `"utf-16"`
  - `"utf-16-le"`
  - `"utf-16-be"`
- Then:
  - Use BOM when present.
  - Use chardet’s endian otherwise.
  - Validate via `is_valid_utf16()`.
  - If invalid → return `None`.

---

### Step 7. Return Final Encoding

- Return one of:
  - Detected encoding
  - `None` (if unsafely ambiguous)

---

## 4. Advantages for Japanese Environments

✔ Emoji-safe UTF-8 detection
No accidental fallback to CP932.

✔ Stable UTF-16 identification
BOM and structural validation greatly reduce errors.

✔ Corrects chardet’s weak areas
Especially:

- UTF-8 misdetected as Windows-1252
- CP932 misdetected as Windows-1252
- UTF-16 misdetected as UTF-8 (without BOM)

✔ Safe and conservative
Returns `None` instead of wrong answers.

---

## 5. Known Limitations

- Distinguishing Shift_JIS vs CP932 is inherently ambiguous.
- Very short files (<4 bytes) cannot be reliably analyzed.
- Some EUC-JP/Shift_JIS overlaps cannot be resolved.

---

## 6. Possible Future Enhancements

- Statistical scoring of Japanese encodings.
- UTF-7 support (legacy mail systems).
- More advanced heuristic for CJK text patterns.
- Confidence score output.

---

## 7. Summary

This encoding detection strategy is:

- Safe
- Emoji-aware
- Japanese-optimized
- Robust in real-world environments

It avoids common misclassification pitfalls while providing predictable and correct results.
