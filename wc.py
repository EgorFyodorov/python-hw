import sys

def get_stats(content):
    lines = content.count(b'\n')
    words = len(content.split())
    byte_count = len(content)
    return lines, words, byte_count

def print_stats(lines, words, byte_count, name=None, width=7):
    if name is None:
        print(f"{lines:>{width}} {words:>{width}} {byte_count:>{width}}")
    else:
        print(f"{lines:>{width}} {words:>{width}} {byte_count:>{width}} {name}")

def main():
    args = sys.argv[1:]
    
    if not args:
        try:
            content = sys.stdin.buffer.read()
            lines, words, byte_count = get_stats(content)
            print_stats(lines, words, byte_count, name=None, width=7)
        except KeyboardInterrupt:
            sys.exit(0)
        return

    total_lines = 0
    total_words = 0
    total_bytes = 0
    
    for filename in args:
        try:
            with open(filename, 'rb') as f:
                content = f.read()
                lines, words, byte_count = get_stats(content)
                print_stats(lines, words, byte_count, name=filename, width=7)

                total_lines += lines
                total_words += words
                total_bytes += byte_count
        except FileNotFoundError:
            print(f"wc: {filename}: No such file or directory", file=sys.stderr)
        except IsADirectoryError:
            print(f"wc: {filename}: Is a directory", file=sys.stderr)
            print_stats(0, 0, 0, name=filename, width=7)
        except Exception as e:
            print(f"wc: {filename}: {e}", file=sys.stderr)
    
    if len(args) > 1:
        print_stats(total_lines, total_words, total_bytes, name="total", width=7)

if __name__ == "__main__":
    main()

