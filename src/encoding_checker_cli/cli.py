import sys
import locale
from pathlib import Path
import typer

from encoding_checker_cli.encoding import detect_file_encoding
from encoding_checker_cli.library.version import __version__

app = typer.Typer(
    invoke_without_command=True,
    no_args_is_help=False,
    help=(
        "This script provides a simple command-line tool to detect the text "
        "encoding of a given file. It attempts to decode the file's binary "
        "contents using a list of common encodings including UTF-8, UTF-16, "
        "UTF-32, Shift_JIS, EUC-JP, ISO-8859 variants, CP932, and others.\n\n"
        "If the file can be successfully decoded with one of these encodings, "
        "the script reports the detected encoding. If none of the encodings "
        "work, it notifies the user that the encoding could not be determined."
    ),
)


def version_callback(value: bool):
    if value:
        print(f"check-encoding-cli {__version__}")
        print(f"Python {sys.version.split()[0]}")
        raise typer.Exit()


@app.callback()
def check_encoding(
    file_path: Path = typer.Argument(
        None,
        help="Path to the file to check encoding.",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version information and exit.",
        callback=version_callback,
        is_eager=True,
    ),
):
    """Run encoding detection."""
    if not Path(file_path).exists():
        print(f"Error: File '{file_path}' does not exist", file=sys.stderr)
        sys.exit(1)

    encoding = detect_file_encoding(file_path)

    if encoding:
        print(f"Detected encoding for '{file_path}': {encoding}")
        if encoding == locale.getpreferredencoding():
            print("(System default encoding)")
    else:
        print(f"Could not detect encoding for '{file_path}'", file=sys.stderr)
        sys.exit(1)


def main():
    app()
