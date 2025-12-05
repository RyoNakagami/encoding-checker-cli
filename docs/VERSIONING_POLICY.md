---
author: "Ryo Nakagami"
date-modified: "2025-12-03"
project: encoding-checker-cli
---

# Versioning Policy

- The versioning of `encoding-checker-cli` follows [Semantic Versioning](https://semver.org/).
- The release number is managed in the format `MAJOR.MINOR.PATCH`.

## MAJOR.MINOR.PATCH

| Release Type | Main Content | Backward Compatibility | Main Application Examples |
|:--------------|:----------|:------------|:------------|
| **Major Release** | - Breaking changes<br>- Removal of deprecated features<br>- API updates with behavioral changes<br>- Changes included in a major release are documented in the **Release Note** | ❌ None | `v1.0.0 → v2.0.0` |
| **Minor Release** | - Addition of new features<br>- Large bug fixes<br>- Addition of deprecation announcements | ✅ Yes | `v1.1.0 → v1.2.0` |
| **Patch Release** | - Bug fixes<br>- Stability and performance improvements (non-breaking)<br>- Assurance that existing code continues to work | ✅ Yes | `v1.2.1 → v1.2.2` |

---

### Deprecation Policy

`encoding-checker-cli` follows the deprecation process as outlined below:

1. Deprecations are announced in a **Minor Release**.
2. Warning messages clearly indicate:

    - Replacement method/attribute
    - Version in which the feature will be removed (e.g., `will be removed in 2.0.0`)

3. After the announcement, the feature continues to work within the same major version (`1.x`)
4. Removal occurs in the next Major Release (`2.0.0`).

---

### Example: Deprecation Flow

| Version | Status              | Description                                                                   |
| :------ | :------------------ | :---------------------------------------------------------------------------- |
| `1.2.0` | 🔔 Announcement     | Function `old_method()` is deprecated. Suggested replacement: `new_method()`. |
| `1.3.0` | ⚠ Warning Continues | Continues to work with a warning. Migration is recommended.                   |
| `2.0.0` | ⛔ Removed           | `old_method()` is completely removed.                                         |

---

## References

- [Semantic Versioning](https://semver.org/)
- [Python Package Building Techniques for Regmonkeys > Versioning Policy](https://ryonakagami.github.io/python-statisticalpackage-techniques/posts/python-packaging-guide/versioning.html)
