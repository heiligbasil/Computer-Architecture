#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) < 2:
    print('Usage: ls8.py <filename>.ls8')
    sys.exit(1)

cpu = CPU()
filename = sys.argv[1]
print(f"Loading program '{filename}'...")
cpu.load(filename)
print('Executing program...')
cpu.run()
