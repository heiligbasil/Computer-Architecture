import sys

if len(sys.argv) != 2:
    print('Usage: file.py filename')
    sys.exit(1)

filename = sys.argv[1]

try:
    with open(filename) as f:
        for line in f:
            # Ignore comments
            comment_split = line.split('#')
            # Strip out whitespace
            num = comment_split[0].strip()
            # Ignore blank lines
            if num == '':
                continue
            val = int(num)
except FileNotFoundError:
    print('File not found')
    sys.exit(2)
