import sys
from collections import deque
from typing import Deque, Iterable, TextIO

def tail_stream(stream: Iterable[str], lines_count: int) -> Deque[str]:
    return deque(stream, maxlen=lines_count)

def print_lines(lines: Iterable[str]) -> None:
    for line in lines:
        print(line, end='')

def main() -> None:
    args = sys.argv[1:]
    
    if not args:
        try:
            lines = tail_stream(sys.stdin, 17)
            print_lines(lines)
        except KeyboardInterrupt:
            sys.exit(0)
        return

    is_multiple_files = len(args) > 1
    first_file = True

    for filename in args:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                if is_multiple_files:
                    if not first_file:
                        print()
                    print(f"==> {filename} <==")
                
                lines = tail_stream(f, 10)
                print_lines(lines)
                
                first_file = False
        except FileNotFoundError:
            print(f"tail: cannot open '{filename}' for reading: No such file or directory", file=sys.stderr)
        except Exception as e:
            print(f"tail: error reading '{filename}': {e}", file=sys.stderr)

if __name__ == "__main__":
    main()

