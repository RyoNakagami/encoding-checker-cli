# encoding-checker-cli

A command-line tool for detecting and converting text file encodings.

## Features

- Detects encoding of text files (e.g., UTF-8, Shift-JIS, EUC-JP)
- CLI interface for quick checks
- Python API for integration

## Encoding Detection Strategy

see [docs/ENCODING_DETECTION_STRATEGY.md](docs/ENCODING_DETECTION_STRATEGY.md)

## Usage

### CLI

```bash
pycheck-encoding <filename>
```

```bash
$ pycheck-encoding --help

 Usage: pycheck-encoding [OPTIONS] [FILE_PATH]

 This script provides a simple command-line tool to detect the text
 encoding of a given file. It attempts to decode the file's binary
 contents using a list of common encodings including UTF-8, UTF-16,
 UTF-32, Shift_JIS, EUC-JP, ISO-8859 variants, CP932, and others.

 If the file can be successfully decoded with one of these encodings, the
 script reports the detected encoding. If none of the encodings work, it
 notifies the user that the encoding could not be determined.

╭─ Arguments ─────────────────────────────────────────────────────────────╮
│   file_path      [FILE_PATH]  Path to the file to check encoding.       │
╰─────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────╮
│ --version  -v        Show version information and exit.                 │
│ --help               Show this message and exit.                        │
╰─────────────────────────────────────────────────────────────────────────╯
```

### Python API

```python
from encoding_checker_cli.encoding import detect_encoding

encoding = detect_encoding("sample.txt")
print(f"Detected encoding: {encoding}")
```

## Installation

```bash
uv tool install git+https://github.com/RyoNakagami/encoding-checker-cli
```

## Test

Run all tests with pytest:

```bash
pytest
```

See [`docs/TEST_STRATEGY.md`](docs/TEST_STRATEGY.md) for details.

## License

MIT License
