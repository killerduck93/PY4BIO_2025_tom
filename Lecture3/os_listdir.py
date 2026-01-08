import os

# Current directory
directory = "./"

# Obtain list of files in directory
files = sorted(os.listdir(directory))
print(files)

def read_first_line_utf8(path: str) -> str:
    """Return first line of file trying UTF-8, falling back, else raise.

    Strategy:
    1. Try utf-8
    2. Try latin-1 (lossless single-byte) if utf-8 fails
    3. If still empty or undecodable, return a marker string.
    """
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.readline().rstrip()
    except UnicodeDecodeError:
        try:
            with open(path, "r", encoding="latin-1") as fh:
                line = fh.readline().rstrip()
                return f"[latin-1] {line}"
        except Exception as e:  # pragma: no cover - very unlikely
            return f"[unreadable: {e}]"

# Loop over files that end with .txt
for filename in files:
    if filename.endswith(".txt"):
        path = os.path.join(directory, filename)
        # Skip if it looks like a binary masquerading as txt (simple heuristic)
        try:
            with open(path, 'rb') as raw:
                sample = raw.read(256)
            if b"\x00" in sample:
                print(f"{filename}: [skipped – binary file]")
                continue
        except OSError as e:
            print(f"{filename}: [could not open: {e}]")
            continue

        first_line = read_first_line_utf8(path)
        print(f"{filename}: {first_line}")

