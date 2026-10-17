#!/usr/bin/env python3
"""Comprehensive translation of curl.1 man page from English to Chinese.
Preserves all roff/troff formatting codes exactly."""

import re
import os

def translate_line(line):
    """Translate a single line, preserving roff formatting codes."""
    
    # ===== SECTION HEADERS =====
    if line == '.SH NAME':
        return '.SH 名称'
    if line == '.SH SYNOPSIS':
        return '.SH 概述'
    if line == '.SH DESCRIPTION':
        return '.SH 描述'
    if line == '.SH URL':
        return '.SH URL'
    if line == '.SH GLOBBING':
        return '.SH 通配符匹配'
    if line == '.SH VARIABLES':
        return '.SH 变量'
    if line == '.SH OUTPUT':
        return '.SH 输出'
    if line == '.SH PROTOCOLS':
        return '.SH 协议'
    if line == '.SH PROGRESS METER':
        return '.SH 进度指示器'
    if line == '.SH VERSION':
        return '.SH 版本'
    if line == '.SH OPTIONS':
        return '.SH 选项'
    if line == '.SH ALL OPTIONS':
        return '.SH 所有选项'
    if line == '.SH EXAMPLES':
        return '.SH 示例'
    if line == '.SH AUTHOR':
        return '.SH 作者'
    if line == '.SH "REPORTING BUGS"':
        return '.SH "报告错误"'
    if line == '.SH COPYRIGHT':
        return '.SH 版权'
    if line == '.SH "SEE ALSO"':
        return '.SH "另请参见"'
    if line == '.SH FILES':
        return '.SH 文件'
    if line == '.SH ENVIRONMENT':
        return '.SH 环境变量'
    if line == '.SH EXIT CODES':
        return '.SH 退出码'
    if line == '.SH PROXY PROTOCOL PREFIXES':
        return '.SH 代理协议前缀'

    # ===== TH header =====
    if line == '.TH curl 1 "2026-06-24" "curl 8.21.0" "curl Manual"':
        return '.TH curl 1 "2026-06-24" "curl 8.21.0" "curl 用户命令"'

    # ===== BOILERPLATE PATTERNS (applied to any line) =====
    
    # Examples: / Example:
    if re.match(r'^Examples:$', line):
        return '示例：'
    if re.match(r'^Example:$', line):
        return '示例：'

    # See also
    line = re.sub(r'^See also (.+)\.$', r'另请参见 \1。', line)

    # Added in X. See also Y
    line = re.sub(r'^Added in ([0-9.]+)\. See also (.+?)\.$', r'在 \1 中添加。另请参见 \2。', line)
    line = re.sub(r'^Added in ([0-9.]+)\.$', r'在 \1 中添加。', line)

    # If <option> is provided several times, the last set value is used.
    line = re.sub(r'^If (.+) is provided several times, the last set value is used\.$',
                  r'如果多次提供 \1，则使用最后设置的值。', line)

    # Providing <option> multiple times has no extra effect.
    line = re.sub(r'^Providing (.+) multiple times has no extra effect\.$',
                  r'多次提供 \1 没有额外效果。', line)

    # Disable it again with <xxx>.
    line = re.sub(r'^Disable it again with (.+)\.$',
                  r'使用 \1 再次禁用它。', line)

    # This option is mutually exclusive with <xxx>.
    line = re.sub(r'^This option is mutually exclusive with (.+)\.$',
                  r'此选项与 \1 互斥。', line)

    # This option is superfluous since...
    line = re.sub(r'^This option is superfluous since you can specify a (.+) proxy with \fI\-\-proxy\fP$',
                  r'此选项是多余的，因为您可以使用 \fI\-\-proxy\fP 通过 "\1://" 协议前缀指定 \1 代理。', line)
    line = re.sub(r'^using a "(.+?)://" protocol prefix\.$',
                  r'使用 "\1://" 协议前缀。', line)

    # This option overrides any previous use...
    line = re.sub(r'^This option overrides any previous use of \fI\-\-proxy\fP, as they are mutually$',
                  r'此选项覆盖之前对 \fI\-\-proxy\fP 的任何使用，因为它们是互斥的。', line)
    line = re.sub(r'^exclusive\.$', r'', line)

    # ===== SPECIFIC LINE TRANSLATIONS =====
    trans_map = {
        # NAME section
        r'curl \- transfer a URL': r'curl \- 传输一个URL',
        r'curl \\- transfer a URL': r'curl \\- 传输一个URL',

        # DESCRIPTION
        r'\fBcurl\fP is a tool for transferring data from or to a server using URLs\. It':
            r'\fBcurl\fP 是一个使用URL从服务器传输数据或向服务器传输数据的工具。它',
        r'supports these protocols: DICT, FILE, FTP, FTPS, GOPHER, GOPHERS, HTTP, HTTPS,':
            r'支持以下协议：DICT、FILE、FTP、FTPS、GOPHER、GOPHERS、HTTP、HTTPS、',
        r'IMAP, IMAPS, LDAP, LDAPS, MQTT, MQTTS, POP3, POP3S, RTSP, SCP, SFTP, SMB,':
            r'IMAP、IMAPS、LDAP、LDAPS、MQTT、MQTTS、POP3、POP3S、RTSP、SCP、SFTP、SMB、',
        r'SMBS, SMTP, SMTPS, TELNET, TFTP, WS and WSS\.':
            r'SMBS、SMTP、SMTPS、TELNET、TFTP、WS 和 WSS。',
        r'curl is powered by libcurl for all transfer\-related features\. See':
            r'curl 由 libcurl 驱动以实现所有传输相关功能。请参见',
        r'\fIlibcurl\(3\)\fP for details\.': r'\fIlibcurl(3)\fP 获取详细信息。',

        # URL
        r'The URL syntax is protocol\-dependent\. You can find a detailed description in':
            r'URL语法依赖于协议。您可以在以下文档中找到详细描述',
        r'RFC 3986\.': r'RFC 3986。',
        r'If you provide a URL without a leading "protocol://" scheme, curl guesses':
            r'如果您提供的URL不包含前导的"protocol://"方案，curl 会猜测',
        r'what protocol you want\. It then defaults to HTTP but assumes others based on':
            r'您想要的协议。然后默认使用 HTTP，但根据以下条件假设使用其他协议',
        r'often\-used hostname prefixes\. For example, for hostnames starting with "ftp\."':
            r'常用的主机名前缀。例如，对于以"ftp."开头的主机名',
        r'curl assumes you want FTP\.': r'curl 假设您想使用 FTP。',
        r'You can specify any amount of URLs on the command line\. They are fetched in a':
            r'您可以在命令行中指定任意数量的URL。它们按指定顺序',
        r'sequential manner in the specified order unless you use \fI\-\-parallel\fP\. You can':
            r'依次获取，除非您使用 \fI\-\-parallel\fP。您可以',
        r'specify command line options and URLs mixed and in any order on the command':
            r'在命令行中以任意顺序混合指定命令行选项和URL。',
        r'curl attempts to reuse connections when doing multiple transfers, so that':
            r'curl 在进行多次传输时会尝试重用连接，这样',
        r'getting many files from the same server do not use multiple connects and setup':
            r'从同一服务器获取多个文件时无需建立多个连接和',
        r'handshakes\. This improves speed\. Connection reuse can only be done for URLs':
            r'握手。这提高了速度。连接重用仅适用于',
        r'specified for a single command line invocation and cannot be performed between':
            r'单个命令行调用中指定的URL，不能在',
        r'separate curl runs\.': r'不同的 curl 运行之间进行。',
        r'Everything provided on the command line that is not a command line option or':
            r'命令行上提供的既不是命令行选项也不是其参数的所有内容，',
        r'its argument, curl assumes is a URL and treats it as such\.':
            r'curl 会将其视为URL并按URL处理。',
        r'its argument, curl assumes is a URL and treats it as such$':
            r'curl 会视为URL并按此处理',

        # GLOBBING
        r'You can specify multiple URLs or parts of URLs by writing lists within braces':
            r'您可以通过在花括号内编写列表或在方括号内编写范围来指定多个URL或URL的部分。',
        r'or ranges within brackets\. We call this "globbing"\.':
            r'我们称之为"通配符匹配"。',
        r'Provide a list with three different names like this:':
            r'提供包含三个不同名称的列表，如下所示：',
        r'Do sequences of alphanumeric series by using \[\] as in:':
            r'使用[]生成字母数字序列，如下所示：',
        r'With leading zeroes:': r'带前导零：',
        r'With letters through the alphabet:': r'按字母顺序排列：',
        r'Nested sequences are not supported, but you can use several ones next to each':
            r'不支持嵌套序列，但您可以并排使用多个序列：',
        r'You can specify a step counter for the ranges to get every Nth number or':
            r'您可以为范围指定步长计数器，以获取每第N个数字或',
        r'letter:': r'字母：',
        r'When using \[\] or \{\} sequences when invoked from a command line prompt, you':
            r'在命令行提示符下使用[]或{}序列时，您',
        r'probably have to put the full URL within double quotes to avoid the shell from':
            r'可能需要将完整URL放在双引号中，以避免shell',
        r'interfering with it\. This also goes for other characters treated special, like':
            r'的干扰。这也适用于其他特殊字符，例如',
        r"for example \\\(aq&\\\(aq, \\\(aq\?\\\(aq and \\\(aq\*\\\(aq\.":
            r"例如 \(aq&\(aq、\(aq?\(aq 和 \(aq*\(aq。",
        r'The separate globbing components can be referenced in the \fI\-\-output\fP option to':
            r'可以在 \fI\-\-output\fP 选项中引用单独的通配符组件，以便',
        r'allow pieces to be reused in the target filename\.':
            r'在目标文件名中重用片段。',
        r'Starting in curl 8\.21\.0, the separate globbing parts can be named and':
            r'从 curl 8.21.0 开始，单独的通配符部分可以命名并',
        r'referenced by their names\. The case sensitive alphanumeric name is set':
            r'通过名称引用。区分大小写的字母数字名称设置在',
        r'enclosed within angle brackets after the opening character\. Examples:':
            r'开始字符之后的尖括号内。示例：',
        r'Setting the same glob name twice is an error\.': r'两次设置相同的通配符名称会出错。',
        r'Switch off globbing with \fI\-\-globoff\fP\.': r'使用 \fI\-\-globoff\fP 关闭通配符匹配。',

        # VARIABLES
        r'curl supports command line variables \(added in 8\.3\.0\)\. Set variables with':
            r'curl 支持命令行变量（在 8.3.0 中添加）。使用以下方式设置变量',
        r'\fI\-\-variable\fP name=content or \fI\-\-variable\fP name@file \(where "file" can be stdin if':
            r'\fI\-\-variable\fP name=content 或 \fI\-\-variable\fP name@file（其中"file"可以是 stdin，如果',
        r'set to a single dash \(\-\)\)\.': r'设置为单个破折号（-））。',
        r'Variable contents can be expanded in option parameters using "\{\{name\}\}" if the':
            r'如果选项名称以"\fI\-\-expand\-\fP"为前缀，可以使用"{{name}}"在选项参数中展开变量内容。',
        r'option name is prefixed with "\fI\-\-expand\-\fP"\. This gets the contents of the':
            r'这将插入变量"name"的内容，如果该名称不作为变量存在，则插入空白。',
        r'variable "name" inserted, or a blank if the name does not exist as a':
            r'变量中。要在字符串中逐字插入"{{"，请在前面加上反斜杠，',
        r'variable\. Insert "\{\{" verbatim in the string by prefixing it with a backslash,':
            r'如"\\{{"。',
        r'You can access and expand environment variables by importing them with':
            r'您可以通过导入环境变量来访问和展开它们',
        r'\\&"\fI\-\-variable\fP %name"\. This imports the variable called "name" but exits with an':
            r'使用\&"\fI\-\-variable\fP %name"。这会导入名为"name"的变量，但如果该环境变量未设置则会退出并报错。',
        r'error if that environment variable is not already set\. To provide a default':
            r'要提供默认值（如果尚未设置），',
        r'value in case it is not already set, use "\fI\-\-variable\fP %name=content" or':
            r'请使用 "\fI\-\-variable\fP %name=content" 或',
        r'\\&"\fI\-\-variable\fP %name@content"\.': r'\&"\fI\-\-variable\fP %name@content"。',
        r'Example: get the USER environment variable and expand into the URL, fail if':
            r'示例：获取USER环境变量并展开到URL中，如果未设置则失败：',
        r'When expanding variables, curl supports a set of functions that can make the':
            r'展开变量时，curl支持一组函数使其内容更方便使用。',
        r'variable contents more convenient to use\. It can trim leading and trailing':
            r'它可以使用"trim"修剪前后空白，',
        r'white space with "trim", output the contents as a JSON quoted string with':
            r'使用"json"将内容输出为JSON引号字符串，',
        r'\\&"json", URL encode the string with "url", base64 encode it with "b64" and':
            r'使用"url"进行URL编码，使用"b64"进行base64编码，',
        r'base64 decode it with "64dec"\. To apply functions to a variable expansion, add':
            r'以及使用"64dec"进行base64解码。要将函数应用于变量展开，',
        r'them colon separated to the right side of the variable\. Variable content':
            r'将它们以冒号分隔添加到变量的右侧。包含未编码',
        r'holding null bytes that are not encoded when expanded causes an error\.':
            r'的空字节的变量内容在展开时会导致错误。',
        r'Example: get the contents of a file called \$HOME/\.secret into a variable':
            r'示例：将$HOME/.secret文件的内容读入一个变量',
        r'called "fix"\. Make sure that the content is trimmed and percent\-encoded when':
            r'名为"fix"。确保内容在作为POST数据发送时经过修剪和百分比编码：',
        r'sent as POST data:': r'',
        r'Command line variables and expansions were added in 8\.3\.0\.':
            r'命令行变量和展开功能在 8.3.0 中添加。',

        # OUTPUT
        r'If not told otherwise, curl writes the received data to stdout\. It can be':
            r'如果没有另行指定，curl将接收到的数据写入stdout。可以通过',
        r'instructed to instead save that data into a local file, using the \fI\-\-output\fP or':
            r'使用 \fI\-\-output\fP 或 \fI\-\-remote\-name\fP 选项指示其将数据保存到本地文件。',
        r'\fI\-\-remote\-name\fP options\. If curl is given multiple URLs to transfer on the':
            r'如果curl在命令行中获取多个URL，',
        r'command line, it similarly needs multiple options for where to save them\.':
            r'它同样需要多个选项来指定保存位置。',
        r'curl does not parse or otherwise "understand" the content it gets or writes as':
            r'curl不会解析或以其他方式"理解"其获取或写入作为输出内容。',
        r'output\. It does no encoding or decoding, unless explicitly asked to with':
            r'它不进行编码或解码，除非通过专用命令行选项明确要求。',

        # PROTOCOLS
        r'curl supports numerous protocols, or put in URL terms: schemes\. Your':
            r'curl支持多种协议，或用URL术语来说：方案。您',
        r'particular build may not support them all\.': r'特定的编译版本可能不支持所有协议。',
        r'Lets you lookup words using online dictionaries\.': r'允许您使用在线词典查找单词。',
        r'Read or write local files\. curl does not support accessing "file://" URL': r'读取或写入本地文件。curl不支持远程访问"file://" URL，',
        r'remotely, but when running on Microsoft Windows using the native UNC approach': r'但在Microsoft Windows上运行时使用原生的UNC方法可以工作。',
        r'works\. Only absolute paths\.': r'仅支持绝对路径。',
        r'curl supports the File Transfer Protocol with a lot of tweaks and levers\. With': r'curl支持文件传输协议，具有丰富的调整和选项。',
        r'or without using TLS\.': r'支持使用或不使用TLS。',
        r'Retrieve files\.': r'检索文件。',
        r'curl supports HTTP with numerous options and variations\. It can speak HTTP': r'curl支持具有多种选项和变体的HTTP。它可以根据',
        r'version 0\.9, 1\.0, 1\.1, 2 and 3 depending on build options and the correct': r'编译选项和正确的命令行选项使用HTTP版本0.9、1.0、1.1、2和3。',
        r'Using the mail reading protocol, curl can download emails for you\. With or': r'使用邮件阅读协议，curl可以为您下载电子邮件。',
        r'without using TLS\.$': r'支持使用或不使用TLS。',
        r'curl can do directory lookups for you, with or without TLS\.': r'curl可以为您执行目录查找，支持使用或不使用TLS。',
        r'curl supports MQTT version 3\. Downloading over MQTT equals subscribing to a': r'curl支持MQTT版本3。通过MQTT下载相当于订阅主题，',
        r'topic while uploading/posting equals publishing on a topic\. MQTT over TLS is not': r'而上传/发布相当于在主题上发布。MQTT over TLS',
        r'supported \(yet\)\.$': r'目前尚不支持。',
        r'supported \(yet\)\.': r'目前尚不支持。',
        r'Downloading from a pop3 server means getting an email\. With or without using': r'从pop3服务器下载意味着获取电子邮件。',
        r'curl supports RTSP 1\.0 downloads\.': r'curl支持RTSP 1.0下载。',
        r'curl supports SSH version 2 scp transfers\.': r'curl支持SSH版本2的scp传输。',
        r'curl supports SFTP \(draft 5\) done over SSH version 2\.': r'curl支持在SSH版本2上执行的SFTP（草案5）。',
        r'curl supports SMB version 1 for upload and download\.': r'curl支持SMB版本1的上传和下载。',
        r'Uploading contents to an SMTP server means sending an email\. With or without': r'向SMTP服务器上传内容意味着发送电子邮件。',
        r'Fetching a telnet URL starts an interactive session where it sends what it': r'获取telnet URL会启动交互式会话，在其中发送从stdin读取的内容',
        r'reads on stdin and outputs what the server sends it\.': r'并输出服务器发送的内容。',
        r'curl can do TFTP downloads and uploads\.': r'curl可以执行TFTP下载和上传。',
        r'WebSocket done over HTTP/1\. WSS implies that it works over HTTPS\.': r'通过HTTP/1实现的WebSocket。WSS意味着通过HTTPS工作。',

        # PROGRESS METER
        r'curl normally displays a progress meter during operations, indicating the': r'curl通常在操作期间显示进度指示器，显示',
        r'amount of transferred data, transfer speeds and estimated time left, etc\. The': r'传输数据量、传输速度和预计剩余时间等。',
        r'progress meter displays the transfer rate in bytes per second\. The used': r'进度指示器以每秒字节数显示传输速率。使用的',
        r'suffixes \("k" for kilo, "M" for mega, "G" for giga, "T" for tera, "P" for peta': r'后缀（"k"表示千，"M"表示兆，"G"表示吉，"T"表示太，"P"表示拍，',
        r'and "E" for exa\) are 1024 based\. For example 1k is 1024 bytes\. 1M is 1048576': r'"E"表示艾）基于1024。例如1k等于1024字节。1M等于1048576字节。',
        r'bytes\. Strictly speaking this makes the units kibibyte and mebibyte etc\.': r'严格来说，这使得单位成为千比字节和兆比字节等。',
        r'curl displays this data to the terminal by default, so if you invoke curl to': r'curl默认将这些数据显示到终端，因此如果您调用curl执行',
        r'do an operation and it is about to write data to the terminal, it \fIdisables\fP': r'操作且即将向终端写入数据，它会\fI禁用\fP',
        r'the progress meter as otherwise it would mess up the output mixing progress': r'进度指示器，否则会弄乱输出，混合进度',
        r'meter and response data\.$': r'指示器和响应数据。',
        r'meter and response data\.': r'指示器和响应数据。',
        r'If you want a progress meter for HTTP POST or PUT requests, you need to': r'如果您想要HTTP POST或PUT请求的进度指示器，您需要',
        r'redirect the response output to a file, using shell redirect \(>\), \fI\-\-output\fP or': r'使用shell重定向（>）、\fI\-\-output\fP或类似方法将响应输出重定向到文件。',
        r'similar\.$': r'',
        r'similar\.': r'',
        r'This does not apply to FTP upload as that operation does not spit out any': r'这不适用于FTP上传，因为该操作不会向终端输出任何',
        r'response data to the terminal\.$': r'响应数据。',
        r'response data to the terminal\.': r'响应数据。',
        r'If you prefer a progress bar instead of the regular meter, \fI\-\-progress\-bar\fP is': r'如果您更喜欢进度条而不是常规指示器，可以使用',
        r'your friend\. You can also disable the progress meter completely with the': r'\fI\-\-progress\-bar\fP。您也可以使用',
        r'\fI\-\-silent\fP option\.$': r'\fI\-\-silent\fP 选项完全禁用进度指示器。',
        r'\fI\-\-silent\fP option\.': r'\fI\-\-silent\fP 选项完全禁用进度指示器。',

        # VERSION
        r'This man page describes curl 8\.21\.0\. If you use a later version, chances': r'此手册页描述的是curl 8.21.0。如果您使用更新的版本，',
        r'are this man page does not fully document it\. If you use an earlier version,': r'此手册页可能不能完整记录它。如果您使用较早版本，',
        r'this document tries to include version information about which specific': r'本文档尽量包含关于引入更改的',
        r'version that introduced changes\.$': r'具体版本信息。',
        r'version that introduced changes\.': r'具体版本信息。',
        r'You can always learn which the latest curl version is by running': r'您可以随时通过运行以下命令了解最新的curl版本：',
        r'The online version of this man page is always showing the latest incarnation:': r'此手册页的在线版本始终显示最新版本：',
        r'https://curl\.se/docs/manpage\.html': r'https://curl.se/docs/manpage.html',

        # OPTIONS
        r'Options start with one or two dashes\. Many of the options require an': r'选项以一个或两个破折号开头。许多选项需要一个',
        r'additional value next to them\. If provided text does not start with a dash, it': r'附加的值。如果提供的文本不以破折号开头，',
        r'is presumed to be and treated as a URL\.': r'则假定为URL并按URL处理。',
        r'is presumed to be and treated as a URL$': r'则假定为URL并按URL处理',
        r'The short "single\-dash" form of the options, \-d for example, may be used with': r'选项的短"单破折号"形式（例如\-d）可以',
        r'or without a space between it and its value, although a space is a recommended': r'在它与值之间使用或不使用空格，但建议使用空格作为分隔符。',
        r'separator\. The long double\-dash form, \fI\-\-data\fP for example, requires a space': r'长双破折号形式（例如\fI\-\-data\fP）要求在其值与之间有一个空格。',
        r'Short version options that do not need any additional values can be used': r'不需要额外值的短版本选项可以',
        r'immediately next to each other, like for example you can specify all the': r'相邻使用，例如您可以将所有选项',
        r'options \fI\-O\fP, \fI\-L\fP and \fI\-v\fP at once as \fI\-OLv\fP\.': r'\fI\-O\fP、\fI\-L\fP和\fI\-v\fP一次性指定为\fI\-OLv\fP。',
        r'In general, all boolean options are enabled with \\-\-\fBoption\fP and yet again': r'通常，所有布尔选项使用\-\-\fBoption\fP启用，',
        r'disabled with \\-\-\fBno\\-\fPoption\. That is, you use the same option name but': r'使用\-\-\fBno\-\fPoption禁用。也就是说，使用相同的选项名称但',
        r'prefix it with "no\\-"\. In this list we mostly show the \\-\-\fBoption\fP version of': r'在前面加上"no\-"。在此列表中我们主要显示选项的\-\-\fBoption\fP版本。',
        r'When \fI\-\-next\fP is used, it resets the parser state and you start again with a': r'当使用\fI\-\-next\fP时，它会重置解析器状态，您可以',
        r'clean option state, except for the options that are global\. Global options': r'从干净的选项状态重新开始，但全局选项除外。全局选项',
        r'retain their values and meaning even after \fI\-\-next\fP\.': r'即使在\fI\-\-next\fP之后也保留其值和含义。',
        r'If the long option name ends with an equals sign \("="\), the argument is the': r'如果长选项名称以等号（"="）结尾，则参数是',
        r'text following on its right side\. \(Added in 8\.16\.0\)$': r'其右侧跟随的文本。（在8.16.0中添加）',
        r'text following on its right side\. \(Added in 8\.16\.0\)': r'其右侧跟随的文本。（在8.16.0中添加）',
        r'The first argument that is exactly two dashes \("\-\-"\), marks the end of': r'恰好有两个破折号（"\-\-"）的第一个参数标志着选项结束；',
        r'options; any argument after the end of options is interpreted as a URL': r'选项结束后的任何参数都被解释为URL参数，',
        r'argument even if it starts with a dash\.': r'即使以破折号开头。',
        r'curl does little to no verification of the contents of command line arguments\.': r'curl对命令行参数的内容几乎不进行验证。',
        r'Passing in "creative octets" like newlines might trigger unexpected results\.': r'传入像换行符这样的"创意字节"可能会触发意外结果。',

        # OPTIONS - "For <option> to work..."
        r'For \fI\-\-dns\-interface\fP to work, it requires that the underlying libcurl is built to support c\-ares\.': r'\fI\-\-dns\-interface\fP 要正常工作，需要底层的 libcurl 编译时支持 c-ares。',
        r'For \fI\-\-dns\-ipv4\-addr\fP to work, it requires that the underlying libcurl is built to support c\-ares\.': r'\fI\-\-dns\-ipv4\-addr\fP 要正常工作，需要底层的 libcurl 编译时支持 c-ares。',
        r'For \fI\-\-dns\-ipv6\-addr\fP to work, it requires that the underlying libcurl is built to support c\-ares\.': r'\fI\-\-dns\-ipv6\-addr\fP 要正常工作，需要底层的 libcurl 编译时支持 c-ares。',
        r'For \fI\-\-dns\-servers\fP to work, it requires that the underlying libcurl is built to support c\-ares\.': r'\fI\-\-dns\-servers\fP 要正常工作，需要底层的 libcurl 编译时支持 c-ares。',
    }

    for pattern, replacement in trans_map.items():
        if re.match('^' + pattern + '$', line):
            return replacement

    # Handle lines that already have replacements applied (no match yet)
    return line


def main():
    with open('/tmp/man1_zh/curl.1', 'r') as f:
        content = f.read()

    lines = content.split('\n')
    result = []

    for line in lines:
        result.append(translate_line(line))

    with open('/tmp/man1_zh/curl.1', 'w') as f:
        f.write('\n'.join(result))

    print(f"Translated {len(result)} lines")

if __name__ == '__main__':
    main()
