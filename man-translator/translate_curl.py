#!/usr/bin/env python3
"""Translate curl.1 man page from English to Chinese, preserving roff formatting."""

import re
import os

# Read the source
with open('/usr/share/man/man1/curl.1.gz', 'rb') as f:
    import gzip
    content = gzip.decompress(f.read()).decode('utf-8', errors='replace')

lines = content.split('\n')

# Translation rules applied in order
translations = [
    # =========== SECTION HEADERS ===========
    (r'^\.SH NAME$', '.SH 名称'),
    (r'^\.SH SYNOPSIS$', '.SH 概述'),
    (r'^\.SH DESCRIPTION$', '.SH 描述'),
    (r'^\.SH URL$', '.SH URL'),
    (r'^\.SH GLOBBING$', '.SH 通配符匹配'),
    (r'^\.SH VARIABLES$', '.SH 变量'),
    (r'^\.SH OUTPUT$', '.SH 输出'),
    (r'^\.SH PROTOCOLS$', '.SH 协议'),
    (r'^\.SH PROGRESS METER$', '.SH 进度指示器'),
    (r'^\.SH VERSION$', '.SH 版本'),
    (r'^\.SH OPTIONS$', '.SH 选项'),
    (r'^\.SH ALL OPTIONS$', '.SH 所有选项'),
    (r'^\.SH EXAMPLES$', '.SH 示例'),
    (r'^\.SH AUTHOR$', '.SH 作者'),
    (r'^\.SH "REPORTING BUGS"$', '.SH "报告错误"'),
    (r'^\.SH COPYRIGHT$', '.SH 版权'),
    (r'^\.SH "SEE ALSO"$', '.SH "另请参见"'),
    (r'^\.SH FILES$', '.SH 文件'),
    (r'^\.SH ENVIRONMENT$', '.SH 环境变量'),
    (r'^\.SH EXIT CODES$', '.SH 退出码'),
    (r'^\.SH PROXY PROTOCOL PREFIXES$', '.SH 代理协议前缀'),

    # =========== MISC FIXED STRINGS ===========
    (r'^(\.SH .*)$', lambda m: m.group(1)),  # preserve already translated

    # =========== PARAGRAPH TEXT TRANSLATIONS - LINE BY LINE ===========

    # .TH header - update "User Commands" style
    (r'^(\.TH curl 1 "2026-06-24" "curl 8\.21\.0" "curl Manual")$',
     r'.TH curl 1 "2026-06-24" "curl 8.21.0" "curl 用户命令"'),

    # NAME section
    (r'^curl \\- transfer a URL$',
     r'curl \- 传输一个URL'),

    # DESCRIPTION section
    (r'^\fBcurl\fP is a tool for transferring data from or to a server using URLs\. It$',
     r'\fBcurl\fP 是一个使用URL从服务器传输数据或向服务器传输数据的工具。它'),
    (r'^supports these protocols: DICT, FILE, FTP, FTPS, GOPHER, GOPHERS, HTTP, HTTPS,$',
     r'支持以下协议：DICT、FILE、FTP、FTPS、GOPHER、GOPHERS、HTTP、HTTPS、'),
    (r'^IMAP, IMAPS, LDAP, LDAPS, MQTT, MQTTS, POP3, POP3S, RTSP, SCP, SFTP, SMB,$',
     r'IMAP、IMAPS、LDAP、LDAPS、MQTT、MQTTS、POP3、POP3S、RTSP、SCP、SFTP、SMB、'),
    (r'^SMBS, SMTP, SMTPS, TELNET, TFTP, WS and WSS\.$',
     r'SMBS、SMTP、SMTPS、TELNET、TFTP、WS 和 WSS。'),

    (r'^curl is powered by libcurl for all transfer\-related features\. See$',
     r'curl 由 libcurl 驱动以实现所有传输相关的功能。请参见'),
    (r'^\fIlibcurl\(3\)\fP for details\.$',
     r'\fIlibcurl(3)\fP 获取详细信息。'),

    # URL section
    (r'^The URL syntax is protocol\-dependent\. You can find a detailed description in$',
     r'URL 语法取决于协议。您可以在以下文档中找到详细描述'),
    (r'^RFC 3986\.$',
     r'RFC 3986。'),

    (r'^If you provide a URL without a leading "protocol://" scheme, curl guesses$',
     r'如果您提供不带前导 "protocol://" 方案的URL，curl 会猜测'),
    (r'^what protocol you want\. It then defaults to HTTP but assumes others based on$',
     r'您想要使用的协议。然后默认使用 HTTP，但会根据'),
    (r'^often\-used hostname prefixes\. For example, for hostnames starting with "ftp\."$',
     r'常用的主机名前缀来假设其他协议。例如，对于以 "ftp." 开头的主机名，'),
    (r'^curl assumes you want FTP\.$',
     r'curl 假设您想要使用 FTP。'),

    (r'^You can specify any amount of URLs on the command line\. They are fetched in a$',
     r'您可以在命令行中指定任意数量的URL。它们按指定顺序'),
    (r'^sequential manner in the specified order unless you use \fI\-\-parallel\fP\. You can$',
     r'依次获取，除非您使用 \fI\-\-parallel\fP。您可以'),
    (r'^specify command line options and URLs mixed and in any order on the command$',
     r'在命令行中以任意顺序混合指定命令行选项和URL。'),
    (r'^line\.$|^$', lambda m: m.group(0)),  # skip empty lines

    # Connection reuse
    (r'^curl attempts to reuse connections when doing multiple transfers, so that$',
     r'curl 在进行多次传输时会尝试重用连接，这样'),
    (r'^getting many files from the same server do not use multiple connects and setup$',
     r'从同一服务器获取多个文件时不会使用多个连接和设置'),
    (r'^handshakes\. This improves speed\. Connection reuse can only be done for URLs$',
     r'握手。这提高了速度。连接重传只能用于'),
    (r'^specified for a single command line invocation and cannot be performed between$',
     r'单个命令行调用中指定的URL，不能在'),
    (r'^separate curl runs\.$',
     r'不同的 curl 运行之间进行。'),

    (r'^Everything provided on the command line that is not a command line option or$',
     r'命令行上提供的所有内容，如果不是命令行选项或'),
    (r'^its argument, curl assumes is a URL and treats it as such\.$',
     r'其参数，curl 会认为是URL并以此处理。'),

    # GLOBBING section
    (r'^You can specify multiple URLs or parts of URLs by writing lists within braces$',
     r'您可以通过在花括号内编写列表或在方括号内编写范围来指定多个URL或URL的部分。'),
    (r'^or ranges within brackets\. We call this "globbing"\.$',
     r'我们称之为"通配符匹配"。'),
    (r'^Provide a list with three different names like this:$',
     r'提供带有三个不同名称的列表，如下所示：'),
    (r'^Do sequences of alphanumeric series by using \[\] as in:$',
     r'使用 [] 生成字母数字序列，如下所示：'),
    (r'^With leading zeroes:$',
     r'带前导零：'),
    (r'^With letters through the alphabet:$',
     r'按字母顺序排列：'),
    (r'^Nested sequences are not supported, but you can use several ones next to each$',
     r'不支持嵌套序列，但您可以并排使用多个序列：'),
    (r'^other:$',
     r''),
    (r'^You can specify a step counter for the ranges to get every Nth number or$',
     r'您可以为范围指定步长计数器，以获取每第N个数字或'),
    (r'^letter:$',
     r'字母：'),
    (r'^When using \[\] or \{\} sequences when invoked from a command line prompt, you$',
     r'当从命令行提示符调用时使用 [] 或 {} 序列，您'),
    (r'^probably have to put the full URL within double quotes to avoid the shell from$',
     r'可能需要将完整的URL放在双引号中，以避免shell'),
    (r'^interfering with it\. This also goes for other characters treated special, like$',
     r'干扰它。这也适用于其他特殊字符，例如'),
    (r"^for example \\\(aq&\\\(aq, \\\(aq\?\\\(aq and \\\(aq\*\\\(aq\.$",
     r'例如 \(aq&\(aq、\(aq?\(aq 和 \(aq*\(aq。'),

    (r'^The separate globbing components can be referenced in the \fI\-\-output\fP option to$',
     r'可以在 \fI\-\-output\fP 选项中引用单独的通配符组件，以'),
    (r'^allow pieces to be reused in the target filename\.$',
     r'允许在目标文件名中重用片段。'),

    (r'^Starting in curl 8\.21\.0, the separate globbing parts can be named and$',
     r'从 curl 8.21.0 开始，可以为单独的通配符部分命名，并'),
    (r'^referenced by their names\. The case sensitive alphanumeric name is set$',
     r'通过名称引用它们。区分大小写的字母数字名称设置'),
    (r'^enclosed within angle brackets after the opening character\. Examples:$',
     r'在开始字符之后，用尖括号括起来。示例：'),

    (r'^Setting the same glob name twice is an error\.$',
     r'设置相同的通配符名称两次是错误的。'),
    (r'^Switch off globbing with \fI\-\-globoff\fP\.$',
     r'使用 \fI\-\-globoff\fP 关闭通配符匹配。'),

    # VARIABLES section
    (r'^curl supports command line variables \(added in 8\.3\.0\)\. Set variables with$',
     r'curl 支持命令行变量（在 8.3.0 中添加）。使用'),
    (r'^\fI\-\-variable\fP name=content or \fI\-\-variable\fP name@file \(where "file" can be stdin if$',
     r'\fI\-\-variable\fP name=content 或 \fI\-\-variable\fP name@file 设置变量（其中"file"可以是 stdin，如果'),
    (r'^set to a single dash \(\-\)\)\.$',
     r'设置为单个破折号（-））。'),

    (r'^Variable contents can be expanded in option parameters using "\{\{name\}\}" if the$',
     r'如果选项名称以 "\fI\-\-expand\-\fP" 为前缀，则可以使用 "{{name}}" 在选项参数中展开变量内容。'),
    (r'^option name is prefixed with "\fI\-\-expand\-\fP"\. This gets the contents of the$',
     r''),
    (r'^variable "name" inserted, or a blank if the name does not exist as a$',
     r'这将插入变量"name"的内容，如果该名称不作为变量存在，则插入空白。'),
    (r'^variable\. Insert "\{\{" verbatim in the string by prefixing it with a backslash,$',
     r'通过在字符串前面加上反斜杠来逐字插入 "{{"，例如 "\\{{"。'),
    (r'^like "\\\\\{\{"\.$',
     r''),

    # Access environment variables
    (r"^You can access and expand environment variables by importing them with$",
     r'您可以通过 \&\fI\-\-variable\fP %name 导入和展开环境变量。'),
    (r'^\\&"\fI\-\-variable\fP %name"\. This imports the variable called "name" but exits with an$',
     r''),
    (r'^error if that environment variable is not already set\. To provide a default$',
     r'如果该环境变量尚未设置，则会退出并报错。要提供默认值，'),
    (r'^value in case it is not already set, use "\fI\-\-variable\fP %name=content" or$',
     r'请使用 "\fI\-\-variable\fP %name=content" 或'),
    (r'^\\&"\fI\-\-variable\fP %name@content"\.$',
     r'\&\fI\-\-variable\fP %name@content。'),

    (r'^Example: get the USER environment variable and expand into the URL, fail if$',
     r'示例：获取 USER 环境变量并展开到URL中，如果未设置则失败：'),
    (r'^USER is not set:$',
     r''),

    # Variable functions
    (r'^When expanding variables, curl supports a set of functions that can make the$',
     r'展开变量时，curl 支持一组函数，可以使变量内容更方便使用。'),
    (r'^variable contents more convenient to use\. It can trim leading and trailing$',
     r'它可以使用 "trim" 修剪前导和尾部空格，'),
    (r'^white space with "trim", output the contents as a JSON quoted string with$',
     r'使用 "json" 将内容输出为JSON引号字符串，'),
    (r'^\\&"json", URL encode the string with "url", base64 encode it with "b64" and$',
     r'使用 "url" 进行URL编码，使用 "b64" 进行base64编码，'),
    (r'^base64 decode it with "64dec"\. To apply functions to a variable expansion, add$',
     r'以及使用 "64dec" 进行base64解码。要将函数应用到变量展开，请将'),
    (r'^them colon separated to the right side of the variable\. Variable content$',
     r'它们以冒号分隔添加到变量的右侧。包含未编码'),
    (r'^holding null bytes that are not encoded when expanded causes an error\.$',
     r'的空字节的变量内容在展开时会导致错误。'),

    (r"^Example: get the contents of a file called \\\$HOME/\.secret into a variable$",
     r'示例：将文件 $HOME/.secret 的内容读入一个名为 "fix" 的变量。'),
    (r'^called "fix"\. Make sure that the content is trimmed and percent\-encoded when$',
     r'确保在作为 POST 数据发送时对内容进行修剪和百分比编码：'),
    (r'^sent as POST data:$',
     r''),

    (r'^Command line variables and expansions were added in 8\.3\.0\.$',
     r'命令行变量和展开功能是在 8.3.0 中添加的。'),

    # OUTPUT section
    (r'^If not told otherwise, curl writes the received data to stdout\. It can be$',
     r'如果没有另行指定，curl 将接收到的数据写入 stdout。可以通过'),
    (r'^instructed to instead save that data into a local file, using the \fI\-\-output\fP or$',
     r'使用 \fI\-\-output\fP 或 \fI\-\-remote\-name\fP 选项指示 curl'),
    (r'^\fI\-\-remote\-name\fP options\. If curl is given multiple URLs to transfer on the$',
     r'将数据保存到本地文件。如果在命令行中给 curl 提供了多个要传输的URL，'),
    (r'^command line, it similarly needs multiple options for where to save them\.$',
     r'它同样需要多个选项来指定保存这些数据的位置。'),

    (r'^curl does not parse or otherwise "understand" the content it gets or writes as$',
     r'curl 不会解析或以其他方式"理解"它获取或写入的输出内容。'),
    (r'^output\. It does no encoding or decoding, unless explicitly asked to with$',
     r'它不会进行编码或解码，除非通过专用命令行选项明确要求。'),
    (r'^dedicated command line options\.$',
     r''),

    # PROTOCOLS section
    (r'^curl supports numerous protocols, or put in URL terms: schemes\. Your$',
     r'curl 支持多种协议，或用URL术语说：方案。您特定的'),
    (r'^particular build may not support them all\.$',
     r'构建版本可能不支持所有这些协议。'),
    (r'^\.IP DICT$',
     r'.IP DICT'),
    (r'^Lets you lookup words using online dictionaries\.$',
     r'允许您使用在线词典查找单词。'),
    (r'^\.IP FILE$',
     r'.IP FILE'),
    (r'^Read or write local files\. curl does not support accessing "file://" URL$',
     r'读取或写入本地文件。curl 不支持远程访问 "file://" URL，'),
    (r'^remotely, but when running on Microsoft Windows using the native UNC approach$',
     r'但在 Microsoft Windows 上运行时使用本地 UNC 方式可以工作。'),
    (r'^works\. Only absolute paths\.$',
     r'只能使用绝对路径。'),
    (r'^\.IP FTP\(S\)$',
     r'.IP FTP(S)'),
    (r'^curl supports the File Transfer Protocol with a lot of tweaks and levers\. With$',
     r'curl 支持文件传输协议，具有许多调整和选项。支持'),
    (r'^or without using TLS\.$',
     r'使用或不使用 TLS。'),
    (r'^\.IP GOPHER\(S\)$',
     r'.IP GOPHER(S)'),
    (r'^Retrieve files\.$',
     r'检索文件。'),
    (r'^\.IP HTTP\(S\)$',
     r'.IP HTTP(S)'),
    (r'^curl supports HTTP with numerous options and variations\. It can speak HTTP$',
     r'curl 支持具有多种选项和变化的 HTTP。它可以根据'),
    (r'^version 0\.9, 1\.0, 1\.1, 2 and 3 depending on build options and the correct$',
     r'构建选项和正确的命令行选项，支持 HTTP 版本 0.9、1.0、1.1、2 和 3。'),
    (r'^command line options\.$',
     r''),
    (r'^\.IP IMAP\(S\)$',
     r'.IP IMAP(S)'),
    (r'^Using the mail reading protocol, curl can download emails for you\. With or$',
     r'使用邮件阅读协议，curl 可以为您下载电子邮件。支持'),
    (r'^without using TLS\.$',
     r'使用或不使用 TLS。'),
    (r'^\.IP LDAP\(S\)$',
     r'.IP LDAP(S)'),
    (r'^curl can do directory lookups for you, with or without TLS\.$',
     r'curl 可以为您执行目录查找，支持使用或不使用 TLS。'),
    (r'^\.IP MQTT$',
     r'.IP MQTT'),
    (r'^curl supports MQTT version 3\. Downloading over MQTT equals subscribing to a$',
     r'curl 支持 MQTT 版本 3。通过 MQTT 下载等于订阅'),
    (r'^topic while uploading/posting equals publishing on a topic\. MQTT over TLS is not$',
     r'主题，而上传/发布等于在主题上发布。MQTT over TLS 尚不支持。'),
    (r'^supported \(yet\)\.$',
     r''),
    (r'^\.IP POP3\(S\)$',
     r'.IP POP3(S)'),
    (r'^Downloading from a pop3 server means getting an email\. With or without using$',
     r'从 pop3 服务器下载意味着获取电子邮件。支持'),
    (r'^TLS\.$',
     r'使用或不使用 TLS。'),
    (r'^\.IP RTSP$',
     r'.IP RTSP'),
    (r'^curl supports RTSP 1\.0 downloads\.$',
     r'curl 支持 RTSP 1.0 下载。'),
    (r'^\.IP SCP$',
     r'.IP SCP'),
    (r'^curl supports SSH version 2 scp transfers\.$',
     r'curl 支持 SSH 版本 2 的 scp 传输。'),
    (r'^\.IP SFTP$',
     r'.IP SFTP'),
    (r'^curl supports SFTP \(draft 5\) done over SSH version 2\.$',
     r'curl 支持在 SSH 版本 2 上执行的 SFTP（草案 5）。'),
    (r'^\.IP SMB\(S\)$',
     r'.IP SMB(S)'),
    (r'^curl supports SMB version 1 for upload and download\.$',
     r'curl 支持 SMB 版本 1 的上传和下载。'),
    (r'^\.IP SMTP\(S\)$',
     r'.IP SMTP(S)'),
    (r'^Uploading contents to an SMTP server means sending an email\. With or without$',
     r'向 SMTP 服务器上传内容意味着发送电子邮件。支持'),
    (r'^TLS\.$',
     r'使用或不使用 TLS。'),
    (r'^\.IP TELNET$',
     r'.IP TELNET'),
    (r'^Fetching a telnet URL starts an interactive session where it sends what it$',
     r'获取 telnet URL 会启动一个交互式会话，在该会话中，它发送'),
    (r'^reads on stdin and outputs what the server sends it\.$',
     r'从 stdin 读取的内容，并输出服务器发送给它的内容。'),
    (r'^\.IP TFTP$',
     r'.IP TFTP'),
    (r'^curl can do TFTP downloads and uploads\.$',
     r'curl 可以执行 TFTP 下载和上传。'),
    (r'^\.IP WS\(S\)$',
     r'.IP WS(S)'),
    (r'^WebSocket done over HTTP/1\. WSS implies that it works over HTTPS\.$',
     r'通过 HTTP/1 实现的 WebSocket。WSS 意味着它通过 HTTPS 工作。'),

    # PROGRESS METER section
    (r'^curl normally displays a progress meter during operations, indicating the$',
     r'curl 通常在操作期间显示进度指示器，指示已传输的数据量、'),
    (r'^amount of transferred data, transfer speeds and estimated time left, etc\. The$',
     r'传输速度和预计剩余时间等。'),
    (r'^progress meter displays the transfer rate in bytes per second\. The used$',
     r'进度指示器以每秒字节数显示传输速率。所使用的'),
    (r'^suffixes \("k" for kilo, "M" for mega, "G" for giga, "T" for tera, "P" for peta$',
     r'后缀（"k"表示千，"M"表示兆，"G"表示吉，"T"表示太，"P"表示拍，'),
    (r'^and "E" for exa\) are 1024 based\. For example 1k is 1024 bytes\. 1M is 1048576$',
     r'"E"表示艾）基于 1024。例如 1k 是 1024 字节。1M 是 1048576 字节。'),
    (r'^bytes\. Strictly speaking this makes the units kibibyte and mebibyte etc\.$',
     r'严格来说，这使得单位成为千比字节和兆比字节等。'),

    (r'^curl displays this data to the terminal by default, so if you invoke curl to$',
     r'curl 默认将这些数据显示到终端，因此如果您调用 curl 执行操作'),
    (r'^do an operation and it is about to write data to the terminal, it \fIdisables\fP$',
     r'并且它即将将数据写入终端，它会\fI禁用\fP'),
    (r'^the progress meter as otherwise it would mess up the output mixing progress$',
     r'进度指示器，否则它会弄乱输出，混合进度指示器和响应数据。'),
    (r'^meter and response data\.$',
     r''),

    (r'^If you want a progress meter for HTTP POST or PUT requests, you need to$',
     r'如果您想要 HTTP POST 或 PUT 请求的进度指示器，您需要'),
    (r'^redirect the response output to a file, using shell redirect \(>\), \fI\-\-output\fP or$',
     r'使用 shell 重定向（>）、\fI\-\-output\fP 或类似方法'),
    (r'^similar\.$',
     r'将响应输出重定向到文件。'),

    (r'^This does not apply to FTP upload as that operation does not spit out any$',
     r'这不适用于 FTP 上传，因为该操作不会向终端输出任何响应数据。'),
    (r'^response data to the terminal\.$',
     r''),

    (r'^If you prefer a progress bar instead of the regular meter, \fI\-\-progress\-bar\fP is$',
     r'如果您喜欢进度条而不是常规指示器，可以使用 \fI\-\-progress\-bar\fP。'),
    (r'^your friend\. You can also disable the progress meter completely with the$',
     r'您还可以使用 \fI\-\-silent\fP 选项完全禁用进度指示器。'),
    (r'^\fI\-\-silent\fP option\.$',
     r''),

    # VERSION section
    (r'^This man page describes curl 8\.21\.0\. If you use a later version, chances$',
     r'此手册页描述的是 curl 8.21.0。如果您使用更高版本，'),
    (r'^are this man page does not fully document it\. If you use an earlier version,$',
     r'此手册页可能无法完全记录它。如果您使用较早版本，'),
    (r'^this document tries to include version information about which specific$',
     r'本文档尽量包含关于引入更改的具体版本信息。'),
    (r'^version that introduced changes\.$',
     r''),

    (r'^You can always learn which the latest curl version is by running$',
     r'您始终可以通过运行以下命令了解最新的 curl 版本：'),

    (r'^The online version of this man page is always showing the latest incarnation:$',
     r'此手册页的在线版本始终显示最新版本：'),

    # OPTIONS section
    (r'^Options start with one or two dashes\. Many of the options require an$',
     r'选项以一个或两个破折号开头。许多选项需要一个'),
    (r'^additional value next to them\. If provided text does not start with a dash, it$',
     r'附加的值。如果提供的文本不以破折号开头，则'),
    (r'^is presumed to be and treated as a URL\.$',
     r'假定它是URL并以此处理。'),

    (r'^The short "single\-dash" form of the options, \\-d for example, may be used with$',
     r'短"单破折号"形式的选项，例如 \-d，可以使用带或不带空格的格式，'),
    (r'^or without a space between it and its value, although a space is a recommended$',
     r'但建议使用空格作为分隔符。'),
    (r'^separator\. The long double\-dash form, \fI\-\-data\fP for example, requires a space$',
     r'长双破折号形式，例如 \fI\-\-data\fP，则要求在其值与之间有一个空格。'),
    (r'^between it and its value\.$',
     r''),

    (r'^Short version options that do not need any additional values can be used$',
     r'不需要额外值的短版本选项可以立刻彼此相邻使用，'),
    (r'^immediately next to each other, like for example you can specify all the$',
     r'例如，您可以一次性将选项 \fI\-O\fP、\fI\-L\fP 和 \fI\-v\fP 指定为 \fI\-OLv\fP。'),
    (r'^options \fI\-O\fP, \fI\-L\fP and \fI\-v\fP at once as \fI\-OLv\fP\.$',
     r''),

    (r'^In general, all boolean options are enabled with \\-\-\fBoption\fP and yet again$',
     r'通常，所有布尔选项使用 \-\-\fB选项名\fP 启用，'),
    (r'^disabled with \\-\-\fBno\\-\fPoption\. That is, you use the same option name but$',
     r'使用 \-\-\fBno\-\fP选项名 禁用。也就是说，使用相同的选项名称但'),
    (r'^prefix it with "no\\-"\. In this list we mostly show the \\-\-\fBoption\fP version of$',
     r'在前面加上 "no\-"。在此列表中，我们主要显示选项的 \-\-\fB选项名\fP 版本。'),
    (r'^them\.$',
     r''),

    (r'^When \fI\-\-next\fP is used, it resets the parser state and you start again with a$',
     r'当使用 \fI\-\-next\fP 时，它会重置解析器状态，您可以重新开始一个'),
    (r'^clean option state, except for the options that are global\. Global options$',
     r'干净的选项状态，但全局选项除外。全局选项'),
    (r'^retain their values and meaning even after \fI\-\-next\fP\.$',
     r'即使在 \fI\-\-next\fP 之后也保留它们的值和含义。'),

    (r'^If the long option name ends with an equals sign \("="\), the argument is the$',
     r'如果长选项名称以等号（"="）结尾，则参数是'),
    (r'^text following on its right side\. \(Added in 8\.16\.0\)$',
     r'在其右侧跟随的文本。（在 8.16.0 中添加）'),

    (r'^The first argument that is exactly two dashes \("\-\-"\), marks the end of$',
     r'恰好为两个破折号（"\-\-"）的第一个参数表示选项的结束；'),
    (r'^options; any argument after the end of options is interpreted as a URL$',
     r'选项结束后的任何参数都被解释为URL参数，'),
    (r'^argument even if it starts with a dash\.$',
     r'即使它以破折号开头。'),

    (r'^curl does little to no verification of the contents of command line arguments\.$',
     r'curl 对命令行参数的内容很少或不进行验证。'),
    (r'^Passing in "creative octets" like newlines might trigger unexpected results\.$',
     r'传入像换行符这样的"创意字节"可能会触发意外结果。'),
]

# Build the translated output
result_lines = []
for line in lines:
    translated = line

    # Apply each translation rule
    for pattern, replacement in translations:
        if callable(replacement):
            # Skip callables for now, just keep original
            continue
        if re.match(pattern, translated):
            translated = replacement
            break

    # Now do the per-line English-to-Chinese text translations
    # Lines that are purely roff codes (starting with . or \\) should be kept
    # Lines with mixed content need careful handling

    # Handle common patterns in option descriptions
    # This is a simplified approach; the full translation of 7000+ lines
    # of option descriptions would be done by the following additional rules

    # "See also" pattern
    translated = re.sub(r'^See also (.+)$', r'另请参见 \1', translated)
    translated = re.sub(r'^Examples:$', r'示例：', translated)
    translated = re.sub(r'^Example:$', r'示例：', translated)
    translated = re.sub(r'^Added in ([0-9.]+)\. See also (.+)$', r'在 \1 中添加。另请参见 \2', translated)
    translated = re.sub(r'^Added in ([0-9.]+)\.$', r'在 \1 中添加。', translated)

    # Boilerplate option patterns
    translated = re.sub(r'^If (.+) is provided several times, the last set value is used\.$',
                        r'如果多次提供 \1，则使用最后设置的值。', translated)
    translated = re.sub(r'^Providing (.+) multiple times has no extra effect\.$',
                        r'多次提供 \1 没有额外效果。', translated)
    translated = re.sub(r'^Disable it again with (.+)\.$',
                        r'使用 \1 再次禁用它。', translated)

    # "This option is mutually exclusive with"
    translated = re.sub(r'^This option is mutually exclusive with (.+)\.$',
                        r'此选项与 \1 互斥。', translated)

    # "This option was formerly known as"
    translated = re.sub(r'^This option was formerly known as (.+)\.$',
                        r'此选项以前被称为 \1。', translated)
    translated = re.sub(r'^That option name can still be used but might be removed in a future version\.$',
                        r'该选项名称仍然可以使用，但可能会在未来的版本中移除。', translated)

    # (HTTP), (FTP) etc protocol tags - keep them
    # "Use the specified" -> "使用指定的"
    # This is getting very complex. Let me use a different approach.

    result_lines.append(translated)

# Write output
os.makedirs('/tmp/man1_zh', exist_ok=True)
with open('/tmp/man1_zh/curl.1', 'w') as f:
    f.write('\n'.join(result_lines))

print(f"Written {len(result_lines)} lines to /tmp/man1_zh/curl.1")
