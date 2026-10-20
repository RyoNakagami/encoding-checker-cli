# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2026-10-20

### Added

- Commit message rules based on Conventional Commits (`docs/COMMITRULES.md`).
- Unit tests for the chardet fallback in `detect_file_encoding`: use of the top-level `chardet.UniversalDetector`, operation without the `chardet.universaldetector` submodule, 1024-byte chunk feeding, early stop when the detector is done, and `None` when no encoding is detected.

### Changed

- Raise the minimum `chardet` version to 7.0.0 (`chardet>=7.0.0`); the lockfile now pins chardet 7.7.0.

### Fixed

- Use `chardet.UniversalDetector` instead of `chardet.universaldetector.UniversalDetector` so encoding detection works with chardet 7.x, which no longer exposes the `chardet.universaldetector` submodule.
- Mermaid diagram rendering in the docs.

[Unreleased]: https://github.com/RyoNakagami/encoding-checker-cli/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/RyoNakagami/encoding-checker-cli/compare/v0.1.1...v0.1.2
