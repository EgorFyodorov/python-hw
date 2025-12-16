import sys
from typing import TextIO

def nl(input_stream: TextIO) -> None:
    for i, line in enumerate(input_stream, 1):
        print(f"{i:>6}\t{line}", end='')

def main() -> None:
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                nl(f)
        except FileNotFoundError:
            print(f"nl: {filename}: No such file or directory", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"nl: Error reading {filename}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            nl(sys.stdin)
        except KeyboardInterrupt:
            sys.exit(0)

if __name__ == "__main__":
    main()

