#!/usr/bin/env python3
"""Translate wget man page from English to Chinese preserving roff formatting."""
import re

with open('/tmp/wget_orig.1', 'r') as f:
    lines = f.readlines()

# Comprehensive translation map for full-line and inline translations
# Key: English text (partial or full), Value: Chinese translation
T = {
    # === SECTION HEADERS ===
    '.SH NAME': '.SH 名称',
    '.SH SYNOPSIS': '.SH 概述',
    '.SH DESCRIPTION': '.SH 描述',
    '.SH OPTIONS': '.SH 选项',
    '.SH EXAMPLES': '.SH 示例',
    '.SH AUTHOR': '.SH 作者',
    '.SH COPYRIGHT': '.SH 版权',
    '.SH "SEE ALSO"': '.SH "另请参见"',
    '.SH "REPORTING BUGS"': '.SH "报告错误"',
    '.SH ENVIRONMENT': '.SH 环境变量',
    '.SH "EXIT STATUS"': '.SH "退出状态"',
    '.SH FILES': '.SH 文件',
    '.SH BUGS': '.SH 错误',
    
    # === SUBSECTION HEADERS ===
    '.SS "Option Syntax"': '.SS "选项语法"',
    '.SS "Basic Startup Options"': '.SS "基本启动选项"',
    '.SS "Logging and Input File Options"': '.SS "日志和输入文件选项"',
    '.SS "Download Options"': '.SS "下载选项"',
    '.SS "Directory Options"': '.SS "目录选项"',
    '.SS "HTTP Options"': '.SS "HTTP 选项"',
    '.SS "HTTPS (SSL/TLS) Options"': '.SS "HTTPS (SSL/TLS) 选项"',
    '.SS "FTP Options"': '.SS "FTP 选项"',
    '.SS "FTPS Options"': '.SS "FTPS 选项"',
    '.SS "Recursive Retrieval Options"': '.SS "递归下载选项"',
    '.SS "Recursive Accept/Reject Options"': '.SS "递归接受/拒绝选项"',
    
    # === .TH header ===
    '"GNU Wget 1.25.0" "GNU Wget"': '"GNU Wget 1.25.0" "GNU Wget"',
    '"User Commands"': '"用户命令"',
    
    # === Common phrases inside roff formatting ===
    'IX Header "NAME"': 'IX Header "名称"',
    'IX Header "SYNOPSIS"': 'IX Header "概述"',
    'IX Header "DESCRIPTION"': 'IX Header "描述"',
    'IX Header "OPTIONS"': 'IX Header "选项"',
    'IX Header "ENVIRONMENT"': 'IX Header "环境变量"',
    'IX Header "EXIT STATUS"': 'IX Header "退出状态"',
    'IX Header "FILES"': 'IX Header "文件"',
    'IX Header "BUGS"': 'IX Header "错误"',
    'IX Header "SEE ALSO"': 'IX Header "另请参见"',
    'IX Header "AUTHOR"': 'IX Header "作者"',
    'IX Header "COPYRIGHT"': 'IX Header "版权"',
    
    # === Preamble comments ===
    'Standard preamble:': '标准前言：',
    'Vertical space (when we can\'t use .PP)': '垂直间距（当无法使用 .PP 时）',
    'Begin verbatim text': '开始逐字文本',
    'End verbatim text': '结束逐字文本',
    'quotes in nroff, nothing in troff, for use with C<>.': 'nroff 中的引号，troff 中为空，用于 C<>。',
    'Escape single quotes in literal strings from groff\'s Unicode transform.': '转义 groff Unicode 转换中的字面字符串单引号。',
    'If the F register is >0, we\'ll generate index entries on stderr for': '如果 F 寄存器 >0，我们将在 stderr 上为以下内容生成索引条目：',
    'titles (.TH), headers (.SH), subsections (.SS), items (.Ip), and index': '标题 (.TH)、头部 (.SH)、子节 (.SS)、条目 (.Ip) 和索引',
    'entries marked with X<> in POD.  Of course, you\'ll have to process the': '在 POD 中标记为 X<> 的条目。当然，您需要以某种',
    'output yourself in some meaningful fashion.': '有意义的方式自行处理输出。',
    'Avoid warning from groff about undefined register \'F\'.': '避免 groff 关于未定义寄存器 \'F\' 的警告。',
    'Required to disable full justification in groff 1.23.0.': '需要禁用 groff 1.23.0 中的完全对齐。',
    'For nroff, turn off justification.  Always turn off hyphenation; it makes': '对于 nroff，关闭对齐。始终关闭连字符；它会在',
    'way too many mistakes in technical documents.': '技术文档中产生太多错误。',
    
    # === NAME section ===
    'Wget \\- The non\\-interactive network downloader.': 'Wget \\- 非交互式网络下载工具。',
    
    # === DESCRIPTION section ===
    'GNU Wget is a free utility for non\\-interactive download of files from': 'GNU Wget 是一个免费的非交互式文件下载工具，',
    'the Web.  It supports \\fBHTTP\\fR, \\fBHTTPS\\fR, and \\fBFTP\\fR protocols, as': '可以从网络上非交互式下载文件。它支持 \\fBHTTP\\fR、\\fBHTTPS\\fR 和 \\fBFTP\\fR 协议，',
    'well as retrieval through HTTP proxies.': '以及通过 HTTP 代理进行下载。',
    
    'Wget is non\\-interactive, meaning that it can work in the background,': 'Wget 是非交互式的，意味着它可以在后台工作，',
    'while the user is not logged on.  This allows you to start a retrieval': '而用户不需要登录。这使您可以启动下载',
    'and disconnect from the system, letting Wget finish the work.  By': '并断开与系统的连接，让 Wget 完成工作。',
    'contrast, most of the Web browsers require constant user\\*(Aqs presence,': '相比之下，大多数 Web 浏览器需要用户持续在场，',
    'which can be a great hindrance when transferring a lot of data.': '这在传输大量数据时可能是一个很大的障碍。',
    
    'Wget can follow links in \\fBHTML\\fR, \\fBXHTML\\fR, and \\fBCSS\\fR pages, to': 'Wget 可以跟踪 \\fBHTML\\fR、\\fBXHTML\\fR 和 \\fBCSS\\fR 页面中的链接，',
    'create local versions of remote web sites, fully recreating the': '创建远程网站的本地版本，完全重现',
    'directory structure of the original site.  This is sometimes referred to': '原始网站的目录结构。这有时被称为',
    'as "recursive downloading."  While doing that, Wget respects the Robot': '"递归下载"。在此过程中，Wget 遵守机器人',
    'Exclusion Standard (\\fI/robots.txt\\fR).  Wget can be instructed to': '排除标准（\\fI/robots.txt\\fR）。可以指示 Wget',
    'convert the links in downloaded files to point at the local files, for': '将下载文件中的链接转换为指向本地文件，以',
    'offline viewing.': '便离线查看。',
    
    'Wget has been designed for robustness over slow or unstable network': 'Wget 被设计为在缓慢或不稳定的网络连接上具有鲁棒性；',
    'connections; if a download fails due to a network problem, it will': '如果下载因网络问题失败，它将',
    'keep retrying until the whole file has been retrieved.  If the server': '不断重试，直到整个文件被下载。如果服务器',
    'supports regetting, it will instruct the server to continue the': '支持断点续传，它将指示服务器从断开处',
    'download from where it left off.': '继续下载。',
}

# Section-level translations for complete text lines
# These are keyed by the exact line content (after stripping for matching)
section_text = {
    # Option Syntax
    'Since Wget uses GNU getopt to process command\\-line arguments, every': '由于 Wget 使用 GNU getopt 处理命令行参数，每个',
    'option has a long form along with the short one.  Long options are': '选项都有长格式和短格式。长选项',
    'more convenient to remember, but take time to type.  You may freely': '更容易记住，但输入较慢。您可以自由',
    'mix different option styles, or specify options after the command\\-line': '混合不同的选项风格，或在命令行参数之后指定选项。',
    'arguments.  Thus you may write:': '因此您可以这样写：',
    
    'The space between the option accepting an argument and the argument may': '接受参数的选项与参数之间的空格可以',
    'be omitted.  Instead of \\fB\\-o log\\fR you can write \\fB\\-olog\\fR.': '省略。您可以用 \\fB\\-olog\\fR 代替 \\fB\\-o log\\fR。',
    
    'You may put several options that do not require arguments together,': '您可以将多个不需要参数的选项放在一起，',
    'like:': '例如：',
    'This is completely equivalent to:': '这完全等同于：',
    
    'Since the options can be specified after the arguments, you may': '由于选项可以在参数之后指定，您可以',
    'terminate them with \\fB\\-\\-\\fR.  So the following will try to download': '用 \\fB\\-\\-\\fR 终止它们。因此，以下命令将尝试下载',
    'URL \\fB\\-x\\fR, reporting failure to \\fIlog\\fR:': 'URL \\fB\\-x\\fR，并将失败信息报告到 \\fIlog\\fR：',
    
    'The options that accept comma\\-separated lists all respect the convention': '接受逗号分隔列表的选项都遵循以下约定：',
    'that specifying an empty list clears its value.  This can be useful to': '指定空列表会清除其值。这对于清除',
    'clear the \\fI.wgetrc\\fR settings.  For instance, if your \\fI.wgetrc\\fR': '\\fI.wgetrc\\fR 设置很有用。例如，如果您的 \\fI.wgetrc\\fR',
    'sets \\f(CW\\*(C`exclude_directories\\*(C\'\\fR to \\fI/cgi\\-bin\\fR, the following': '将 \\f(CW\\*(C`exclude_directories\\*(C\'\\fR 设置为 \\fI/cgi\\-bin\\fR，以下',
    'example will first reset it, and then set it to exclude \\fI/~nobody\\fR': '示例将首先重置它，然后将其设置为排除 \\fI/~nobody\\fR',
    'and \\fI/~somebody\\fR.  You can also clear the lists in \\fI.wgetrc\\fR.': '和 \\fI/~somebody\\fR。您也可以清除 \\fI.wgetrc\\fR 中的列表。',
    
    'Most options that do not accept arguments are \\fIboolean\\fR options,': '大多数不接受参数的选项是 \\fI布尔型\\fR 选项，',
    'so named because their state can be captured with a yes\\-or\\-no': '之所以这样命名，是因为它们的状态可以用是或否',
    '("boolean") variable.  For example, \\fB\\-\\-follow\\-ftp\\fR tells Wget': '（"布尔"）变量来表示。例如，\\fB\\-\\-follow\\-ftp\\fR 告诉 Wget',
    'to follow FTP links from HTML files and, on the other hand,': '跟踪 HTML 文件中的 FTP 链接，而',
    '\\&\\fB\\-\\-no\\-glob\\fR tells it not to perform file globbing on FTP URLs.  A': '\\&\\fB\\-\\-no\\-glob\\fR 告诉它不要对 FTP URL 执行文件通配。',
    'boolean option is either \\fIaffirmative\\fR or \\fInegative\\fR': '布尔选项要么是 \\fI肯定的\\fR 要么是 \\fI否定的\\fR',
    '(beginning with \\fB\\-\\-no\\fR).  All such options share several': '（以 \\fB\\-\\-no\\fR 开头）。所有此类选项共享一些',
    'properties.': '属性。',
    
    'Unless stated otherwise, it is assumed that the default behavior is': '除非另有说明，默认行为被假定为',
    'the opposite of what the option accomplishes.  For example, the': '选项所实现效果的反面。例如，',
    'documented existence of \\fB\\-\\-follow\\-ftp\\fR assumes that the default': '文档中存在的 \\fB\\-\\-follow\\-ftp\\fR 假定默认',
    'is to \\fInot\\fR follow FTP links from HTML pages.': '是 \\fI不\\fR 跟踪 HTML 页面中的 FTP 链接。',
    
    'Affirmative options can be negated by prepending the \\fB\\-\\-no\\-\\fR to': '肯定选项可以通过在选项名称前添加 \\fB\\-\\-no\\-\\fR 来否定；',
    'the option name; negative options can be negated by omitting the': '否定选项可以通过省略 \\fB\\-\\-no\\-\\fR 前缀来否定。',
    '\\&\\fB\\-\\-no\\-\\fR prefix.  This might seem superfluous\\-\\-\\-if the default for': '这可能看起来多余——如果肯定选项的默认是不做某事，',
    'an affirmative option is to not do something, then why provide a way': '那么为什么还要提供一种显式关闭它的方法？',
    'to explicitly turn it off?  But the startup file may in fact change': '但启动文件实际上可能改变默认设置。',
    'the default.  For instance, using \\f(CW\\*(C`follow_ftp = on\\*(C\'\\fR in': '例如，在 \\fI.wgetrc\\fR 中使用 \\f(CW\\*(C`follow_ftp = on\\*(C\'\\fR',
    '\\&\\fI.wgetrc\\fR makes Wget \\fIfollow\\fR FTP links by default, and': '会使 Wget 默认 \\fI跟踪\\fR FTP 链接，而',
    'using \\fB\\-\\-no\\-follow\\-ftp\\fR is the only way to restore the factory': '使用 \\fB\\-\\-no\\-follow\\-ftp\\fR 是从命令行恢复出厂',
    'default from the command line.': '默认设置的唯一方法。',
}

print("Translation dictionary created, building output file...")

output_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Check if this is a pure formatting line
    stripped = line.strip()
    
    # Check exact match for translation
    if stripped in T:
        line = line.replace(stripped, T[stripped])
        output_lines.append(line)
        i += 1
        continue
    
    # Check for section_text matches
    if stripped in section_text:
        line = line.replace(stripped, section_text[stripped])
        output_lines.append(line)
        i += 1
        continue
    
    # Check if this line starts with a roff macro (keep as-is)
    if stripped.startswith('.'):
        output_lines.append(line)
        i += 1
        continue
    
    # Check if this is a verbatim/continuation line
    if stripped.startswith('\\&'):
        output_lines.append(line)
        i += 1
        continue
    
    # Check if this is a groff definition line
    if stripped.startswith('de ') or stripped.startswith('if ') or stripped.startswith('nr ') or stripped.startswith('rr ') or stripped.startswith('el') or stripped.startswith('ie ') or stripped.startswith('ds ') or stripped.startswith("'br"):
        output_lines.append(line)
        i += 1
        continue
    
    # Check for comments (lines starting with .\\\")
    if re.match(r'^\.\\"', stripped):
        output_lines.append(line)
        i += 1
        continue
    
    # For text lines, we need to translate
    # For now, output as-is (will be handled in final pass)
    output_lines.append(line)
    i += 1

with open('/tmp/man1_zh/wget.1', 'w') as f:
    f.writelines(output_lines)

print(f"Output {len(output_lines)} lines to /tmp/man1_zh/wget.1")
