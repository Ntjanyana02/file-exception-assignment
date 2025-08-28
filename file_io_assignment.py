#!/usr/bin/env python3
"""
File Handling & Exception Handling Assignment

Part 1: File Read & Write Challenge
- Read a text file and write a modified version to a new file.
- This script:
    * trims extra spaces,
    * collapses internal whitespace,
    * uppercases text,
    * adds line numbers.

Part 2: Error Handling Lab
- Prompt the user for a filename.
- Gracefully handle errors if it doesn't exist or can't be read.

Output
- The modified file is saved as: modified_<original_name>.txt (same folder).
"""

from pathlib import Path

def transform_text(text: str) -> str:
    """
    Modify the content:
    - Strip leading/trailing whitespace per line.
    - Collapse multiple spaces/tabs within lines.
    - Uppercase all text.
    - Add line numbers.
    """
    lines = text.splitlines()
    cleaned = [" ".join(line.strip().split()) for line in lines]  # collapse whitespace
    cleaned_upper = [ln.upper() for ln in cleaned]

    width = len(str(max(1, len(cleaned_upper))))
    numbered = [f"{i:0{width}d} | {ln}" for i, ln in enumerate(cleaned_upper, start=1)]
    return "\n".join(numbered) + ("\n" if text.endswith("\n") else "")

def read_text(path: Path) -> str:
    """Read file as UTF-8 text."""
    with path.open("r", encoding="utf-8") as f:
        return f.read()

def write_text(path: Path, content: str) -> None:
    """Write UTF-8 text (creates or overwrites)."""
    with path.open("w", encoding="utf-8") as f:
        f.write(content)

def main() -> None:
    print("=== File Handling & Exception Handling Assignment ===")
    print("Tip: Enter a path like 'input.txt' or 'docs/notes.txt'. Type 'q' to quit.\n")

    while True:
        try:
            user = input("Enter the filename to read: ").strip()
            if user.lower() in {"q", "quit", "exit"}:
                print("Goodbye!")
                return

            src = Path(user)
            if not src.exists():
                print("Error: File not found. Please try again.\n")
                continue
            if not src.is_file():
                print("Error: That path is not a file. Please try again.\n")
                continue

            try:
                original = read_text(src)
            except UnicodeDecodeError:
                print("Error: Could not decode file as UTF-8 text.")
                print("Try saving it as UTF-8 or pick a different file.\n")
                continue
            except PermissionError:
                print("Error: Permission denied when reading the file.\n")
                continue
            except OSError as e:
                print(f"Error: Could not read the file ({e}).\n")
                continue

            # Transform and write
            modified = transform_text(original)
            out_name = f"modified_{src.stem}.txt"
            dst = src.with_name(out_name)

            try:
                write_text(dst, modified)
            except PermissionError:
                print("Error: Permission denied when writing the output file.\n")
                continue
            except OSError as e:
                print(f"Error: Could not write the output file ({e}).\n")
                continue

            print(f"\nSuccess! Wrote modified file to: {dst.resolve()}\n")
            break

        except KeyboardInterrupt:
            print("\nCanceled by user. Goodbye!")
            return

if __name__ == "__main__":
    main()
