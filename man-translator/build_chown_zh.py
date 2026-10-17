#!/usr/bin/env python3
"""Build Chinese translation of chown man page from original English version."""
import subprocess

# Read original
result = subprocess.run(['zcat', '/usr/share/man/man1/chown.1.gz'], capture_output=True, text=True)
orig = result.stdout

# Do string replacements on the entire content
# Use unique substrings from the English to match and replace

# Header: "User Commands" -> "用户命令"
orig = orig.replace('"User Commands"', '"\u7528\u6237\u547d\u4ee4"')

# Section headers
orig = orig.replace('.SH NAME', '.SH \u540d\u79f0')
orig = orig.replace('.SH SYNOPSIS', '.SH \u6982\u8ff0')
orig = orig.replace('.SH DESCRIPTION', '.SH \u63cf\u8ff0')
orig = orig.replace('.SH OPTIONS', '.SH \u9009\u9879')
orig = orig.replace('.SH EXAMPLES', '.SH \u793a\u4f8b')
orig = orig.replace('.SH AUTHOR', '.SH \u4f5c\u8005')
orig = orig.replace('.SH "REPORTING BUGS"', '.SH "\u62a5\u544a\u9519\u8bef"')
orig = orig.replace('.SH COPYRIGHT', '.SH \u7248\u6743')
orig = orig.replace('.SH "SEE ALSO"', '.SH "\u53e6\u8bf7\u53c2\u89c1"')

# NAME section text after the section header
orig = orig.replace('chown \\- change file owner and group',
                    'chown \\- \u66f4\u6539\u6587\u4ef6\u6240\u6709\u8005\u548c\u6240\u5c5e\u7ec4')

# DESCRIPTION section - replace entire text block
desc_block = """This manual page
documents the GNU version of
.BR chown .
.B chown
changes the user and/or group ownership of each given file.  If
only an owner (a user name or numeric user ID) is given, that user is made the
owner of each given file, and the files' group is not changed.  If the
owner is followed by a colon and a group name (or numeric group ID),
with no spaces between them, the group ownership of the files is
changed as well.  If a colon but no group name follows the user name,
that user is made the owner of the files and the group of the files is
changed to that user's login group.  If the colon and group are given,
but the owner is omitted, only the group of the files is changed;
in this case,
.B chown
performs the same function as
.BR chgrp .
If only a colon is given, or if the entire operand is empty, neither the
owner nor the group is changed."""

desc_zh = """\u672c\u624b\u518c\u9875\u8bb0\u5f55\u4e86 GNU \u7248\u672c\u7684
.BR chown \u3002
.B chown
\u66f4\u6539\u6bcf\u4e2a\u6307\u5b9a\u6587\u4ef6\u7684\u7528\u6237\u548c/\u6216\u7ec4\u6240\u6709\u6743\u3002\u5982\u679c
\u53ea\u6307\u5b9a\u4e86\u6240\u6709\u8005\uff08\u7528\u6237\u540d\u6216\u6570\u5b57\u7528\u6237 ID\uff09\uff0c\u5219\u8be5\u7528\u6237\u5c06\u6210\u4e3a\u6bcf\u4e2a\u6307\u5b9a
\u6587\u4ef6\u7684\u6240\u6709\u8005\uff0c\u800c\u6587\u4ef6\u7684\u7ec4\u4e0d\u4f1a\u6539\u53d8\u3002\u5982\u679c\u8be5
\u6240\u6709\u8005\u7684\u540e\u9762\u8ddf\u7740\u5192\u53f7\u548c\u7ec4\u540d\uff08\u6216\u6570\u5b57\u7ec4 ID\uff09\uff0c
\u4e14\u4e4b\u95f4\u6ca1\u6709\u7a7a\u683c\uff0c\u5219\u6587\u4ef6\u7684\u7ec4\u6240\u6709\u6743\u4e5f\u4f1a
\u88ab\u66f4\u6539\u3002\u5982\u679c\u7528\u6237\u540d\u540e\u9762\u8ddf\u7740\u5192\u53f7\u4f46\u6ca1\u6709\u7ec4\u540d\uff0c
\u5219\u8be5\u7528\u6237\u5c06\u6210\u4e3a\u6587\u4ef6\u7684\u6240\u6709\u8005\uff0c\u5e76\u4e14\u6587\u4ef6\u7684\u7ec4\u5c06
\u88ab\u66f4\u6539\u4e3a\u8be5\u7528\u6237\u7684\u767b\u5f55\u7ec4\u3002\u5982\u679c\u6307\u5b9a\u4e86\u5192\u53f7\u548c\u7ec4\uff0c
\u4f46\u7701\u7565\u4e86\u6240\u6709\u8005\uff0c\u5219\u53ea\u66f4\u6539\u6587\u4ef6\u7684\u7ec4\uff1b
\u5728\u8fd9\u79cd\u60c5\u51b5\u4e0b\uff0c
.B chown
\u6267\u884c\u4e0e
.BR chgrp
\u76f8\u540c\u7684\u529f\u80fd\u3002
\u5982\u679c\u53ea\u7ed9\u51fa\u4e86\u4e00\u4e2a\u5192\u53f7\uff0c\u6216\u8005\u6574\u4e2a\u64cd\u4f5c\u6570\u4e3a\u7a7a\uff0c\u5219
\u6240\u6709\u8005\u548c\u7ec4\u90fd\u4e0d\u4f1a\u88ab\u66f4\u6539\u3002"""

orig = orig.replace(desc_block, desc_zh)

# OPTIONS intro
orig = orig.replace(
    'Change the owner and/or group of each FILE to OWNER and/or GROUP.',
    '\u5c06\u6bcf\u4e2a FILE \u7684\u6240\u6709\u8005\u548c/\u6216\u7ec4\u66f4\u6539\u4e3a OWNER \u548c/\u6216 GROUP\u3002'
)
orig = orig.replace(
    'With \\fB\\-\\-reference\\fR, change the owner and group of each FILE to those of RFILE.',
    '\u4f7f\u7528 \\fB\\-\\-reference\\fR \u65f6\uff0c\u5c06\u6bcf\u4e2a FILE \u7684\u6240\u6709\u8005\u548c\u7ec4\u66f4\u6539\u4e3a RFILE \u7684\u6240\u6709\u8005\u548c\u7ec4\u3002'
)

# Option descriptions
orig = orig.replace(
    'like verbose but report only when a change is made',
    '\u7c7b\u4f3c\u4e8e verbose\uff0c\u4f46\u4ec5\u5728\u53d1\u751f\u66f4\u6539\u65f6\u62a5\u544a'
)
orig = orig.replace(
    'suppress most error messages',
    '\u6291\u5236\u5927\u591a\u6570\u9519\u8bef\u6d88\u606f'
)
orig = orig.replace(
    'output a diagnostic for every file processed',
    '\u4e3a\u6bcf\u4e2a\u5904\u7406\u7684\u6587\u4ef6\u8f93\u51fa\u8bca\u65ad\u4fe1\u606f'
)
orig = orig.replace(
    'affect the referent of each symbolic link (this is\nthe default), rather than the symbolic link itself',
    '\u5f71\u54cd\u6bcf\u4e2a\u7b26\u53f7\u94fe\u63a5\u6240\u5f15\u7528\u7684\u6587\u4ef6\uff08\u8fd9\u662f\n\u9ed8\u8ba4\u884c\u4e3a\uff09\uff0c\u800c\u4e0d\u662f\u7b26\u53f7\u94fe\u63a5\u672c\u8eab'
)
orig = orig.replace(
    'affect symbolic links instead of any referenced file;\nuseful only on systems that can change the ownership of a symlink',
    '\u5f71\u54cd\u7b26\u53f7\u94fe\u63a5\u672c\u8eab\u800c\u975e\u4efb\u4f55\u5f15\u7528\u7684\u6587\u4ef6\uff1b\n\u4ec5\u5728\u80fd\u591f\u66f4\u6539\u7b26\u53f7\u94fe\u63a5\u6240\u6709\u6743\u7684\u7cfb\u7edf\u4e0a\u6709\u7528'
)
orig = orig.replace(
    'change the ownership of each file only if its\ncurrent owner and/or group match those specified here.\nEither may be omitted, in which case a match\nis not required for the omitted attribute',
    '\u4ec5\u5f53\u6bcf\u4e2a\u6587\u4ef6\u7684\u5f53\u524d\u6240\u6709\u8005\u548c/\u6216\u7ec4\u4e0e\u6b64\u5904\u6307\u5b9a\u7684\u76f8\u5339\u914d\u65f6\u624d\u66f4\u6539\u5176\u6240\u6709\u6743\u3002\n\u4e24\u8005\u4e2d\u7684\u4efb\u4f55\u4e00\u4e2a\u90fd\u53ef\u4ee5\u7701\u7565\uff0c\u5728\u8fd9\u79cd\u60c5\u51b5\u4e0b\uff0c\n\u7701\u7565\u7684\u5c5e\u6027\u4e0d\u9700\u8981\u5339\u914d'
)
orig = orig.replace(
    "do not treat '/' specially (the default)",
    "\u4e0d\u5bf9 '/' \u8fdb\u884c\u7279\u6b8a\u5904\u7406\uff08\u9ed8\u8ba4\u884c\u4e3a\uff09"
)
orig = orig.replace(
    "fail to operate recursively on '/'",
    "\u65e0\u6cd5\u5bf9 '/' \u8fdb\u884c\u9012\u5f52\u64cd\u4f5c"
)
orig = orig.replace(
    "use RFILE's ownership rather than specifying values.\nRFILE is always dereferenced if a symbolic link.",
    '\u4f7f\u7528 RFILE \u7684\u6240\u6709\u6743\u800c\u975e\u6307\u5b9a\u503c\u3002\n\u5982\u679c RFILE \u662f\u7b26\u53f7\u94fe\u63a5\uff0c\u5219\u59cb\u7ec8\u4f1a\u89e3\u5f15\u7528\u5b83\u3002'
)
orig = orig.replace(
    'operate on files and directories recursively',
    '\u9012\u5f52\u5730\u5bf9\u6587\u4ef6\u548c\u76ee\u5f55\u8fdb\u884c\u64cd\u4f5c'
)

# Traversal options
orig = orig.replace(
    'The following options modify how a hierarchy is traversed when the \\fB\\-R\\fR\noption is also specified.  If more than one is specified, only the final\none takes effect. \\fB\\-P\\fR is the default.',
    '\u4ee5\u4e0b\u9009\u9879\u4fee\u6539\u540c\u65f6\u6307\u5b9a\u4e86 \\fB\\-R\\fR\n\u9009\u9879\u65f6\u904d\u5386\u5c42\u6b21\u7ed3\u6784\u7684\u65b9\u5f0f\u3002\u5982\u679c\u6307\u5b9a\u4e86\u591a\u4e2a\u9009\u9879\uff0c\u5219\u53ea\u6709\u6700\u540e\u4e00\u4e2a\n\u751f\u6548\u3002\\fB\\-P\\fR \u662f\u9ed8\u8ba4\u503c\u3002'
)

orig = orig.replace(
    'if a command line argument is a symlink to a directory, traverse it',
    '\u5982\u679c\u547d\u4ee4\u884c\u53c2\u6570\u662f\u6307\u5411\u76ee\u5f55\u7684\u7b26\u53f7\u94fe\u63a5\uff0c\u5219\u904d\u5386\u5b83'
)
orig = orig.replace(
    'traverse every symbolic link to a directory encountered',
    '\u904d\u5386\u9047\u5230\u7684\u6bcf\u4e2a\u6307\u5411\u76ee\u5f55\u7684\u7b26\u53f7\u94fe\u63a5'
)
orig = orig.replace(
    'do not traverse any symbolic links',
    '\u4e0d\u904d\u5386\u4efb\u4f55\u7b26\u53f7\u94fe\u63a5'
)
orig = orig.replace(
    'display this help and exit',
    '\u663e\u793a\u6b64\u5e2e\u52a9\u4fe1\u606f\u5e76\u9000\u51fa'
)
orig = orig.replace(
    'output version information and exit',
    '\u8f93\u51fa\u7248\u672c\u4fe1\u606f\u5e76\u9000\u51fa'
)

# Final paragraph
orig = orig.replace(
    'Owner is unchanged if missing.  Group is unchanged if missing, but changed\nto login group if implied by a ',
    '\u5982\u679c\u7f3a\u5c11\u6240\u6709\u8005\uff0c\u5219\u6240\u6709\u8005\u4e0d\u53d8\u3002\u5982\u679c\u7f3a\u5c11\u7ec4\uff0c\u5219\u7ec4\u4e0d\u53d8\uff0c\u4f46\u5982\u679c\n\u7b26\u53f7\u6240\u6709\u8005\u540e\u9762\u8ddf\u7740 '
)

# The single quote after a colon - tricky, need to match: ':' following a symbolic OWNER.
orig = orig.replace(
    "following a symbolic OWNER.",
    "\u9690\u542b\u4e86\u7ec4\u66f4\u6539\uff0c\u5219\u4f1a\u66f4\u6539\u4e3a\u767b\u5f55\u7ec4\u3002"
)
orig = orig.replace(
    'OWNER and GROUP may be numeric as well as symbolic.',
    'OWNER \u548c GROUP \u53ef\u4ee5\u662f\u6570\u5b57\u5f62\u5f0f\u7684\uff0c\u4e5f\u53ef\u4ee5\u662f\u7b26\u53f7\u5f62\u5f0f\u7684\u3002'
)

# Examples
orig = orig.replace(
    'Change the owner of /u to "root".',
    '\u5c06 /u \u7684\u6240\u6709\u8005\u66f4\u6539\u4e3a "root"\u3002'
)
orig = orig.replace(
    'Likewise, but also change its group to "staff".',
    '\u540c\u4e0a\uff0c\u4f46\u540c\u65f6\u5c06\u5176\u7ec4\u66f4\u6539\u4e3a "staff"\u3002'
)
orig = orig.replace(
    'Change the owner of /u and subfiles to "root".',
    '\u5c06 /u \u53ca\u5176\u5b50\u6587\u4ef6\u7684\u6240\u6709\u8005\u66f4\u6539\u4e3a "root"\u3002'
)

# Author
orig = orig.replace(
    'Written by David MacKenzie and Jim Meyering.',
    '\u7531 David MacKenzie \u548c Jim Meyering \u7f16\u5199\u3002'
)

# Copyright text
orig = orig.replace(
    'This is free software: you are free to change and redistribute it.',
    '\u8fd9\u662f\u81ea\u7531\u8f6f\u4ef6\uff1a\u60a8\u53ef\u4ee5\u81ea\u7531\u66f4\u6539\u548c\u91cd\u65b0\u5206\u53d1\u5b83\u3002'
)
orig = orig.replace(
    'There is NO WARRANTY, to the extent permitted by law.',
    '\u5728\u6cd5\u5f8b\u5141\u8bb8\u7684\u8303\u56f4\u5185\uff0c\u4e0d\u63d0\u4f9b\u4efb\u4f55\u62c5\u4fdd\u3002'
)

# SEE ALSO
orig = orig.replace(
    'Full documentation <https://www.gnu.org/software/coreutils/chown>',
    '\u5b8c\u6574\u6587\u6863 <https://www.gnu.org/software/coreutils/chown>'
)
orig = orig.replace(
    'or available locally via: ',
    '\u6216\u901a\u8fc7\u4ee5\u4e0b\u65b9\u5f0f\u5728\u672c\u5730\u83b7\u53d6\uff1a'
)

# Write the output
with open('/tmp/man1_zh/chown.1', 'w') as f:
    f.write(orig)

print("Done writing /tmp/man1_zh/chown.1")
print(f"Length: {len(orig)} chars")
