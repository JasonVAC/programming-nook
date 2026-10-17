#!/usr/bin/env python3
"""
Translate wget man page from English to Chinese, preserving ALL roff formatting.
Processes line by line, translating English text while keeping roff codes intact.
"""
import re, sys

with open('/tmp/wget_orig.1', 'r') as f:
    content = f.read()

# ============================================================
# SECTION HEADERS
# ============================================================
content = content.replace('.SH NAME', '.SH 名称')
content = content.replace('.SH SYNOPSIS', '.SH 概述')
content = content.replace('.SH DESCRIPTION', '.SH 描述')
content = content.replace('.SH OPTIONS', '.SH 选项')
content = content.replace('.SH EXAMPLES', '.SH 示例')
content = content.replace('.SH AUTHOR', '.SH 作者')
content = content.replace('.SH COPYRIGHT', '.SH 版权')
content = content.replace('.SH "SEE ALSO"', '.SH "另请参见"')
content = content.replace('.SH "REPORTING BUGS"', '.SH "报告错误"')
content = content.replace('.SH ENVIRONMENT', '.SH 环境变量')
content = content.replace('.SH "EXIT STATUS"', '.SH "退出状态"')
content = content.replace('.SH FILES', '.SH 文件')
content = content.replace('.SH BUGS', '.SH 错误')

content = content.replace('IX Header "NAME"', 'IX Header "名称"')
content = content.replace('IX Header "SYNOPSIS"', 'IX Header "概述"')
content = content.replace('IX Header "DESCRIPTION"', 'IX Header "描述"')
content = content.replace('IX Header "OPTIONS"', 'IX Header "选项"')
content = content.replace('IX Header "ENVIRONMENT"', 'IX Header "环境变量"')
content = content.replace('IX Header "EXIT STATUS"', 'IX Header "退出状态"')
content = content.replace('IX Header "FILES"', 'IX Header "文件"')
content = content.replace('IX Header "BUGS"', 'IX Header "错误"')
content = content.replace('IX Header "SEE ALSO"', 'IX Header "另请参见"')
content = content.replace('IX Header "AUTHOR"', 'IX Header "作者"')
content = content.replace('IX Header "COPYRIGHT"', 'IX Header "版权"')

# ============================================================
# SUBSECTION HEADERS
# ============================================================
content = content.replace('.SS "Option Syntax"', '.SS "选项语法"')
content = content.replace('.SS "Basic Startup Options"', '.SS "基本启动选项"')
content = content.replace('.SS "Logging and Input File Options"', '.SS "日志与输入文件选项"')
content = content.replace('.SS "Download Options"', '.SS "下载选项"')
content = content.replace('.SS "Directory Options"', '.SS "目录选项"')
content = content.replace('.SS "HTTP Options"', '.SS "HTTP 选项"')
content = content.replace('.SS "HTTPS (SSL/TLS) Options"', '.SS "HTTPS (SSL/TLS) 选项"')
content = content.replace('.SS "FTP Options"', '.SS "FTP 选项"')
content = content.replace('.SS "FTPS Options"', '.SS "FTPS 选项"')
content = content.replace('.SS "Recursive Retrieval Options"', '.SS "递归下载选项"')
content = content.replace('.SS "Recursive Accept/Reject Options"', '.SS "递归接受/拒绝选项"')

# ============================================================
# COMMENTS
# ============================================================
content = content.replace('Standard preamble:', '标准前言：')
content = content.replace("Vertical space (when we can\\'t use .PP)", "垂直间距（当无法使用 .PP 时）")
content = content.replace('Begin verbatim text', '开始逐字文本')
content = content.replace('End verbatim text', '结束逐字文本')
content = content.replace('quotes in nroff, nothing in troff, for use with C<>.', 'nroff 中的引号，troff 中为空，用于 C<>。')
content = content.replace("Escape single quotes in literal strings from groff\\'s Unicode transform.", "转义 groff Unicode 转换中字面字符串的单引号。")
content = content.replace("If the F register is >0, we\\'ll generate index entries on stderr for", "若 F 寄存器 >0，则在 stderr 上为以下内容生成索引条目：")
content = content.replace('titles (.TH), headers (.SH), subsections (.SS), items (.Ip), and index', '标题 (.TH)、头部 (.SH)、子节 (.SS)、条目 (.Ip) 和索引')
content = content.replace('entries marked with X<> in POD.  Of course, you\\'ll have to process the', '在 POD 中标记为 X<> 的条目。当然，您需要以某种')
content = content.replace('output yourself in some meaningful fashion.', '有意义的方式自行处理输出。')
content = content.replace("Avoid warning from groff about undefined register \\'F\\'.", "避免 groff 出现未定义寄存器 \\'F\\' 的警告。")
content = content.replace('Required to disable full justification in groff 1.23.0.', '用于在 groff 1.23.0 中禁用完全对齐。')
content = content.replace('For nroff, turn off justification.  Always turn off hyphenation; it makes', '对于 nroff，关闭对齐。始终关闭连字符；')
content = content.replace('way too many mistakes in technical documents.', '它在技术文档中会产生太多错误。')

# ============================================================
# NAME section
# ============================================================
content = content.replace(
    'Wget \\- The non\\-interactive network downloader.',
    'Wget \\- 非交互式网络下载工具。')

# ============================================================
# DESCRIPTION section - line by line
# ============================================================
# First paragraph
old_desc_p1 = (
    'GNU Wget is a free utility for non\\-interactive download of files from\n'
    'the Web.  It supports \\fBHTTP\\fR, \\fBHTTPS\\fR, and \\fBFTP\\fR protocols, as\n'
    'well as retrieval through HTTP proxies.')
new_desc_p1 = (
    'GNU Wget 是一个免费的非交互式文件下载工具，\n'
    '可从 Web 下载文件。它支持 \\fBHTTP\\fR、\\fBHTTPS\\fR 和 \\fBFTP\\fR 协议，\n'
    '以及通过 HTTP 代理进行下载。')
content = content.replace(old_desc_p1, new_desc_p1)

old_desc_p2 = (
    'Wget is non\\-interactive, meaning that it can work in the background,\n'
    'while the user is not logged on.  This allows you to start a retrieval\n'
    'and disconnect from the system, letting Wget finish the work.  By\n'
    'contrast, most of the Web browsers require constant user\\*(Aqs presence,\n'
    'which can be a great hindrance when transferring a lot of data.')
new_desc_p2 = (
    'Wget 是非交互式的，意味着它可以在用户未登录时在后台工作。\n'
    '这使您可以启动下载并断开与系统的连接，让 Wget 完成工作。\n'
    '相比之下，大多数 Web 浏览器需要用户持续在场，\n'
    '这在传输大量数据时可能造成很大不便。')
content = content.replace(old_desc_p2, new_desc_p2)

old_desc_p3 = (
    'Wget can follow links in \\fBHTML\\fR, \\fBXHTML\\fR, and \\fBCSS\\fR pages, to\n'
    'create local versions of remote web sites, fully recreating the\n'
    'directory structure of the original site.  This is sometimes referred to\n'
    'as "recursive downloading."  While doing that, Wget respects the Robot\n'
    'Exclusion Standard (\\fI/robots.txt\\fR).  Wget can be instructed to\n'
    'convert the links in downloaded files to point at the local files, for\n'
    'offline viewing.')
new_desc_p3 = (
    'Wget 可以跟踪 \\fBHTML\\fR、\\fBXHTML\\fR 和 \\fBCSS\\fR 页面中的链接，\n'
    '创建远程网站的本地版本，完全重现原始网站的目录结构。\n'
    '这有时被称为"递归下载"。在下载过程中，Wget 遵守\n'
    '机器人排除标准（\\fI/robots.txt\\fR）。可以指示 Wget\n'
    '将下载文件中的链接转换为指向本地文件，以便离线查看。')
content = content.replace(old_desc_p3, new_desc_p3)

old_desc_p4 = (
    'Wget has been designed for robustness over slow or unstable network\n'
    'connections; if a download fails due to a network problem, it will\n'
    'keep retrying until the whole file has been retrieved.  If the server\n'
    'supports regetting, it will instruct the server to continue the\n'
    'download from where it left off.')
new_desc_p4 = (
    'Wget 被设计为在缓慢或不稳定的网络连接上具有鲁棒性；\n'
    '如果下载因网络问题失败，它将不断重试，直到整个文件被下载。\n'
    '如果服务器支持断点续传，它将指示服务器从上次断开处继续下载。')
content = content.replace(old_desc_p4, new_desc_p4)

# ============================================================
# OPTIONS section
# ============================================================

# Option Syntax
old_optsyn1 = (
    'Since Wget uses GNU getopt to process command\\-line arguments, every\n'
    'option has a long form along with the short one.  Long options are\n'
    'more convenient to remember, but take time to type.  You may freely\n'
    'mix different option styles, or specify options after the command\\-line\n'
    'arguments.  Thus you may write:')
new_optsyn1 = (
    '由于 Wget 使用 GNU getopt 处理命令行参数，每个选项都有长格式和短格式。\n'
    '长选项更容易记忆，但输入较慢。您可以自由混合不同的选项风格，\n'
    '或在命令行参数之后指定选项。因此可以这样写：')
content = content.replace(old_optsyn1, new_optsyn1)

old_optsyn2 = (
    'The space between the option accepting an argument and the argument may\n'
    'be omitted.  Instead of \\fB\\-o log\\fR you can write \\fB\\-olog\\fR.')
new_optsyn2 = (
    '接受参数的选项与参数之间的空格可以省略。\n'
    '可以用 \\fB\\-olog\\fR 代替 \\fB\\-o log\\fR。')
content = content.replace(old_optsyn2, new_optsyn2)

old_optsyn3 = (
    'You may put several options that do not require arguments together,\n'
    'like:')
new_optsyn3 = (
    '您可以将多个不需要参数的选项放在一起，\n'
    '例如：')
content = content.replace(old_optsyn3, new_optsyn3)

content = content.replace('This is completely equivalent to:', '这完全等同于：')

old_optsyn4 = (
    'Since the options can be specified after the arguments, you may\n'
    'terminate them with \\fB\\-\\-\\fR.  So the following will try to download\n'
    'URL \\fB\\-x\\fR, reporting failure to \\fIlog\\fR:')
new_optsyn4 = (
    '由于选项可以在参数之后指定，您可以用 \\fB\\-\\-\\fR 终止选项。\n'
    '因此以下命令将尝试下载 URL \\fB\\-x\\fR，并将失败信息报告到 \\fIlog\\fR：')
content = content.replace(old_optsyn4, new_optsyn4)

old_optsyn5 = (
    'The options that accept comma\\-separated lists all respect the convention\n'
    'that specifying an empty list clears its value.  This can be useful to\n'
    'clear the \\fI.wgetrc\\fR settings.  For instance, if your \\fI.wgetrc\\fR\n'
    'sets \\f(CW\\*(C`exclude_directories\\*(C\\'\\fR to \\fI/cgi\\-bin\\fR, the following\n'
    'example will first reset it, and then set it to exclude \\fI/~nobody\\fR\n'
    'and \\fI/~somebody\\fR.  You can also clear the lists in \\fI.wgetrc\\fR.')
new_optsyn5 = (
    '接受逗号分隔列表的选项都遵循以下约定：指定空列表会清除其值。\n'
    '这对于清除 \\fI.wgetrc\\fR 设置很有用。例如，如果您的 \\fI.wgetrc\\fR\n'
    '将 \\f(CW\\*(C`exclude_directories\\*(C\\'\\fR 设置为 \\fI/cgi\\-bin\\fR，以下\n'
    '示例将首先重置它，然后设置为排除 \\fI/~nobody\\fR 和 \\fI/~somebody\\fR。\n'
    '您也可以清除 \\fI.wgetrc\\fR 中的列表。')
content = content.replace(old_optsyn5, new_optsyn5)

old_optsyn6 = (
    'Most options that do not accept arguments are \\fIboolean\\fR options,\n'
    'so named because their state can be captured with a yes\\-or\\-no\n'
    '("boolean") variable.  For example, \\fB\\-\\-follow\\-ftp\\fR tells Wget\n'
    'to follow FTP links from HTML files and, on the other hand,\n'
    '\\&\\fB\\-\\-no\\-glob\\fR tells it not to perform file globbing on FTP URLs.  A\n'
    'boolean option is either \\fIaffirmative\\fR or \\fInegative\\fR\n'
    '(beginning with \\fB\\-\\-no\\fR).  All such options share several\n'
    'properties.')
new_optsyn6 = (
    '大多数不接受参数的选项是 \\fI布尔型\\fR 选项，\n'
    '之所以这样命名，是因为其状态可以用是或否（"布尔"）变量来表示。\n'
    '例如，\\fB\\-\\-follow\\-ftp\\fR 告诉 Wget 跟踪 HTML 文件中的 FTP 链接，\n'
    '而 \\&\\fB\\-\\-no\\-glob\\fR 告诉它不要对 FTP URL 执行文件通配。\n'
    '布尔选项要么是 \\fI肯定的\\fR 要么是 \\fI否定的\\fR\n'
    '（以 \\fB\\-\\-no\\fR 开头）。所有此类选项共享一些属性。')
content = content.replace(old_optsyn6, new_optsyn6)

old_optsyn7 = (
    'Unless stated otherwise, it is assumed that the default behavior is\n'
    'the opposite of what the option accomplishes.  For example, the\n'
    'documented existence of \\fB\\-\\-follow\\-ftp\\fR assumes that the default\n'
    'is to \\fInot\\fR follow FTP links from HTML pages.')
new_optsyn7 = (
    '除非另有说明，默认行为被假定为选项所实现效果的反面。\n'
    '例如，文档中存在的 \\fB\\-\\-follow\\-ftp\\fR 假定默认是\n'
    '\\fI不\\fR 跟踪 HTML 页面中的 FTP 链接。')
content = content.replace(old_optsyn7, new_optsyn7)

old_optsyn8 = (
    'Affirmative options can be negated by prepending the \\fB\\-\\-no\\-\\fR to\n'
    'the option name; negative options can be negated by omitting the\n'
    '\\&\\fB\\-\\-no\\-\\fR prefix.  This might seem superfluous\\-\\-\\-if the default for\n'
    'an affirmative option is to not do something, then why provide a way\n'
    'to explicitly turn it off?  But the startup file may in fact change\n'
    'the default.  For instance, using \\f(CW\\*(C`follow_ftp = on\\*(C\\'\\fR in\n'
    '\\&\\fI.wgetrc\\fR makes Wget \\fIfollow\\fR FTP links by default, and\n'
    'using \\fB\\-\\-no\\-follow\\-ftp\\fR is the only way to restore the factory\n'
    'default from the command line.')
new_optsyn8 = (
    '肯定选项可以通过在选项名称前添加 \\fB\\-\\-no\\-\\fR 来否定；\n'
    '否定选项可以通过省略 \\fB\\-\\-no\\-\\fR 前缀来否定。\n'
    '这可能看起来多余——如果肯定选项的默认是不做某事，\n'
    '那么为什么还要提供一种显式关闭它的方法？但启动文件可能\n'
    '实际上改变了默认设置。例如，在 \\fI.wgetrc\\fR 中使用\n'
    '\\f(CW\\*(C`follow_ftp = on\\*(C\\'\\fR 会使 Wget 默认 \\fI跟踪\\fR FTP 链接，\n'
    '而使用 \\fB\\-\\-no\\-follow\\-ftp\\fR 是从命令行恢复出厂默认设置的唯一方法。')
content = content.replace(old_optsyn8, new_optsyn8)

# Basic Startup Options
old_startup1 = (
    'Display the version of Wget.')
new_startup1 = (
    '显示 Wget 的版本。')
content = content.replace(old_startup1, new_startup1)

old_startup2 = (
    'Print a help message describing all of Wget\\*(Aqs command\\-line options.')
new_startup2 = (
    '打印帮助消息，描述所有 Wget 的命令行选项。')
content = content.replace(old_startup2, new_startup2)

old_startup3 = (
    'Go to background immediately after startup.  If no output file is\n'
    'specified via the \\fB\\-o\\fR, output is redirected to \\fIwget\\-log\\fR.')
new_startup3 = (
    '启动后立即转到后台运行。如果未通过 \\fB\\-o\\fR 指定输出文件，\n'
    '输出将重定向到 \\fIwget\\-log\\fR。')
content = content.replace(old_startup3, new_startup3)

old_startup4 = (
    'Execute \\fIcommand\\fR as if it were a part of \\fI.wgetrc\\fR.  A command thus invoked will be executed\n'
    '\\&\\fIafter\\fR the commands in \\fI.wgetrc\\fR, thus taking precedence over\n'
    'them.  If you need to specify more than one wgetrc command, use multiple\n'
    'instances of \\fB\\-e\\fR.')
new_startup4 = (
    '将 \\fIcommand\\fR 当作 \\fI.wgetrc\\fR 的一部分来执行。\n'
    '这样调用的命令将在 \\fI.wgetrc\\fR 中的命令 \\fI之后\\fR 执行，\n'
    '因此优先级更高。如果需要指定多个 wgetrc 命令，请使用多个 \\fB\\-e\\fR 实例。')
content = content.replace(old_startup4, new_startup4)

# Logging and Input File Options
old_log1 = (
    'Log all messages to \\fIlogfile\\fR.  The messages are normally reported\n'
    'to standard error.')
new_log1 = (
    '将所有消息记录到 \\fIlogfile\\fR。消息通常报告到标准错误输出。')
content = content.replace(old_log1, new_log1)

old_log2 = (
    'Append to \\fIlogfile\\fR.  This is the same as \\fB\\-o\\fR, only it appends\n'
    'to \\fIlogfile\\fR instead of overwriting the old log file.  If\n'
    '\\&\\fIlogfile\\fR does not exist, a new file is created.')
new_log2 = (
    '追加到 \\fIlogfile\\fR。与 \\fB\\-o\\fR 相同，只是追加到 \\fIlogfile\\fR\n'
    '而不是覆盖旧的日志文件。如果 \\fIlogfile\\fR 不存在，则创建新文件。')
content = content.replace(old_log2, new_log2)

old_log3 = (
    'Turn on debug output, meaning various information important to the\n'
    'developers of Wget if it does not work properly.  Your system\n'
    'administrator may have chosen to compile Wget without debug support, in\n'
    'which case \\fB\\-d\\fR will not work.  Please note that compiling with\n'
    'debug support is always safe\\-\\-\\-Wget compiled with the debug support will\n'
    '\\&\\fInot\\fR print any debug info unless requested with \\fB\\-d\\fR.')
new_log3 = (
    '开启调试输出，即 Wget 不正常工作时对开发者重要的各种信息。\n'
    '您的系统管理员可能选择在不包含调试支持的情况下编译 Wget，\n'
    '这种情况下 \\fB\\-d\\fR 将不起作用。请注意，使用调试支持编译始终是安全的——\n'
    '带有调试支持的 Wget \\fI不会\\fR 打印任何调试信息，除非使用 \\fB\\-d\\fR 请求。')
content = content.replace(old_log3, new_log3)

old_log4 = "Turn off Wget\\*(Aqs output."
new_log4 = "关闭 Wget 的输出。"
content = content.replace(old_log4, new_log4)

old_log5 = (
    'Turn on verbose output, with all the available data.  The default output\n'
    'is verbose.')
new_log5 = (
    '开启详细输出，包含所有可用数据。默认输出是详细模式。')
content = content.replace(old_log5, new_log5)

old_log6 = (
    'Turn off verbose without being completely quiet (use \\fB\\-q\\fR for\n'
    'that), which means that error messages and basic information still get\n'
    'printed.')
new_log6 = (
    '关闭详细输出但不完全静默（使用 \\fB\\-q\\fR 实现完全静默），\n'
    '这意味着错误消息和基本信息仍然会被打印。')
content = content.replace(old_log6, new_log6)

old_log7 = (
    'Output bandwidth as \\fItype\\fR.  The only accepted value is \\fBbits\\fR.')
new_log7 = (
    '以 \\fItype\\fR 格式输出带宽。唯一接受的值是 \\fBbits\\fR。')
content = content.replace(old_log7, new_log7)

old_log8 = (
    'Read URLs from a local or external \\fIfile\\fR.  If \\fB\\-\\fR is\n'
    'specified as \\fIfile\\fR, URLs are read from the standard input.  \n'
    '(Use \\fB./\\-\\fR to read from a file literally named \\fB\\-\\fR.)\n'
    '.Sp\n'
    'If this function is used, no URLs need be present on the command\n'
    'line.  If there are URLs both on the command line and in an input\n'
    'file, those on the command lines will be the first ones to be\n'
    'retrieved.  If \\fB\\-\\-force\\-html\\fR is not specified, then \\fIfile\\fR\n'
    'should consist of a series of URLs, one per line.\n'
    '.Sp\n'
    'However, if you specify \\fB\\-\\-force\\-html\\fR, the document will be\n'
    'regarded as \\fBhtml\\fR.  In that case you may have problems with\n'
    'relative links, which you can solve either by adding \\f(CW\\*(C`<base\n'
    'href="\\fR\\f(CIurl\\fR\\f(CW">\\*(C\\'\\fR to the documents or by specifying\n'
    '\\&\\fB\\-\\-base=\\fR\\fIurl\\fR on the command line.\n'
    '.Sp\n'
    'If the \\fIfile\\fR is an external one, the document will be automatically\n'
    'treated as \\fBhtml\\fR if the Content\\-Type matches \\fBtext/html\\fR.\n'
    'Furthermore, the \\fIfile\\fR\\*(Aqs location will be implicitly used as base\n'
    'href if none was specified.\n'
    '.Sp\n'
    'If the \\fIfile\\fR is a local file, on systems that support it, it will be\n'
    'opened with the \\f(CW\\*(C`O_NONBLOCK\\*(C\\'\\fR flag to allow non\\-blocking reads from the\n'
    'file. \\fBWget\\fR will attempt to continue reading from the file until\n'
    'EOF is reached or it is closed. This allows one to stream a list of files\n'
    'for retrieval where the list is dynamically generated during the execution\n'
    'of the process. Currently, this feature is not available on Windows platforms.')
new_log8 = (
    '从本地或外部 \\fIfile\\fR 读取 URL。如果 \\fB\\-\\fR 被指定为\n'
    '\\fIfile\\fR，则从标准输入读取 URL。\n'
    '（使用 \\fB./\\-\\fR 从字面名为 \\fB\\-\\fR 的文件读取。）\n'
    '.Sp\n'
    '如果使用此功能，命令行上不需要出现 URL。\n'
    '如果命令行和输入文件中都有 URL，命令行中的 URL 将首先被下载。\n'
    '如果未指定 \\fB\\-\\-force\\-html\\fR，则 \\fIfile\\fR 应包含一系列 URL，每行一个。\n'
    '.Sp\n'
    '但是，如果指定了 \\fB\\-\\-force\\-html\\fR，文档将被视为 \\fBhtml\\fR。\n'
    '这种情况下可能会遇到相对链接的问题，可以通过在文档中添加\n'
    '\\f(CW\\*(C`<base href="\\fR\\f(CIurl\\fR\\f(CW">\\*(C\\'\\fR 或在命令行上指定\n'
    '\\&\\fB\\-\\-base=\\fR\\fIurl\\fR 来解决。\n'
    '.Sp\n'
    '如果 \\fIfile\\fR 是外部文件，且 Content\\-Type 匹配 \\fBtext/html\\fR，\n'
    '文档将自动被视为 \\fBhtml\\fR。此外，如果未指定 base href，\n'
    '\\fIfile\\fR 的位置将隐式用作基准 URL。\n'
    '.Sp\n'
    '如果 \\fIfile\\fR 是本地文件，在支持的系统上，将使用\n'
    '\\f(CW\\*(C`O_NONBLOCK\\*(C\\'\\fR 标志打开以允许非阻塞读取。\n'
    '\\fBWget\\fR 将尝试继续从文件中读取，直到达到 EOF 或文件关闭。\n'
    '这允许流式传输动态生成的文件列表进行下载。\n'
    '目前，此功能在 Windows 平台上不可用。')
content = content.replace(old_log8, new_log8)

old_log9 = (
    'Downloads files covered in local Metalink \\fIfile\\fR. Metalink version 3\n'
    'and 4 are supported.')
new_log9 = (
    '下载本地 Metalink \\fIfile\\fR 中涵盖的文件。支持 Metalink 版本 3 和 4。')
content = content.replace(old_log9, new_log9)

old_log10 = (
    'Keeps downloaded Metalink\\*(Aqs files with a bad hash. It appends .badhash\n'
    'to the name of Metalink\\*(Aqs files which have a checksum mismatch, except\n'
    'without overwriting existing files.')
new_log10 = (
    '保留校验和不匹配的 Metalink 下载文件。它在校验和不匹配的 Metalink\n'
    '文件名后添加 .badhash 后缀，但不会覆盖现有文件。')
content = content.replace(old_log10, new_log10)

old_log11 = (
    'Issues HTTP HEAD request instead of GET and extracts Metalink metadata\n'
    'from response headers. Then it switches to Metalink download.\n'
    'If no valid Metalink metadata is found, it falls back to ordinary HTTP download.\n'
    'Enables \\fBContent\\-Type: application/metalink4+xml\\fR files download/processing.')
new_log11 = (
    '发出 HTTP HEAD 请求而非 GET，并从响应头中提取 Metalink 元数据。\n'
    '然后切换到 Metalink 下载。如果未找到有效的 Metalink 元数据，\n'
    '则回退到普通 HTTP 下载。\n'
    '启用 \\fBContent\\-Type: application/metalink4+xml\\fR 文件的下载/处理。')
content = content.replace(old_log11, new_log11)

old_log12 = (
    'Set the Metalink \\fBapplication/metalink4+xml\\fR metaurl ordinal\n'
    'NUMBER. From 1 to the total number of "application/metalink4+xml"')
new_log12 = (
    '设置 Metalink \\fBapplication/metalink4+xml\\fR 元 URL 序号\n'
    'NUMBER。从 1 到 "application/metalink4+xml" 的总数。')
content = content.replace(old_log12, new_log12)

old_log12b = (
    'available.  Specify 0 or \\fBinf\\fR to choose the first good one.\n'
    'Metaurls, such as those from a \\fB\\-\\-metalink\\-over\\-http\\fR, may have\n'
    'been sorted by priority key\\*(Aqs value; keep this in mind to choose the\n'
    'right NUMBER.')
new_log12b = (
    '指定 0 或 \\fBinf\\fR 可选择第一个可用的。\n'
    '元 URL（例如来自 \\fB\\-\\-metalink\\-over\\-http\\fR 的）可能已按优先级键值排序；\n'
    '在选择正确的 NUMBER 时请记住这一点。')
content = content.replace(old_log12b, new_log12b)

old_log13 = (
    'Set preferred location for Metalink resources. This has effect if multiple\n'
    'resources with same priority are available.')
new_log13 = (
    '设置 Metalink 资源的首选位置。当存在多个具有相同优先级的资源时生效。')
content = content.replace(old_log13, new_log13)

old_log14 = (
    'Enable use of file system\\*(Aqs extended attributes to save the\n'
    'original URL and the Referer HTTP header value if used.\n'
    '.Sp\n'
    'Be aware that the URL might contain private information like\n'
    'access tokens or credentials.')
new_log14 = (
    '启用文件系统的扩展属性来保存原始 URL 和 Referer HTTP 头值（如果使用的话）。\n'
    '.Sp\n'
    '请注意，URL 可能包含访问令牌或凭据等私密信息。')
content = content.replace(old_log14, new_log14)

old_log15 = (
    'When input is read from a file, force it to be treated as an HTML\n'
    'file.  This enables you to retrieve relative links from existing\n'
    'HTML files on your local disk, by adding \\f(CW\\*(C`<base\n'
    'href="\\fR\\f(CIurl\\fR\\f(CW">\\*(C\\'\\fR to HTML, or using the \\fB\\-\\-base\\fR command\\-line\n'
    'option.')
new_log15 = (
    '当从文件读取输入时，强制将其视为 HTML 文件。\n'
    '这使您可以通过在 HTML 中添加 \\f(CW\\*(C`<base href="\\fR\\f(CIurl\\fR\\f(CW">\\*(C\\'\\fR\n'
    '或使用 \\fB\\-\\-base\\fR 命令行选项，从本地磁盘上现有 HTML 文件中获取相对链接。')
content = content.replace(old_log15, new_log15)

old_log16 = (
    'Resolves relative links using \\fIURL\\fR as the point of reference,\n'
    'when reading links from an HTML file specified via the\n'
    '\\&\\fB\\-i\\fR/\\fB\\-\\-input\\-file\\fR option (together with\n'
    '\\&\\fB\\-\\-force\\-html\\fR, or when the input file was fetched remotely from\n'
    'a server describing it as HTML). This is equivalent to the\n'
    'presence of a \\f(CW\\*(C`BASE\\*(C\\'\\fR tag in the HTML input file, with\n'
    '\\&\\fIURL\\fR as the value for the \\f(CW\\*(C`href\\*(C\\'\\fR attribute.')
new_log16 = (
    '使用 \\fIURL\\fR 作为参考点解析相对链接，\n'
    '当通过 \\fB\\-i\\fR/\\fB\\-\\-input\\-file\\fR 选项（配合\n'
    '\\fB\\-\\-force\\-html\\fR，或输入文件是从服务器远程获取并描述为 HTML 时）\n'
    '从 HTML 文件读取链接时使用。这相当于在 HTML 输入文件中存在\n'
    '\\f(CW\\*(C`BASE\\*(C\\'\\fR 标签，其 \\f(CW\\*(C`href\\*(C\\'\\fR 属性值为 \\fIURL\\fR。')
content = content.replace(old_log16, new_log16)

old_log17 = (
    'For instance, if you specify \\fBhttp://foo/bar/a.html\\fR for\n'
    '\\&\\fIURL\\fR, and Wget reads \\fB../baz/b.html\\fR from the input file, it\n'
    'would be resolved to \\fBhttp://foo/baz/b.html\\fR.')
new_log17 = (
    '例如，如果为 \\fIURL\\fR 指定 \\fBhttp://foo/bar/a.html\\fR，\n'
    '并且 Wget 从输入文件中读取 \\fB../baz/b.html\\fR，\n'
    '它将被解析为 \\fBhttp://foo/baz/b.html\\fR。')
content = content.replace(old_log17, new_log17)

old_log18 = (
    'Specify the location of a startup file you wish to use instead of the\n'
    'default one(s). Use \\-\\-no\\-config to disable reading of config files.\n'
    'If both \\-\\-config and \\-\\-no\\-config are given, \\-\\-no\\-config is ignored.')
new_log18 = (
    '指定要使用的启动文件位置，代替默认文件。使用 \\-\\-no\\-config 禁用配置文件读取。\n'
    '如果同时给出 \\-\\-config 和 \\-\\-no\\-config，\\-\\-no\\-config 将被忽略。')
content = content.replace(old_log18, new_log18)

old_log19 = (
    'Logs all URL rejections to \\fIlogfile\\fR as comma separated values.  The values\n'
    'include the reason of rejection, the URL and the parent URL it was found in.')
new_log19 = (
    '将所有 URL 拒绝记录以逗号分隔值的形式记录到 \\fIlogfile\\fR。\n'
    '这些值包括拒绝原因、URL 以及发现该 URL 的父级 URL。')
content = content.replace(old_log19, new_log19)

# ============================================================
# Download Options
# ============================================================
old_dl1 = (
    'When making client TCP/IP connections, bind to \\fIADDRESS\\fR on\n'
    'the local machine.  \\fIADDRESS\\fR may be specified as a hostname or IP\n'
    'address.  This option can be useful if your machine is bound to multiple\n'
    'IPs.')
new_dl1 = (
    '建立客户端 TCP/IP 连接时，绑定到本地机器上的 \\fIADDRESS\\fR。\n'
    '\\fIADDRESS\\fR 可指定为主机名或 IP 地址。\n'
    '如果您的机器绑定了多个 IP，此选项会很有用。')
content = content.replace(old_dl1, new_dl1)

old_dl2 = (
    '[libcares only]\n'
    'This address overrides the route for DNS requests. If you ever need to\n'
    'circumvent the standard settings from /etc/resolv.conf, this option together\n'
    'with \\fB\\-\\-dns\\-servers\\fR is your friend.\n'
    '\\&\\fIADDRESS\\fR must be specified either as IPv4 or IPv6 address.\n'
    'Wget needs to be built with libcares for this option to be available.')
new_dl2 = (
    '[仅限 libcares]\n'
    '此地址覆盖 DNS 请求的路由。如果需要绕过 /etc/resolv.conf 中的标准设置，\n'
    '此选项与 \\fB\\-\\-dns\\-servers\\fR 配合使用即可。\n'
    '\\&\\fIADDRESS\\fR 必须指定为 IPv4 或 IPv6 地址。\n'
    'Wget 需要使用 libcares 编译才能使此选项可用。')
content = content.replace(old_dl2, new_dl2)

old_dl3 = (
    '[libcares only]\n'
    'The given address(es) override the standard nameserver\n'
    'addresses,  e.g. as configured in /etc/resolv.conf.\n'
    '\\&\\fIADDRESSES\\fR may be specified either as IPv4 or IPv6 addresses,\n'
    'comma\\-separated.\n'
    'Wget needs to be built with libcares for this option to be available.')
new_dl3 = (
    '[仅限 libcares]\n'
    '给定的地址覆盖标准名称服务器地址，\n'
    '例如 /etc/resolv.conf 中配置的地址。\n'
    '\\&\\fIADDRESSES\\fR 可指定为 IPv4 或 IPv6 地址，以逗号分隔。\n'
    'Wget 需要使用 libcares 编译才能使此选项可用。')
content = content.replace(old_dl3, new_dl3)

old_dl4 = (
    'Set number of tries to \\fInumber\\fR. Specify 0 or \\fBinf\\fR for\n'
    'infinite retrying.  The default is to retry 20 times, with the exception\n'
    'of fatal errors like "connection refused" or "not found" (404),\n'
    'which are not retried.')
new_dl4 = (
    '将重试次数设置为 \\fInumber\\fR。指定 0 或 \\fBinf\\fR 可无限重试。\n'
    '默认重试 20 次，但致命错误（如"连接被拒绝"或"未找到"(404)）除外，\n'
    '这些错误不会重试。')
content = content.replace(old_dl4, new_dl4)

# Save the intermediate result
with open('/tmp/man1_zh/wget.1', 'w') as f:
    f.write(content)

print("Phase 1 complete. Intermediate file written.")
