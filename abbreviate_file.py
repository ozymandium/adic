#!/usr/bin/env python
"""
create a shorter version of a long text file by only keeping the beginning

Usage:
  abbreviate_alog_file.py <input> <output> <# lines>
"""
import sys, os

max_lines = int(sys.argv[3])
new_lines = []
count = 0

with open(os.path.abspath(sys.argv[1]), 'r') as f:
  for line in f:
    new_lines.append(line)
    count += 1
    if count > max_lines:
      break

with open(os.path.abspath(sys.argv[2]), 'w') as f:
  for line in new_lines:
    f.write(line)
