#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess, os

# Read original English man page
result = subprocess.run(['zcat', '/usr/share/man/man1/chown.1.gz'], capture_output=True, text=True)
lines = result.stdout.split('\n')

# Build translation map for lines
# We'll translate line by line, translating only the English text portions
# while preserving all formatting codes exactly

translated_lines = []
for line in lines:
    if line.startswith('.TH CHOWN'):
        # Translate "User Commands" to "用户命令"
        line = line.replace('"User Commands"', '"\\(`\\(`\\(`\\(`\\(`"')  # placeholder
    elif line.startswith('.SH NAME'):
        # First replace section header
        line = line.replace('.SH NAME', '.SH \n\\(`')
        # Translate the description after the command
        # "chown \- change file owner and group" -> "chown \- \\(`\\(`\\(`\\(`\\(`\\(`\\(`\\(`\\(`\\(`\\(`\\(`\\(`\\(`\\(`\\(`\\(`\\(`\\(`"
    translated_lines.append(line)

# Write the file
with open('/tmp/man1_zh/chown.1', 'w') as f:
    f.write(result.stdout)  # Just write original for now

print("Temporary file written - still in English")
subprocess.run(['ls', '-la', '/tmp/man1_zh/chown.1'])
