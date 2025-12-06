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

### Python API

```python
from encoding_checker_cli.encoding import detect_encoding

encoding = detect_encoding("sample.txt")
print(f"Detected encoding: {encoding}")
```

## Installation

```bash
pip install .
```

## Test

Run all tests with pytest:

```bash
pytest
```

See [`docs/TEST_STRATEGY.md`](docs/TEST_STRATEGY.md) for details.

## License

MIT License
