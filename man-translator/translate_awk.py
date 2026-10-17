import sys, re

def translate_man_page(text):
    lines = text.split('\n')
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Preserve comments and empty lines with formatting
        if line.startswith('.\\"'):
            result.append(line)
            i += 1
            continue
        
        # .TH header translation
        m = re.match(r'^(\.TH\s+AWK\s+"1P"\s+2017\s+)"IEEE/The Open Group"\s+"POSIX Programmer\'s Manual"', line)
        if m:
            result.append(m.group(1) + '"IEEE/The Open Group" "POSIX 程序员手册"')
            i += 1
            continue
        
        # Section headers
        if line.startswith('.SH PROLOG'):
            result.append(line)  # Keep as-is
            i += 1
            continue
        if line.startswith('.SH NAME'):
            result.append('.SH 名称')
            i += 1
            continue
        if line.startswith('.SH SYNOPSIS'):
            result.append('.SH 概述')
            i += 1
            continue
        if line.startswith('.SH DESCRIPTION'):
            result.append('.SH 描述')
            i += 1
            continue
        if line.startswith('.SH OPTIONS'):
            result.append('.SH 选项')
            i += 1
            continue
        if line.startswith('.SH OPERANDS'):
            result.append('.SH 操作数')
            i += 1
            continue
        if line.startswith('.SH STDIN'):
            result.append('.SH 标准输入')
            i += 1
            continue
        if line.startswith('.SH "INPUT FILES"'):
            result.append('.SH "输入文件"')
            i += 1
            continue
        if line.startswith('.SH "OUTPUT FILES"'):
            result.append('.SH "输出文件"')
            i += 1
            continue
        if line.startswith('.SH STDOUT'):
            result.append('.SH 标准输出')
            i += 1
            continue
        if line.startswith('.SH STDERR'):
            result.append('.SH 标准错误')
            i += 1
            continue
        if line.startswith('.SH "ENVIRONMENT VARIABLES"'):
            result.append('.SH "环境变量"')
            i += 1
            continue
        if line.startswith('.SH "ASYNCHRONOUS EVENTS"'):
            result.append('.SH "异步事件"')
            i += 1
            continue
        if line.startswith('.SH "EXTENDED DESCRIPTION"'):
            result.append('.SH "扩展描述"')
            i += 1
            continue
        if line.startswith('.SH "EXIT STATUS"'):
            result.append('.SH 退出状态')
            i += 1
            continue
        if line.startswith('.SH "CONSEQUENCES OF ERRORS"'):
            result.append('.SH "错误后果"')
            i += 1
            continue
        if line.startswith('.SH "APPLICATION USAGE"'):
            result.append('.SH "应用用法"')
            i += 1
            continue
        if line.startswith('.SH EXAMPLES'):
            result.append('.SH 示例')
            i += 1
            continue
        if line.startswith('.SH RATIONALE'):
            result.append('.SH 原理说明')
            i += 1
            continue
        if line.startswith('.SH "FUTURE DIRECTIONS"'):
            result.append('.SH "未来方向"')
            i += 1
            continue
        if line.startswith('.SH "SEE ALSO"'):
            result.append('.SH "另请参见"')
            i += 1
            continue
        if line.startswith('.SH COPYRIGHT'):
            result.append('.SH 版权')
            i += 1
            continue
        
        # Subsection headers
        if line.startswith('.SS "Overall Program Structure"'):
            result.append('.SS "整体程序结构"')
            i += 1
            continue
        if line.startswith('.SS "Expressions in awk"'):
            result.append('.SS "awk 中的表达式"')
            i += 1
            continue
        if line.startswith('.SS "Variables and Special Variables"'):
            result.append('.SS "变量与特殊变量"')
            i += 1
            continue
        if line.startswith('.SS "Regular Expressions"'):
            result.append('.SS "正则表达式"')
            i += 1
            continue
        if line.startswith('.SS "Patterns"'):
            result.append('.SS "模式"')
            i += 1
            continue
        if line.startswith('.SS "Special Patterns"'):
            result.append('.SS "特殊模式"')
            i += 1
            continue
        if line.startswith('.SS "Expression Patterns"'):
            result.append('.SS "表达式模式"')
            i += 1
            continue
        if line.startswith('.SS "Pattern Ranges"'):
            result.append('.SS "模式范围"')
            i += 1
            continue
        if line.startswith('.SS "Actions"'):
            result.append('.SS "动作"')
            i += 1
            continue
        if line.startswith('.SS "Output Statements"'):
            result.append('.SS "输出语句"')
            i += 1
            continue
        if line.startswith('.SS "Functions"'):
            result.append('.SS "函数"')
            i += 1
            continue
        if line.startswith('.SS "Arithmetic Functions"'):
            result.append('.SS "算术函数"')
            i += 1
            continue
        if line.startswith('.SS "String Functions"'):
            result.append('.SS "字符串函数"')
            i += 1
            continue
        if line.startswith('.SS "Input/Output and General Functions"'):
            result.append('.SS "输入/输出与通用函数"')
            i += 1
            continue
        if line.startswith('.SS "User-Defined Functions"'):
            result.append('.SS "用户自定义函数"')
            i += 1
            continue
        if line.startswith('.SS "Grammar"'):
            result.append('.SS "语法"')
            i += 1
            continue
        if line.startswith('.SS "Lexical Conventions"'):
            result.append('.SS "词法约定"')
            i += 1
            continue
        
        # Translate specific English text lines
        line = translate_line(line)
        result.append(line)
        i += 1
    
    return '\n'.join(result)

def translate_line(line):
    # Don't translate lines that are purely formatting/roff
    if not line.strip():
        return line
    if line.lstrip().startswith('.'):
        # Translate text on roff macro lines
        return translate_roff_line(line)
    
    # Plain text lines
    return translate_plain_text(line)

def translate_roff_line(line):
    """Translate text content within roff macro lines"""
    stripped = line.lstrip()
    
    # Skip pure macro lines with no translatable text
    if re.match(r'^\.(TH|SH|SS|LP|P|PP|RE|RS|br|fi|nf|sp|ce|ad)\s', stripped) or stripped in ['.P', '.PP', '.LP', '.RE', '.RS', '.br', '.fi', '.nf', '.sp', '.ce']:
        return line
    
    # Handle .IP lines
    m = re.match(r'^(\.IP\s+".*?"\s+\d+)$', stripped)
    if m:
        return line
    
    # Handle .B, .BR, .IR, etc. lines - these have mostly non-translatable content
    # But some have translatable text mixed in
    
    # Specific translations for known sentences
    if 'This manual page is part of the POSIX' in line:
        return line.replace('This manual page is part of the POSIX Programmer\'s Manual.',
                          '本手册页是 POSIX 程序员手册的一部分。')
    if 'The Linux implementation of this interface may differ' in line:
        return line.replace('The Linux implementation of this interface may differ (consult',
                          '此接口的 Linux 实现可能有所不同（请参阅')
    if 'the corresponding Linux manual page for details of Linux behavior' in line:
        return line.replace('the corresponding Linux manual page for details of Linux behavior',
                          '相应的 Linux 手册页以了解 Linux 行为的详细信息')
    if 'or the interface may not be implemented on Linux' in line:
        return line.replace('or the interface may not be implemented on Linux',
                          '或者该接口可能未在 Linux 上实现')
    if 'pattern scanning and processing language' in line:
        return line.replace('pattern scanning and processing language',
                          '模式扫描与处理语言')
    
    return line

def translate_plain_text(line):
    """Translate plain English text lines"""
    t = translations.get(line.strip(), None)
    if t:
        return t
    return line

# Key phrase translations
translations = {
    # ... main translations
}

# Process the file
text = sys.stdin.read()
result = translate_man_page(text)

# Write detailed translation
# For the full translation, we pass through with structural changes and key phrase translations

print(result)
