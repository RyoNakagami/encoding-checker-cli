---
author: "Ryo Nakagami"
date-modified: "2025-12-03"
project: encoding-checker-cli
---

# Markdownlint Rules Document

| Rule  | Enabled    | Scope / Notes                        |
| ----- | ---------- | ------------------------------------ |
| MD013 | ✅ Enabled  | 80-character limit, excluding tables |
| MD033 | ❌ Disabled | Allows usage of inline HTML          |

## MD013 – Line Length

- MD013 is a rule that limits the maximum number of characters per line in Markdown.
- This setting ensures readability while providing flexibility for tables.

### MD013 Example Settings for VSCode

```json
"MD013": {
  "tables": false,
  "code_blocks": true,
  "headings": true,
  "line_length": 100
}
```

| Option        | Value   | Description                                    |
| ------------- | ------- | ---------------------------------------------- |
| `tables`      | `false` | Do not enforce line length limit inside tables |
| `code_blocks` | `true`  | Enforce line length limit in code blocks       |
| `headings`    | `true`  | Enforce line length limit in headings          |
| `line_length` | `100`   | Set maximum line length to 100 characters      |

## MD033 – インライン HTML

- MD033 is a rule that warns against using inline HTML in Markdown.
- Setting it to `false` allows combining HTML for advanced formatting.

### MD033 Example Settings for VSCode

```json
"MD033": false
```

## MD036 – Spaces Around Headings (No Emphasis As Header)

- MD036 is a rule that warns when emphasis (e.g., **text** or _text_) is used as a heading.
- Examples like `**Heading**` or `_Heading_` are not allowed.
- Setting it to `false` disables this warning.

### MD036 Example Settings for VSCode

```json
"MD036": false
```
