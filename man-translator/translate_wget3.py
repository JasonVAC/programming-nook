#!/usr/bin/env python3
"""Translate wget man page from English to Chinese."""
import re

with open('/tmp/wget_orig.1', 'r') as f:
    content = f.read()

# ============================================================
# SECTION HEADERS
# ============================================================
rep = [
    ('.SH NAME', '.SH 名称'),
    ('.SH SYNOPSIS', '.SH 概述'),
    ('.SH DESCRIPTION', '.SH 描述'),
    ('.SH OPTIONS', '.SH 选项'),
    ('.SH EXAMPLES', '.SH 示例'),
    ('.SH AUTHOR', '.SH 作者'),
    ('.SH COPYRIGHT', '.SH 版权'),
    ('.SH "SEE ALSO"', '.SH "另请参见"'),
    ('.SH "REPORTING BUGS"', '.SH "报告错误"'),
    ('.SH ENVIRONMENT', '.SH 环境变量'),
    ('.SH "EXIT STATUS"', '.SH "退出状态"'),
    ('.SH FILES', '.SH 文件'),
    ('.SH BUGS', '.SH 错误'),
    ('IX Header "NAME"', 'IX Header "名称"'),
    ('IX Header "SYNOPSIS"', 'IX Header "概述"'),
    ('IX Header "DESCRIPTION"', 'IX Header "描述"'),
    ('IX Header "OPTIONS"', 'IX Header "选项"'),
    ('IX Header "ENVIRONMENT"', 'IX Header "环境变量"'),
    ('IX Header "EXIT STATUS"', 'IX Header "退出状态"'),
    ('IX Header "FILES"', 'IX Header "文件"'),
    ('IX Header "BUGS"', 'IX Header "错误"'),
    ('IX Header "SEE ALSO"', 'IX Header "另请参见"'),
    ('IX Header "AUTHOR"', 'IX Header "作者"'),
    ('IX Header "COPYRIGHT"', 'IX Header "版权"'),
    ('.SS "Option Syntax"', '.SS "选项语法"'),
    ('.SS "Basic Startup Options"', '.SS "基本启动选项"'),
    ('.SS "Logging and Input File Options"', '.SS "日志与输入文件选项"'),
    ('.SS "Download Options"', '.SS "下载选项"'),
    ('.SS "Directory Options"', '.SS "目录选项"'),
    ('.SS "HTTP Options"', '.SS "HTTP 选项"'),
    ('.SS "HTTPS (SSL/TLS) Options"', '.SS "HTTPS (SSL/TLS) 选项"'),
    ('.SS "FTP Options"', '.SS "FTP 选项"'),
    ('.SS "FTPS Options"', '.SS "FTPS 选项"'),
    ('.SS "Recursive Retrieval Options"', '.SS "递归下载选项"'),
    ('.SS "Recursive Accept/Reject Options"', '.SS "递归接受/拒绝选项"'),
]

for old, new in rep:
    content = content.replace(old, new)

# Preamble translations
rep2 = [
    ('Standard preamble:', '标准前言：'),
    ('de Sp " Vertical space (when we can\'t use .PP)"', 'de Sp " 垂直间距（当无法使用 .PP 时）"'),
    ('Begin verbatim text', '开始逐字文本'),
    ('End verbatim text', '结束逐字文本'),
    ('quotes in nroff, nothing in troff, for use with C<>.', 'nroff 中的引号，troff 中为空，用于 C<>。'),
    ("Escape single quotes in literal strings from groff's Unicode transform.", "转义 groff Unicode 转换中字面字符串的单引号。"),
    ("If the F register is >0, we'll generate index entries on stderr for", "若 F 寄存器 >0，则在 stderr 上为以下内容生成索引条目："),
    ('titles (.TH), headers (.SH), subsections (.SS), items (.Ip), and index', '标题 (.TH)、头部 (.SH)、子节 (.SS)、条目 (.Ip) 和索引'),
    ("entries marked with X<> in POD.  Of course, you'll have to process the", "在 POD 中标记为 X<> 的条目。当然，您需要以某种"),
    ('output yourself in some meaningful fashion.', '有意义的方式自行处理输出。'),
    ("Avoid warning from groff about undefined register 'F'.", "避免 groff 出现未定义寄存器 'F' 的警告。"),
    ('Required to disable full justification in groff 1.23.0.', '用于在 groff 1.23.0 中禁用完全对齐。'),
    ('For nroff, turn off justification.  Always turn off hyphenation; it makes', '对于 nroff，关闭对齐。始终关闭连字符；'),
    ('way too many mistakes in technical documents.', '它在技术文档中会产生太多错误。'),
]
for old, new in rep2:
    content = content.replace(old, new)

# NAME section
content = content.replace(
    'Wget \\- The non\\-interactive network downloader.',
    'Wget \\- 非交互式网络下载工具。')

# DESCRIPTION section
rep_desc = [
    (
        'GNU Wget is a free utility for non\\-interactive download of files from\n'
        'the Web.  It supports \\fBHTTP\\fR, \\fBHTTPS\\fR, and \\fBFTP\\fR protocols, as\n'
        'well as retrieval through HTTP proxies.',
        'GNU Wget 是一个免费的非交互式文件下载工具，\n'
        '可从 Web 下载文件。它支持 \\fBHTTP\\fR、\\fBHTTPS\\fR 和 \\fBFTP\\fR 协议，\n'
        '以及通过 HTTP 代理进行下载。'
    ),
    (
        'Wget is non\\-interactive, meaning that it can work in the background,\n'
        'while the user is not logged on.  This allows you to start a retrieval\n'
        'and disconnect from the system, letting Wget finish the work.  By\n'
        'contrast, most of the Web browsers require constant user\\*(Aqs presence,\n'
        'which can be a great hindrance when transferring a lot of data.',
        'Wget 是非交互式的，意味着它可以在用户未登录时在后台工作。\n'
        '这使您可以启动下载并断开与系统的连接，让 Wget 完成工作。\n'
        '相比之下，大多数 Web 浏览器需要用户持续在场，\n'
        '这在传输大量数据时可能造成很大不便。'
    ),
    (
        'Wget can follow links in \\fBHTML\\fR, \\fBXHTML\\fR, and \\fBCSS\\fR pages, to\n'
        'create local versions of remote web sites, fully recreating the\n'
        'directory structure of the original site.  This is sometimes referred to\n'
        'as "recursive downloading."  While doing that, Wget respects the Robot\n'
        'Exclusion Standard (\\fI/robots.txt\\fR).  Wget can be instructed to\n'
        'convert the links in downloaded files to point at the local files, for\n'
        'offline viewing.',
        'Wget 可以跟踪 \\fBHTML\\fR、\\fBXHTML\\fR 和 \\fBCSS\\fR 页面中的链接，\n'
        '创建远程网站的本地版本，完全重现原始网站的目录结构。\n'
        '这有时被称为"递归下载"。在下载过程中，Wget 遵守\n'
        '机器人排除标准（\\fI/robots.txt\\fR）。可以指示 Wget\n'
        '将下载文件中的链接转换为指向本地文件，以便离线查看。'
    ),
    (
        'Wget has been designed for robustness over slow or unstable network\n'
        'connections; if a download fails due to a network problem, it will\n'
        'keep retrying until the whole file has been retrieved.  If the server\n'
        'supports regetting, it will instruct the server to continue the\n'
        'download from where it left off.',
        'Wget 被设计为在缓慢或不稳定的网络连接上具有鲁棒性；\n'
        '如果下载因网络问题失败，它将不断重试，直到整个文件被下载。\n'
        '如果服务器支持断点续传，它将指示服务器从上次断开处继续下载。'
    ),
]
for old, new in rep_desc:
    content = content.replace(old, new)

# Option Syntax
rep_optsyn = [
    (
        'Since Wget uses GNU getopt to process command\\-line arguments, every\n'
        'option has a long form along with the short one.  Long options are\n'
        'more convenient to remember, but take time to type.  You may freely\n'
        'mix different option styles, or specify options after the command\\-line\n'
        'arguments.  Thus you may write:',
        '由于 Wget 使用 GNU getopt 处理命令行参数，每个选项都有长格式和短格式。\n'
        '长选项更容易记忆，但输入较慢。您可以自由混合不同的选项风格，\n'
        '或在命令行参数之后指定选项。因此可以这样写：'
    ),
    (
        'The space between the option accepting an argument and the argument may\n'
        'be omitted.  Instead of \\fB\\-o log\\fR you can write \\fB\\-olog\\fR.',
        '接受参数的选项与参数之间的空格可以省略。\n'
        '可以用 \\fB\\-olog\\fR 代替 \\fB\\-o log\\fR。'
    ),
    (
        'You may put several options that do not require arguments together,\n'
        'like:',
        '您可以将多个不需要参数的选项放在一起，\n'
        '例如：'
    ),
    ('This is completely equivalent to:', '这完全等同于：'),
    (
        'Since the options can be specified after the arguments, you may\n'
        'terminate them with \\fB\\-\\-\\fR.  So the following will try to download\n'
        'URL \\fB\\-x\\fR, reporting failure to \\fIlog\\fR:',
        '由于选项可以在参数之后指定，您可以用 \\fB\\-\\-\\fR 终止选项。\n'
        '因此以下命令将尝试下载 URL \\fB\\-x\\fR，并将失败信息报告到 \\fIlog\\fR：'
    ),
    (
        'The options that accept comma\\-separated lists all respect the convention\n'
        'that specifying an empty list clears its value.  This can be useful to\n'
        'clear the \\fI.wgetrc\\fR settings.  For instance, if your \\fI.wgetrc\\fR\n'
        'sets \\f(CW\\*(C`exclude_directories\\*(C\'\\fR to \\fI/cgi\\-bin\\fR, the following\n'
        'example will first reset it, and then set it to exclude \\fI/~nobody\\fR\n'
        'and \\fI/~somebody\\fR.  You can also clear the lists in \\fI.wgetrc\\fR.',
        '接受逗号分隔列表的选项都遵循以下约定：指定空列表会清除其值。\n'
        '这对于清除 \\fI.wgetrc\\fR 设置很有用。例如，如果您的 \\fI.wgetrc\\fR\n'
        '将 \\f(CW\\*(C`exclude_directories\\*(C\'\\fR 设置为 \\fI/cgi\\-bin\\fR，以下\n'
        '示例将首先重置它，然后设置为排除 \\fI/~nobody\\fR 和 \\fI/~somebody\\fR。\n'
        '您也可以清除 \\fI.wgetrc\\fR 中的列表。'
    ),
    (
        'Most options that do not accept arguments are \\fIboolean\\fR options,\n'
        'so named because their state can be captured with a yes\\-or\\-no\n'
        '("boolean") variable.  For example, \\fB\\-\\-follow\\-ftp\\fR tells Wget\n'
        'to follow FTP links from HTML files and, on the other hand,\n'
        '\\&\\fB\\-\\-no\\-glob\\fR tells it not to perform file globbing on FTP URLs.  A\n'
        'boolean option is either \\fIaffirmative\\fR or \\fInegative\\fR\n'
        '(beginning with \\fB\\-\\-no\\fR).  All such options share several\n'
        'properties.',
        '大多数不接受参数的选项是 \\fI布尔型\\fR 选项，\n'
        '之所以这样命名，是因为其状态可以用是或否（"布尔"）变量来表示。\n'
        '例如，\\fB\\-\\-follow\\-ftp\\fR 告诉 Wget 跟踪 HTML 文件中的 FTP 链接，\n'
        '而 \\&\\fB\\-\\-no\\-glob\\fR 告诉它不要对 FTP URL 执行文件通配。\n'
        '布尔选项要么是 \\fI肯定的\\fR 要么是 \\fI否定的\\fR\n'
        '（以 \\fB\\-\\-no\\fR 开头）。所有此类选项共享一些属性。'
    ),
    (
        'Unless stated otherwise, it is assumed that the default behavior is\n'
        'the opposite of what the option accomplishes.  For example, the\n'
        'documented existence of \\fB\\-\\-follow\\-ftp\\fR assumes that the default\n'
        'is to \\fInot\\fR follow FTP links from HTML pages.',
        '除非另有说明，默认行为被假定为选项所实现效果的反面。\n'
        '例如，文档中存在的 \\fB\\-\\-follow\\-ftp\\fR 假定默认是\n'
        '\\fI不\\fR 跟踪 HTML 页面中的 FTP 链接。'
    ),
    (
        'Affirmative options can be negated by prepending the \\fB\\-\\-no\\-\\fR to\n'
        'the option name; negative options can be negated by omitting the\n'
        '\\&\\fB\\-\\-no\\-\\fR prefix.  This might seem superfluous\\-\\-\\-if the default for\n'
        'an affirmative option is to not do something, then why provide a way\n'
        'to explicitly turn it off?  But the startup file may in fact change\n'
        'the default.  For instance, using \\f(CW\\*(C`follow_ftp = on\\*(C\'\\fR in\n'
        '\\&\\fI.wgetrc\\fR makes Wget \\fIfollow\\fR FTP links by default, and\n'
        'using \\fB\\-\\-no\\-follow\\-ftp\\fR is the only way to restore the factory\n'
        'default from the command line.',
        '肯定选项可以通过在选项名称前添加 \\fB\\-\\-no\\-\\fR 来否定；\n'
        '否定选项可以通过省略 \\fB\\-\\-no\\-\\fR 前缀来否定。\n'
        '这可能看起来多余——如果肯定选项的默认是不做某事，\n'
        '那么为什么还要提供一种显式关闭它的方法？但启动文件可能\n'
        '实际上改变了默认设置。例如，在 \\fI.wgetrc\\fR 中使用\n'
        '\\f(CW\\*(C`follow_ftp = on\\*(C\'\\fR 会使 Wget 默认 \\fI跟踪\\fR FTP 链接，\n'
        '而使用 \\fB\\-\\-no\\-follow\\-ftp\\fR 是从命令行恢复出厂默认设置的唯一方法。'
    ),
]
for old, new in rep_optsyn:
    content = content.replace(old, new)

# Basic Startup Options
rep_startup = [
    ('Display the version of Wget.', '显示 Wget 的版本。'),
    ("Print a help message describing all of Wget\\*(Aqs command\\-line options.", "打印帮助消息，描述 Wget 的所有命令行选项。"),
    (
        'Go to background immediately after startup.  If no output file is\n'
        'specified via the \\fB\\-o\\fR, output is redirected to \\fIwget\\-log\\fR.',
        '启动后立即转到后台运行。如果未通过 \\fB\\-o\\fR 指定输出文件，\n'
        '输出将重定向到 \\fIwget\\-log\\fR。'
    ),
    (
        'Execute \\fIcommand\\fR as if it were a part of \\fI.wgetrc\\fR.  A command thus invoked will be executed\n'
        '\\&\\fIafter\\fR the commands in \\fI.wgetrc\\fR, thus taking precedence over\n'
        'them.  If you need to specify more than one wgetrc command, use multiple\n'
        'instances of \\fB\\-e\\fR.',
        '将 \\fIcommand\\fR 当作 \\fI.wgetrc\\fR 的一部分来执行。\n'
        '这样调用的命令将在 \\fI.wgetrc\\fR 中的命令 \\fI之后\\fR 执行，\n'
        '因此优先级更高。如果需要指定多个 wgetrc 命令，请使用多个 \\fB\\-e\\fR 实例。'
    ),
]
for old, new in rep_startup:
    content = content.replace(old, new)

# Logging and Input File Options
rep_log = [
    (
        'Log all messages to \\fIlogfile\\fR.  The messages are normally reported\n'
        'to standard error.',
        '将所有消息记录到 \\fIlogfile\\fR。消息通常报告到标准错误输出。'
    ),
    (
        'Append to \\fIlogfile\\fR.  This is the same as \\fB\\-o\\fR, only it appends\n'
        'to \\fIlogfile\\fR instead of overwriting the old log file.  If\n'
        '\\&\\fIlogfile\\fR does not exist, a new file is created.',
        '追加到 \\fIlogfile\\fR。与 \\fB\\-o\\fR 相同，只是追加到 \\fIlogfile\\fR\n'
        '而不是覆盖旧的日志文件。如果 \\fIlogfile\\fR 不存在，则创建新文件。'
    ),
    (
        'Turn on debug output, meaning various information important to the\n'
        'developers of Wget if it does not work properly.  Your system\n'
        'administrator may have chosen to compile Wget without debug support, in\n'
        'which case \\fB\\-d\\fR will not work.  Please note that compiling with\n'
        'debug support is always safe\\-\\-\\-Wget compiled with the debug support will\n'
        '\\&\\fInot\\fR print any debug info unless requested with \\fB\\-d\\fR.',
        '开启调试输出，即 Wget 不正常工作时对开发者重要的各种信息。\n'
        '您的系统管理员可能选择在不包含调试支持的情况下编译 Wget，\n'
        '这种情况下 \\fB\\-d\\fR 将不起作用。请注意，使用调试支持编译始终是安全的——\n'
        '带有调试支持的 Wget \\fI不会\\fR 打印任何调试信息，除非使用 \\fB\\-d\\fR 请求。'
    ),
    ("Turn off Wget\\*(Aqs output.", "关闭 Wget 的输出。"),
    (
        'Turn on verbose output, with all the available data.  The default output\n'
        'is verbose.',
        '开启详细输出，包含所有可用数据。默认输出是详细模式。'
    ),
    (
        'Turn off verbose without being completely quiet (use \\fB\\-q\\fR for\n'
        'that), which means that error messages and basic information still get\n'
        'printed.',
        '关闭详细输出但不完全静默（使用 \\fB\\-q\\fR 实现完全静默），\n'
        '这意味着错误消息和基本信息仍然会被打印。'
    ),
    (
        'Output bandwidth as \\fItype\\fR.  The only accepted value is \\fBbits\\fR.',
        '以 \\fItype\\fR 格式输出带宽。唯一接受的值是 \\fBbits\\fR。'
    ),
]
for old, new in rep_log:
    content = content.replace(old, new)

with open('/tmp/man1_zh/wget.1', 'w') as f:
    f.write(content)

print("Phase 2 complete. Output written to /tmp/man1_zh/wget.1")
