import re, os

SECTION_MAP = {
    r'\.SH "NAME"': '.SH "\u540d\u79f0"',
    r'\.SH NAME': '.SH \u540d\u79f0',
    r'\.SH "SYNOPSIS"': '.SH "\u6982\u8ff0"',
    r'\.SH SYNOPSIS': '.SH \u6982\u8ff0',
    r'\.SH "DESCRIPTION"': '.SH "\u63cf\u8ff0"',
    r'\.SH DESCRIPTION': '.SH \u63cf\u8ff0',
    r'\.SH "OPTIONS"': '.SH "\u9009\u9879"',
    r'\.SH OPTIONS': '.SH \u9009\u9879',
    r'\.SH "CONFIGURATION"': '.SH "\u914d\u7f6e"',
    r'\.SH CONFIGURATION': '.SH \u914d\u7f6e',
    r'\.SH "EXAMPLES"': '.SH "\u793a\u4f8b"',
    r'\.SH EXAMPLES': '.SH \u793a\u4f8b',
    r'\.SH "SEE ALSO"': '.SH "\u53e6\u8bf7\u53c2\u9605"',
    r'\.SH SEE ALSO': '.SH \u53e6\u8bf7\u53c2\u9605',
    r'\.SH "GIT"': '.SH "GIT"',
    r'\.SH GIT': '.SH GIT',
    r'\.SH "DISCUSSION"': '.SH "\u8ba8\u8bba"',
    r'\.SH DISCUSSION': '.SH \u8ba8\u8bba',
    r'\.SH "OUTPUT"': '.SH "\u8f93\u51fa"',
    r'\.SH OUTPUT': '.SH \u8f93\u51fa',
    r'\.SH "EXIT STATUS"': '.SH "\u9000\u51fa\u72b6\u6001"',
    r'\.SH EXIT STATUS': '.SH \u9000\u51fa\u72b6\u6001',
    r'\.SH "BUGS"': '.SH "\u7f3a\u9677"',
    r'\.SH BUGS': '.SH \u7f3a\u9677',
    r'\.SH "CAVEATS"': '.SH "\u6ce8\u610f\u4e8b\u9879"',
    r'\.SH CAVEATS': '.SH \u6ce8\u610f\u4e8b\u9879',
    r'\.SH "FORMATS"': '.SH "\u683c\u5f0f"',
    r'\.SH FORMATS': '.SH \u683c\u5f0f',
    r'\.SH "NOTES"': '.SH "\u5907\u6ce8"',
    r'\.SH NOTES': '.SH \u5907\u6ce8',
    r'\.SH "WARNING"': '.SH "\u8b66\u544a"',
    r'\.SH WARNING': '.SH \u8b66\u544a',
    r'\.SH "COMMANDS"': '.SH "\u547d\u4ee4"',
    r'\.SH COMMANDS': '.SH \u547d\u4ee4',
    r'\.SH "QUARANTINE ENVIRONMENT"': '.SH "\u9694\u79bb\u73af\u5883"',
    r'\.SH "OUTPUT STABILITY"': '.SH "\u8f93\u51fa\u7a33\u5b9a\u6027"',
    r'\.SH "ALGORITHM"': '.SH "\u7b97\u6cd5"',
    r'\.SH "MERGING"': '.SH "\u5408\u5e76"',
    r'\.SH "SPARSE CHECKOUT"': '.SH "\u7a00\u758f\u68c0\u51fa"',
    r'\.SH "SPECIFYING REFS"': '.SH "\u6307\u5b9a\u5f15\u7528"',
    r'\.SH "SENDING PATCHES"': '.SH "\u53d1\u9001\u8865\u4e01"',
    r'\.SH "INFO KEYS"': '.SH "\u4fe1\u606f\u952e"',
    r'\.SH "KNOWN LIMITATIONS"': '.SH "\u5df2\u77e5\u9650\u5236"',
    r'\.SH "CREATING REPLACEMENT OBJECTS"': '.SH "\u521b\u5efa\u66ff\u6362\u5bf9\u8c61"',
    r'\.SH "DELTA ISLANDS"': '.SH "\u589e\u91cf\u5b64\u5c9b"',
    r'\.SH "PRE-RECEIVE HOOK"': '.SH "\u9884\u63a5\u6536\u94a9\u5b50"',
    r'\.SH "UPDATE HOOK"': '.SH "\u66f4\u65b0\u94a9\u5b50"',
    r'\.SH "POST-RECEIVE HOOK"': '.SH "\u63a5\u6536\u540e\u94a9\u5b50"',
    r'\.SH "POST-UPDATE HOOK"': '.SH "\u66f4\u65b0\u540e\u94a9\u5b50"',
    r'\.SH "SPECIFYING REVISIONS"': '.SH "\u6307\u5b9a\u4fee\u8ba2\u7248\u672c"',
    r'\.SH "SPECIFYING RANGES"': '.SH "\u6307\u5b9a\u8303\u56f4"',
    r'\.SH "REVISION RANGE SUMMARY"': '.SH "\u4fee\u8ba2\u8303\u56f4\u6458\u8981"',
    r'\.SH "PARSEOPT"': '.SH "\u89e3\u6790\u9009\u9879"',
    r'\.SH "SQ-QUOTE"': '.SH "SQ\u5f15\u7528"',
    r'\.SH "INTERACTIVE USE"': '.SH "\u4ea4\u4e92\u4f7f\u7528"',
    r'\.SH "ENVIRONMENT VARIABLES"': '.SH "\u73af\u5883\u53d8\u91cf"',
    r'\.SH "ENVIRONMENT VARIABLES PASSED TO COMMAND"': '.SH "\u4f20\u9012\u7ed9\u547d\u4ee4\u7684\u73af\u5883\u53d8\u91cf"',
    r'\.SH "EXAMPLES OF SMTP SERVERS"': '.SH "SMTP\u670d\u52a1\u5668\u793a\u4f8b"',
    r'\.SH "GIT"': '.SH "GIT"',
    r'\.SH "PRETTY FORMATS"': '.SH "\u7f8e\u5316\u683c\u5f0f"',
    r'\.SH PRETTY FORMATS': '.SH \u7f8e\u5316\u683c\u5f0f',
}

SS_MAP = {
    'Commit Limiting': '\u63d0\u4ea4\u9650\u5236',
    'Commit Ordering': '\u63d0\u4ea4\u6392\u5e8f',
    'Object Traversal': '\u5bf9\u8c61\u904d\u5386',
    'History Simplification': '\u5386\u53f2\u7b80\u5316',
    'Bisection Helpers': '\u4e8c\u5206\u67e5\u627e\u8f85\u52a9',
    'Single Tree Merge': '\u5355\u6811\u5408\u5e76',
    'Two Tree Merge': '\u53cc\u6811\u5408\u5e76',
    '3-Way Merge': '\u4e09\u8def\u5408\u5e76',
    'Composing': '\u64b0\u5199',
    'Sending': '\u53d1\u9001',
    'Automating': '\u81ea\u52a8\u5316',
    'Administering': '\u7ba1\u7406',
    'Information': '\u4fe1\u606f',
    'Operation Modes': '\u64cd\u4f5c\u6a21\u5f0f',
    'Example': '\u793a\u4f8b',
    'Input Format': '\u8f93\u5165\u683c\u5f0f',
    'Usage text': '\u7528\u6cd5\u6587\u672c',
    'Commit Exclusions': '\u63d0\u4ea4\u6392\u9664',
    'Dotted Range Notations': '\u70b9\u8303\u56f4\u8868\u793a\u6cd5',
    'Commit Formatting': '\u63d0\u4ea4\u683c\u5f0f\u5316',
}

PHRASES = {
    'Part of the \\fBgit\\fR(1) suite': '\\fBgit\\fR(1) \u5957\u4ef6\u7684\u4e00\u90e8\u5206',
    '\\fBNote\\fR': '\\fB\u6ce8\u610f\\fR',
}

def process_line(line):
    s = line.strip()
    # Check exact SH matches
    for en, zh in SECTION_MAP.items():
        if s == en:
            return zh
    
    # SS headers
    ss = re.match(r'^\.SS "(.+)"$', s)
    if ss:
        txt = ss.group(1)
        if txt in SS_MAP:
            return f'.SS "{SS_MAP[txt]}"'
    
    # Replace Note
    if '\\fBNote\\fR' in line:
        idx = line.find('\\fBNote\\fR')
        return line[:idx] + '\\fB\u6ce8\u610f\\fR' + line[idx+10:]
    
    # Part of git suite
    if 'Part of the \\fBgit\\fR(1) suite' in line:
        return line.replace('Part of the \\fBgit\\fR(1) suite', 
                          '\\fBgit\\fR(1) \u5957\u4ef6\u7684\u4e00\u90e8\u5206')
    
    return line

remaining = """git-replay git-rev-list git-rev-parse git-send-email git-shortlog
git-show-branch git-show-index git-show-ref git-sparse-checkout git-stage
git-stripspace git-subtree git-svn git-symbolic-ref git-update-index""".split()

for cmd in remaining:
    src = f'/tmp/{cmd}.1'
    dst = f'/tmp/man1_zh/{cmd}.1'
    if os.path.exists(src):
        with open(src) as f:
            lines = f.readlines()
        with open(dst, 'w') as f:
            for line in lines:
                f.write(process_line(line.rstrip('\n')) + '\n')
        print(f'OK: {cmd}')

