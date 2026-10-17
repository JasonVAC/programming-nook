#!/usr/bin/env python3
"""
Translates curl.1 man page English text to Chinese.
Preserves ALL roff/troff formatting codes EXACTLY.
Does NOT translate: command names, option names, file paths, URLs, version numbers, email addresses.
"""

import re, os

with open('/tmp/man1_zh/curl.1', 'r') as f:
    lines = f.readlines()

# Strip newlines for processing
raw_lines = [l.rstrip('\n') for l in lines]

# Classify each line
LINE_ROFF_CMD = 1   # .SH, .TH, .IP, .RS, .RE, .nf, .fi, .B, .I, etc.
LINE_TEXT = 2        # English text
LINE_BLANK = 3       # empty
LINE_COMMENT = 4     # .\" comments

def classify(line):
    if line == '' or line == '.':
        return LINE_BLANK
    if line.startswith('.\\"'):
        return LINE_COMMENT
    # Roff commands
    if re.match(r'^\.(TH|SH|SS|IP|RS|RE|nf|fi|B|I|BR|IR|RB|RI|BI|)\\', line):
        return LINE_ROFF_CMD
    # .IP may be followed by option definition
    if re.match(r'^\.\w', line):
        return LINE_ROFF_CMD
    return LINE_TEXT

# ====== MULTI-LINE TRANSLATIONS ======
# Join entire file, apply translations, then split back
content = '\n'.join(raw_lines)

# === SECTION HEADERS ===
content = re.sub(r'\n\.SH NAME\n', r'\n.SH 名称\n', content)
content = re.sub(r'\n\.SH SYNOPSIS\n', r'\n.SH 概述\n', content)
content = re.sub(r'\n\.SH DESCRIPTION\n', r'\n.SH 描述\n', content)
content = re.sub(r'\n\.SH GLOBBING\n', r'\n.SH 通配符匹配\n', content)
content = re.sub(r'\n\.SH VARIABLES\n', r'\n.SH 变量\n', content)
content = re.sub(r'\n\.SH OUTPUT\n', r'\n.SH 输出\n', content)
content = re.sub(r'\n\.SH PROTOCOLS\n', r'\n.SH 协议\n', content)
content = re.sub(r'\n\.SH PROGRESS METER\n', r'\n.SH 进度指示器\n', content)
content = re.sub(r'\n\.SH VERSION\n', r'\n.SH 版本\n', content)
content = re.sub(r'\n\.SH OPTIONS\n', r'\n.SH 选项\n', content)
content = re.sub(r'\n\.SH ALL OPTIONS\n', r'\n.SH 所有选项\n', content)
content = re.sub(r'\n\.SH EXAMPLES\n', r'\n.SH 示例\n', content)
content = re.sub(r'\n\.SH AUTHOR\n', r'\n.SH 作者\n', content)
content = re.sub(r'\n\.SH "REPORTING BUGS"\n', r'\n.SH "报告错误"\n', content)
content = re.sub(r'\n\.SH COPYRIGHT\n', r'\n.SH 版权\n', content)
content = re.sub(r'\n\.SH "SEE ALSO"\n', r'\n.SH "另请参见"\n', content)
content = re.sub(r'\n\.SH FILES\n', r'\n.SH 文件\n', content)
content = re.sub(r'\n\.SH ENVIRONMENT\n', r'\n.SH 环境变量\n', content)
content = re.sub(r'\n\.SH EXIT CODES\n', r'\n.SH 退出码\n', content)
content = re.sub(r'\n\.SH PROXY PROTOCOL PREFIXES\n', r'\n.SH 代理协议前缀\n', content)

# === TH header ===
content = content.replace(
    '.TH curl 1 "2026-06-24" "curl 8.21.0" "curl Manual"',
    '.TH curl 1 "2026-06-24" "curl 8.21.0" "curl 用户命令"'
)

# === NAME section ===
content = content.replace(
    'curl \\- transfer a URL',
    'curl \\- 传输一个URL'
)

# === DESCRIPTION section ===
content = content.replace(
    '\\fBcurl\\fP is a tool for transferring data from or to a server using URLs. It\n'
    'supports these protocols: DICT, FILE, FTP, FTPS, GOPHER, GOPHERS, HTTP, HTTPS,\n'
    'IMAP, IMAPS, LDAP, LDAPS, MQTT, MQTTS, POP3, POP3S, RTSP, SCP, SFTP, SMB,\n'
    'SMBS, SMTP, SMTPS, TELNET, TFTP, WS and WSS.',
    '\\fBcurl\\fP 是一个使用URL从服务器传输数据或向服务器传输数据的工具。它\n'
    '支持以下协议：DICT、FILE、FTP、FTPS、GOPHER、GOPHERS、HTTP、HTTPS、\n'
    'IMAP、IMAPS、LDAP、LDAPS、MQTT、MQTTS、POP3、POP3S、RTSP、SCP、SFTP、SMB、\n'
    'SMBS、SMTP、SMTPS、TELNET、TFTP、WS 和 WSS。'
)

content = content.replace(
    'curl is powered by libcurl for all transfer\\-related features. See\n'
    '\\fIlibcurl(3)\\fP for details.',
    'curl 由 libcurl 驱动以实现所有传输相关功能。请参见\n'
    '\\fIlibcurl(3)\\fP 获取详细信息。'
)

# === URL section ===
content = content.replace(
    'The URL syntax is protocol\\-dependent. You can find a detailed description in\n'
    'RFC 3986.',
    'URL语法取决于协议。您可以在 RFC 3986 中找到详细描述。'
)

content = content.replace(
    'If you provide a URL without a leading "protocol://" scheme, curl guesses\n'
    'what protocol you want. It then defaults to HTTP but assumes others based on\n'
    'often\\-used hostname prefixes. For example, for hostnames starting with "ftp."\n'
    'curl assumes you want FTP.',
    '如果您提供的URL中不包含前导的"protocol://"方案，curl 会猜测\n'
    '您想要的协议。然后默认使用 HTTP，但会根据\n'
    '常用的主机名前缀来假设其他协议。例如，对于以"ftp."开头的主机名，\n'
    'curl 会假设您要使用 FTP。'
)

content = content.replace(
    'You can specify any amount of URLs on the command line. They are fetched in a\n'
    'sequential manner in the specified order unless you use \\fI\\-\\-parallel\\fP. You can\n'
    'specify command line options and URLs mixed and in any order on the command\n'
    'line.',
    '您可以在命令行中指定任意数量的URL。它们按指定顺序\n'
    '依次获取，除非您使用 \\fI\\-\\-parallel\\fP。您可以\n'
    '在命令行中以任意顺序混合指定命令行选项和URL。'
)

content = content.replace(
    'curl attempts to reuse connections when doing multiple transfers, so that\n'
    'getting many files from the same server do not use multiple connects and setup\n'
    'handshakes. This improves speed. Connection reuse can only be done for URLs\n'
    'specified for a single command line invocation and cannot be performed between\n'
    'separate curl runs.',
    'curl 在进行多次传输时会尝试重用连接，这样\n'
    '从同一服务器获取多个文件时无需建立多个连接和\n'
    '握手。这提高了速度。连接重用仅适用于\n'
    '单个命令行调用中指定的URL，不能在\n'
    '不同的 curl 运行之间进行。'
)

content = content.replace(
    'Everything provided on the command line that is not a command line option or\n'
    'its argument, curl assumes is a URL and treats it as such.',
    '命令行上提供的所有内容，如果不是命令行选项或\n'
    '其参数，curl 会将其视为URL并按URL处理。'
)

# === GLOBBING section ===
content = content.replace(
    'You can specify multiple URLs or parts of URLs by writing lists within braces\n'
    'or ranges within brackets. We call this "globbing".',
    '您可以通过在花括号内编写列表或在方括号内编写范围来指定多个URL或URL的部分。\n'
    '我们称之为"通配符匹配"。'
)

content = content.replace(
    'Provide a list with three different names like this:',
    '提供包含三个不同名称的列表，如下所示：'
)

content = content.replace(
    'Do sequences of alphanumeric series by using [] as in:',
    '使用 [] 生成字母数字序列，如下所示：'
)

content = content.replace('With leading zeroes:', '带前导零：')
content = content.replace('With letters through the alphabet:', '按字母顺序排列：')

content = content.replace(
    'Nested sequences are not supported, but you can use several ones next to each\n'
    'other:',
    '不支持嵌套序列，但您可以并排使用多个序列：'
)

content = content.replace(
    'You can specify a step counter for the ranges to get every Nth number or\n'
    'letter:',
    '您可以为范围指定步长计数器，以获取每第N个数字或\n'
    '字母：'
)

content = content.replace(
    'When using [] or {} sequences when invoked from a command line prompt, you\n'
    'probably have to put the full URL within double quotes to avoid the shell from\n'
    'interfering with it. This also goes for other characters treated special, like\n'
    'for example \\(aq&\\(aq, \\(aq?\\(aq and \\(aq*\\(aq.',
    '当从命令行提示符调用时使用 [] 或 {} 序列，您\n'
    '可能需要将完整URL放在双引号中，以避免 shell\n'
    '干扰它。这也适用于其他特殊处理的字符，例如\n'
    '\\(aq&\\(aq、\\(aq?\\(aq 和 \\(aq*\\(aq。'
)

content = content.replace(
    'The separate globbing components can be referenced in the \\fI\\-\\-output\\fP option to\n'
    'allow pieces to be reused in the target filename.',
    '可以在 \\fI\\-\\-output\\fP 选项中引用单独的通配符组件，\n'
    '以在目标文件名中重用片段。'
)

content = content.replace(
    'Starting in curl 8.21.0, the separate globbing parts can be named and\n'
    'referenced by their names. The case sensitive alphanumeric name is set\n'
    'enclosed within angle brackets after the opening character. Examples:',
    '从 curl 8.21.0 开始，单独的通配符部分可以命名并\n'
    '通过名称引用。区分大小写的字母数字名称设置在\n'
    '开始字符之后的尖括号内。示例：'
)

content = content.replace(
    'Setting the same glob name twice is an error.',
    '两次设置相同的通配符名称会出错。'
)

content = content.replace(
    'Switch off globbing with \\fI\\-\\-globoff\\fP.',
    '使用 \\fI\\-\\-globoff\\fP 关闭通配符匹配。'
)

# === VARIABLES section ===
content = content.replace(
    'curl supports command line variables (added in 8.3.0). Set variables with\n'
    '\\fI\\-\\-variable\\fP name=content or \\fI\\-\\-variable\\fP name@file (where "file" can be stdin if\n'
    'set to a single dash (\\-)).',
    'curl 支持命令行变量（在 8.3.0 中添加）。使用以下方式设置变量\n'
    '\\fI\\-\\-variable\\fP name=content 或 \\fI\\-\\-variable\\fP name@file（其中"file"可以是 stdin，如果\n'
    '设置为单个破折号（\\-））。'
)

content = content.replace(
    'Variable contents can be expanded in option parameters using "{{name}}" if the\n'
    'option name is prefixed with "\\fI\\-\\-expand\\-\\fP". This gets the contents of the\n'
    'variable "name" inserted, or a blank if the name does not exist as a\n'
    'variable. Insert "{{" verbatim in the string by prefixing it with a backslash,\n'
    'like "\\\\{{".',
    '如果选项名称以 "\\fI\\-\\-expand\\-\\fP" 为前缀，可以在选项参数中使用 "{{name}}" 展开变量内容。\n'
    '这将插入变量"name"的内容，如果该名称不作为变量存在则插入空白。\n'
    '要在字符串中逐字插入 "{{"，请在前面加上反斜杠，\n'
    '如 "\\\\{{"。'
)

content = content.replace(
    'You can access and expand environment variables by importing them with\n'
    '\\&"\\fI\\-\\-variable\\fP %name". This imports the variable called "name" but exits with an\n'
    'error if that environment variable is not already set. To provide a default\n'
    'value in case it is not already set, use "\\fI\\-\\-variable\\fP %name=content" or\n'
    '\\&"\\fI\\-\\-variable\\fP %name@content".',
    '您可以通过导入环境变量来访问和展开它们，\n'
    '使用 \\&"\\fI\\-\\-variable\\fP %name"。这将导入名为"name"的变量，但如果该环境变量\n'
    '尚未设置，则会退出并报错。要在未设置时提供默认值，\n'
    '请使用 "\\fI\\-\\-variable\\fP %name=content" 或\n'
    '\\&"\\fI\\-\\-variable\\fP %name@content"。'
)

content = content.replace(
    'Example: get the USER environment variable and expand into the URL, fail if\n'
    'USER is not set:',
    '示例：获取 USER 环境变量并展开到URL中，如果 USER 未设置则失败：'
)

content = content.replace(
    'When expanding variables, curl supports a set of functions that can make the\n'
    'variable contents more convenient to use. It can trim leading and trailing\n'
    'white space with "trim", output the contents as a JSON quoted string with\n'
    '\\&"json", URL encode the string with "url", base64 encode it with "b64" and\n'
    'base64 decode it with "64dec". To apply functions to a variable expansion, add\n'
    'them colon separated to the right side of the variable. Variable content\n'
    'holding null bytes that are not encoded when expanded causes an error.',
    '展开变量时，curl 支持一组函数，可以使变量内容更方便使用。\n'
    '它可以使用"trim"修剪前后空白，\n'
    '使用\\&"json"将内容输出为JSON引号字符串，\n'
    '使用"url"进行URL编码，使用"b64"进行base64编码，\n'
    '以及使用"64dec"进行base64解码。要将函数应用于变量展开，请\n'
    '将它们以冒号分隔添加到变量的右侧。包含\n'
    '未编码的空字节的变量内容在展开时会导致错误。'
)

content = content.replace(
    'Example: get the contents of a file called $HOME/.secret into a variable\n'
    'called "fix". Make sure that the content is trimmed and percent\\-encoded when\n'
    'sent as POST data:',
    '示例：将 $HOME/.secret 文件的内容读入一个名为"fix"的变量。\n'
    '确保内容在作为 POST 数据发送时经过修剪和百分比编码：'
)

content = content.replace(
    'Command line variables and expansions were added in 8.3.0.',
    '命令行变量和展开功能是在 8.3.0 中添加的。'
)

# === OUTPUT section ===
content = content.replace(
    'If not told otherwise, curl writes the received data to stdout. It can be\n'
    'instructed to instead save that data into a local file, using the \\fI\\-\\-output\\fP or\n'
    '\\fI\\-\\-remote\\-name\\fP options. If curl is given multiple URLs to transfer on the\n'
    'command line, it similarly needs multiple options for where to save them.',
    '如果没有另行指定，curl 将接收到的数据写入 stdout。可以通过\n'
    '使用 \\fI\\-\\-output\\fP 或 \\fI\\-\\-remote\\-name\\fP 选项\n'
    '将其保存到本地文件。如果 curl 在命令行中有多个要传输的URL，\n'
    '它同样需要多个选项来指定保存位置。'
)

content = content.replace(
    'curl does not parse or otherwise "understand" the content it gets or writes as\n'
    'output. It does no encoding or decoding, unless explicitly asked to with\n'
    'dedicated command line options.',
    'curl 不会解析或以其他方式"理解"其获取或写入作为\n'
    '输出的内容。它不进行编码或解码，除非通过专用命令行选项明确要求。'
)

# === PROTOCOLS section ===
content = content.replace(
    'curl supports numerous protocols, or put in URL terms: schemes. Your\n'
    'particular build may not support them all.',
    'curl 支持多种协议，或用URL术语来说：方案。您\n'
    '特定的构建版本可能不支持所有协议。'
)

# Individual protocol descriptions
proto_trans = {
    '\nLets you lookup words using online dictionaries.':
        '\n允许您使用在线词典查找单词。',
    '\nRead or write local files. curl does not support accessing "file://" URL\n'
    'remotely, but when running on Microsoft Windows using the native UNC approach\n'
    'works. Only absolute paths.':
        '\n读取或写入本地文件。curl 不支持远程访问 "file://" URL，\n'
        '但在 Microsoft Windows 上运行时使用原生 UNC 方法可以工作。\n'
        '仅支持绝对路径。',
    '\ncurl supports the File Transfer Protocol with a lot of tweaks and levers. With\n'
    'or without using TLS.':
        '\ncurl 支持文件传输协议，具有丰富的调整和选项。\n'
        '支持使用或不使用 TLS。',
    '\nRetrieve files.': '\n检索文件。',
    '\ncurl supports HTTP with numerous options and variations. It can speak HTTP\n'
    'version 0.9, 1.0, 1.1, 2 and 3 depending on build options and the correct\n'
    'command line options.':
        '\ncurl 支持具有多种选项和变体的 HTTP。它可以根据\n'
        '构建选项和正确的命令行选项，支持\n'
        'HTTP 版本 0.9、1.0、1.1、2 和 3。',
    '\nUsing the mail reading protocol, curl can download emails for you. With or\n'
    'without using TLS.':
        '\n使用邮件阅读协议，curl 可以为您下载电子邮件。支持\n'
        '使用或不使用 TLS。',
    '\ncurl can do directory lookups for you, with or without TLS.':
        '\ncurl 可以为您执行目录查找，支持使用或不使用 TLS。',
    '\ncurl supports MQTT version 3. Downloading over MQTT equals subscribing to a\n'
    'topic while uploading/posting equals publishing on a topic. MQTT over TLS is not\n'
    'supported (yet).':
        '\ncurl 支持 MQTT 版本 3。通过 MQTT 下载相当于订阅\n'
        '主题，而上传/发布相当于在主题上发布。MQTT over TLS\n'
        '目前尚不支持。',
    '\nDownloading from a pop3 server means getting an email. With or without using\n'
    'TLS.':
        '\n从 pop3 服务器下载意味着获取电子邮件。支持\n'
        '使用或不使用 TLS。',
    '\ncurl supports RTSP 1.0 downloads.': '\ncurl 支持 RTSP 1.0 下载。',
    '\ncurl supports SSH version 2 scp transfers.': '\ncurl 支持 SSH 版本 2 的 scp 传输。',
    '\ncurl supports SFTP (draft 5) done over SSH version 2.':
        '\ncurl 支持在 SSH 版本 2 上执行的 SFTP（草案 5）。',
    '\ncurl supports SMB version 1 for upload and download.':
        '\ncurl 支持 SMB 版本 1 的上传和下载。',
    '\nUploading contents to an SMTP server means sending an email. With or without\n'
    'TLS.':
        '\n向 SMTP 服务器上传内容意味着发送电子邮件。支持\n'
        '使用或不使用 TLS。',
    '\nFetching a telnet URL starts an interactive session where it sends what it\n'
    'reads on stdin and outputs what the server sends it.':
        '\n获取 telnet URL 会启动一个交互式会话，在其中发送\n'
        '从 stdin 读取的内容，并输出服务器发送的内容。',
    '\ncurl can do TFTP downloads and uploads.': '\ncurl 可以执行 TFTP 下载和上传。',
    '\nWebSocket done over HTTP/1. WSS implies that it works over HTTPS.':
        '\n通过 HTTP/1 实现的 WebSocket。WSS 意味着通过 HTTPS 工作。',
}

for eng, chn in proto_trans.items():
    content = content.replace(eng, chn)

# === PROGRESS METER section ===
content = content.replace(
    'curl normally displays a progress meter during operations, indicating the\n'
    'amount of transferred data, transfer speeds and estimated time left, etc. The\n'
    'progress meter displays the transfer rate in bytes per second. The used\n'
    'suffixes ("k" for kilo, "M" for mega, "G" for giga, "T" for tera, "P" for peta\n'
    'and "E" for exa) are 1024 based. For example 1k is 1024 bytes. 1M is 1048576\n'
    'bytes. Strictly speaking this makes the units kibibyte and mebibyte etc.',
    'curl 通常在操作期间显示进度指示器，显示\n'
    '已传输的数据量、传输速度和预计剩余时间等。\n'
    '进度指示器以每秒字节数显示传输速率。使用的\n'
    '后缀（"k"表示千，"M"表示兆，"G"表示吉，"T"表示太，"P"表示拍，\n'
    '"E"表示艾）基于 1024。例如 1k 等于 1024 字节。1M 等于 1048576\n'
    '字节。严格来说，这使得单位成为千比字节和兆比字节等。'
)

content = content.replace(
    'curl displays this data to the terminal by default, so if you invoke curl to\n'
    'do an operation and it is about to write data to the terminal, it \\fIdisables\\fP\n'
    'the progress meter as otherwise it would mess up the output mixing progress\n'
    'meter and response data.',
    'curl 默认将这些数据显示到终端，因此如果您调用 curl 执行操作，\n'
    '并且它即将向终端写入数据，它会\\fI禁用\\fP\n'
    '进度指示器，否则会弄乱输出，混合进度\n'
    '指示器和响应数据。'
)

content = content.replace(
    'If you want a progress meter for HTTP POST or PUT requests, you need to\n'
    'redirect the response output to a file, using shell redirect (>), \\fI\\-\\-output\\fP or\n'
    'similar.',
    '如果您想要 HTTP POST 或 PUT 请求的进度指示器，您需要\n'
    '使用 shell 重定向（>）、\\fI\\-\\-output\\fP 或类似方法\n'
    '将响应输出重定向到文件。'
)

content = content.replace(
    'This does not apply to FTP upload as that operation does not spit out any\n'
    'response data to the terminal.',
    '这不适用于 FTP 上传，因为该操作不会向终端输出任何\n'
    '响应数据。'
)

content = content.replace(
    'If you prefer a progress bar instead of the regular meter, \\fI\\-\\-progress\\-bar\\fP is\n'
    'your friend. You can also disable the progress meter completely with the\n'
    '\\fI\\-\\-silent\\fP option.',
    '如果您更喜欢进度条而不是常规指示器，\\fI\\-\\-progress\\-bar\\fP 是\n'
    '您的选择。您也可以使用 \\fI\\-\\-silent\\fP 选项\n'
    '完全禁用进度指示器。'
)

# === VERSION section ===
content = content.replace(
    'This man page describes curl 8.21.0. If you use a later version, chances\n'
    'are this man page does not fully document it. If you use an earlier version,\n'
    'this document tries to include version information about which specific\n'
    'version that introduced changes.',
    '此手册页描述的是 curl 8.21.0。如果您使用更新的版本，\n'
    '可能此手册页不能完整记录它。如果您使用较早版本，\n'
    '本文档尽量包含关于引入更改的具体\n'
    '版本信息。'
)

content = content.replace(
    'You can always learn which the latest curl version is by running',
    '您可以随时通过运行以下命令了解最新的 curl 版本：'
)

content = content.replace(
    'The online version of this man page is always showing the latest incarnation:',
    '此手册页的在线版本始终显示最新版本的内容：'
)

# === OPTIONS section intro ===
content = content.replace(
    'Options start with one or two dashes. Many of the options require an\n'
    'additional value next to them. If provided text does not start with a dash, it\n'
    'is presumed to be and treated as a URL.',
    '选项以一个或两个破折号开头。许多选项需要一个\n'
    '附加的值。如果提供的文本不以破折号开头，\n'
    '则会假设为URL并按URL处理。'
)

content = content.replace(
    'The short "single\\-dash" form of the options, \\-d for example, may be used with\n'
    'or without a space between it and its value, although a space is a recommended\n'
    'separator. The long double\\-dash form, \\fI\\-\\-data\\fP for example, requires a space\n'
    'between it and its value.',
    '选项的短"单破折号"形式（例如 \\-d）可以在它与值之间\n'
    '使用或不使用空格，但建议使用空格作为分隔符。\n'
    '长双破折号形式（例如 \\fI\\-\\-data\\fP）要求在其值与之间\n'
    '有一个空格。'
)

content = content.replace(
    'Short version options that do not need any additional values can be used\n'
    'immediately next to each other, like for example you can specify all the\n'
    'options \\fI\\-O\\fP, \\fI\\-L\\fP and \\fI\\-v\\fP at once as \\fI\\-OLv\\fP.',
    '不需要额外值的短版本选项可以立即\n'
    '彼此相邻使用，例如您可以一次性将\n'
    '选项 \\fI\\-O\\fP、\\fI\\-L\\fP 和 \\fI\\-v\\fP 指定为 \\fI\\-OLv\\fP。'
)

content = content.replace(
    'In general, all boolean options are enabled with \\-\\-\\fBoption\\fP and yet again\n'
    'disabled with \\-\\-\\fBno\\-\\fPoption. That is, you use the same option name but\n'
    'prefix it with "no\\-". In this list we mostly show the \\-\\-\\fBoption\\fP version of\n'
    'them.',
    '通常，所有布尔选项使用 \\-\\-\\fBoption\\fP 启用，\n'
    '使用 \\-\\-\\fBno\\-\\fPoption 禁用。也就是说，使用相同的选项名称但\n'
    '在前面加上"no\\-"。在此列表中，我们主要显示选项的 \\-\\-\\fBoption\\fP 版本。'
)

content = content.replace(
    'When \\fI\\-\\-next\\fP is used, it resets the parser state and you start again with a\n'
    'clean option state, except for the options that are global. Global options\n'
    'retain their values and meaning even after \\fI\\-\\-next\\fP.',
    '当使用 \\fI\\-\\-next\\fP 时，它会重置解析器状态，您可以\n'
    '从干净的选项状态重新开始，但全局选项除外。全局选项\n'
    '即使在 \\fI\\-\\-next\\fP 之后也保留其值和含义。'
)

content = content.replace(
    'If the long option name ends with an equals sign ("="), the argument is the\n'
    'text following on its right side. (Added in 8.16.0)',
    '如果长选项名称以等号（"="）结尾，则参数是\n'
    '其右侧跟随的文本。（在 8.16.0 中添加）'
)

content = content.replace(
    'The first argument that is exactly two dashes ("\\-\\-"), marks the end of\n'
    'options; any argument after the end of options is interpreted as a URL\n'
    'argument even if it starts with a dash.',
    '恰好为两个破折号（"\\-\\-"）的第一个参数标记选项的结束；\n'
    '选项结束后的任何参数都被解释为URL参数，\n'
    '即使以破折号开头。'
)

content = content.replace(
    'curl does little to no verification of the contents of command line arguments.\n'
    'Passing in "creative octets" like newlines might trigger unexpected results.',
    'curl 对命令行参数的内容几乎不进行验证。\n'
    '传入像换行符这样的"创意字节"可能会触发意外结果。'
)

content = content.replace(
    'The following options are global: \\fI\\-\\-fail\\-early\\fP, \\fI\\-\\-libcurl\\fP, \\fI\\-\\-parallel\\-immediate\\fP, \\fI\\-\\-parallel\\-max\\-host\\fP, \\fI\\-\\-parallel\\-max\\fP, \\fI\\-\\-parallel\\fP, \\fI\\-\\-progress\\-bar\\fP, \\fI\\-\\-rate\\fP, \\fI\\-\\-show\\-error\\fP, \\fI\\-\\-stderr\\fP, \\fI\\-\\-styled\\-output\\fP, \\fI\\-\\-trace\\-ascii\\fP, \\fI\\-\\-trace\\-config\\fP, \\fI\\-\\-trace\\-ids\\fP, \\fI\\-\\-trace\\-time\\fP, \\fI\\-\\-trace\\fP and \\fI\\-\\-verbose\\fP.',
    '以下选项是全局的：\\fI\\-\\-fail\\-early\\fP、\\fI\\-\\-libcurl\\fP、\\fI\\-\\-parallel\\-immediate\\fP、\\fI\\-\\-parallel\\-max\\-host\\fP、\\fI\\-\\-parallel\\-max\\fP、\\fI\\-\\-parallel\\fP、\\fI\\-\\-progress\\-bar\\fP、\\fI\\-\\-rate\\fP、\\fI\\-\\-show\\-error\\fP、\\fI\\-\\-stderr\\fP、\\fI\\-\\-styled\\-output\\fP、\\fI\\-\\-trace\\-ascii\\fP、\\fI\\-\\-trace\\-config\\fP、\\fI\\-\\-trace\\-ids\\fP、\\fI\\-\\-trace\\-time\\fP、\\fI\\-\\-trace\\fP 和 \\fI\\-\\-verbose\\fP。'
)

# ====== OPTION DESCRIPTION BOILERPLATE ======
# These are the repetitive patterns found in every option description

# "If option is provided several times, the last set value is used."
content = re.sub(r'\nIf (.+?) is provided several times, the last set value is used\.\n',
                 r'\n如果多次提供 \1，则使用最后设置的值。\n', content)

# "Providing option multiple times has no extra effect."
content = re.sub(r'\nProviding (.+?) multiple times has no extra effect\.\n',
                 r'\n多次提供 \1 没有额外效果。\n', content)

# "Disable it again with --xxx."
content = re.sub(r'\nDisable it again with (.+?)\.\n',
                 r'\n使用 \1 再次禁用它。\n', content)

# "This option is mutually exclusive with..."
content = re.sub(r'\nThis option is mutually exclusive with (.+?)\.\n',
                 r'\n此选项与 \1 互斥。\n', content)

# "See also..."
content = re.sub(r'\nSee also (.+?)\.\n',
                 r'\n另请参见 \1。\n', content)

# "Added in X. See also..."
content = re.sub(r'\nAdded in (\d+\.\d+\.\d+)\. See also (.+?)\.\n',
                 r'\n在 \1 中添加。另请参见 \2。\n', content)

# "Added in X."
content = re.sub(r'\nAdded in (\d+\.\d+\.\d+)\.\n',
                 r'\n在 \1 中添加。\n', content)

# "Examples:" / "Example:"
content = re.sub(r'\nExamples:\n', r'\n示例：\n', content)
content = re.sub(r'\nExample:\n', r'\n示例：\n', content)

# "This option is superfluous since you can specify a socks4 proxy with --proxy"
content = re.sub(
    r'\nThis option is superfluous since you can specify a (\S+) proxy with \\fI\\-\\-proxy\\fP\n',
    r'\n此选项是多余的，因为您可以使用 \\fI\\-\\-proxy\\fP 通过 "\1://" 协议前缀指定 \1 代理。\n',
    content
)
content = re.sub(r'\nusing a "(.+?)://" protocol prefix\.\n', r'', content)

# "This option overrides any previous use of --proxy, as they are mutually exclusive."
# (The "exclusive." part may be on a separate line due to line wrapping)
content = re.sub(
    r'\nThis option overrides any previous use of \\fI\\-\\-proxy\\fP, as they are mutually\n',
    r'\n此选项会覆盖之前对 \\fI\\-\\-proxy\\fP 的任何使用，因为它们是互斥的。\n',
    content
)

# "For --option to work, it requires that the underlying libcurl is built to support TLS."
content = re.sub(
    r'\nFor (.+?) to work, it requires that the underlying libcurl is built to support TLS\.\n',
    r'\n要使用 \1，需要底层 libcurl 编译时支持 TLS。\n', content
)

# "For --option to work, it requires that the underlying libcurl is built to support c-ares."
content = re.sub(
    r'\nFor (.+?) to work, it requires that the underlying libcurl is built to support c-ares\.\n',
    r'\n要使用 \1，需要底层 libcurl 编译时支持 c-ares。\n', content
)

# "This option was formerly known as..."
content = re.sub(
    r'\nThis option was formerly known as (.+?)\.\n',
    r'\n此选项以前被称为 \1。\n', content
)
content = re.sub(
    r'\nThat option name can still be used but might be removed in a future version\.\n',
    r'\n该选项名称仍然可以使用，但可能会在未来的版本中移除。\n', content
)

# "This option is global and does not need to be specified for each use of --next."
content = re.sub(
    r'\nThis option is global and does not need to be specified for each use of \\fI\\-\\-next\\fP\.\n',
    r'\n此选项是全局选项，不需要为每次使用 \\fI\\-\\-next\\fP 指定。\n', content
)

# "This option was called --name before X.X.X. The previous name remains functional."
content = re.sub(
    r'\nThis option was called (.+?) before (.+?)\. The previous name remains functional\.\n',
    r'\n此选项在 \2 之前被称为 \1。之前的名称仍然可用。\n', content
)

# "\fBoption\fP can be used several times in a command line."
content = re.sub(
    r'\n(\\fI\\-\\-[\w\\-]+\\fP) can be used several times in a command line\.\n',
    r'\n\1 可以在命令行中多次使用。\n', content
)
content = re.sub(
    r'\n(\\fI\\-\\-[\w\\-]+\\fP) and (\\fI\\-\\-[\w\\-]+\\fP) can be used several times in a command line\.\n',
    r'\n\1 和 \2 可以在命令行中多次使用。\n', content
)

# "If this option is used several times, curl loads contents from all the..."
content = re.sub(
    r'\nIf this option is used several times, curl loads contents from all the\nfiles but the last one is used for saving\.\n',
    r'\n如果多次使用此选项，curl 从所有文件中加载内容，但\n最后一个文件用于保存。\n', content
)

# "You may want to restrict your umask..."
content = re.sub(
    r'\nYou may want to restrict your umask to prevent other users on the same system\nto access the created file\.\n',
    r'\n您可能需要限制 umask 以防止同一系统上的其他用户\n访问创建的文件。\n', content
)

# "This option does not work with TLS 1.3."
content = re.sub(
    r'\nThis option does not work with TLS 1\.3\.\n',
    r'\n此选项不适用于 TLS 1.3。\n', content
)

# "This option does not work with FTPS or LDAP."
content = re.sub(
    r'\nThis option does not work with FTPS or LDAP\.\n',
    r'\n此选项不适用于 FTPS 或 LDAP。\n', content
)

# "Use "-" as filename to have the output sent to stdout."
content = re.sub(
    r'\nUse "\-" as filename to have the output sent to stdout\. Use "%" as filename to have the output sent to stderr\.\n',
    r'\n使用"-"作为文件名将输出发送到 stdout。使用"%"作为文件名将输出发送到 stderr。\n', content
)
content = re.sub(
    r'\nUse "\-" as filename to have the output sent to stdout\.\n',
    r'\n使用"-"作为文件名将输出发送到 stdout。\n', content
)

# "Note that verbose output of curl activities and network traffic might contain..."
content = re.sub(
    r'\nNote that verbose output of curl activities and network traffic might contain\nsensitive data, including usernames, credentials or secret data content\. Be\naware and be careful when sharing trace logs with others\.\n',
    r'\n请注意，curl 活动和网络流量的详细输出可能包含\n敏感数据，包括用户名、凭据或秘密数据内容。请\n注意并与他人共享跟踪日志时谨慎。\n', content
)

# "Specify a "" filename (zero length) to avoid loading/saving and make curl"
content = re.sub(
    r'\nSpecify a "" filename \(zero length\) to avoid loading/saving and make curl\nhandle the cache in memory\.\n',
    r'\n指定一个""的文件名（长度为零）以避免加载/保存，并让 curl\n在内存中处理缓存。\n', content
)

# "curl passes on the verbatim string you give it in the request without any\nfilter or other safe guards. That includes white space and control characters."
content = re.sub(
    r'\ncurl passes on the verbatim string you give it in the request without any\nfilter or other safe guards\. That includes white space and control characters\.\n',
    r'\ncurl 将您提供的字符串原样传递给请求，不进行任何\n过滤或其他安全检查。这包括空白字符和控制字符。\n', content
)

# "curl uses an exponentially increasing timeout between retries" 
# and similar self-referential text

# "\fBWARNING\fP: ..."
content = re.sub(
    r'\n\\fBWARNING\\fP: this option loosens the SSL security, and by using this flag you\nask for exactly that\.\n',
    r'\n\\fBWARNING\\fP：此选项会降低 SSL 安全性，使用此标志即表示您\n明确要求这么做。\n', content
)

# "WARNING: for server compatibility curl attempts to retry..."
content = re.sub(
    r'\n\\fBWARNING\\fP: For server compatibility curl attempts to retry failed flaky\n',
    r'\n\\fBWARNING\\fP：为了服务器兼容性，curl 尝试尽可能按原始方式重试失败的\n',
    content
)

# === COMMON OPTION DESCRIPTION PATTERNS (single-line) ===

# "(HTTP) ", "(FTP) ", "(TLS) " etc. - keep as-is

# "If <option> is provided several times, the last set value is used."
content = re.sub(
    r'^If (.+?) is provided several times, the last set value is used\.$',
    r'如果多次提供 \1，则使用最后设置的值。',
    content, flags=re.M
)

# "Providing <option> multiple times has no extra effect."
content = re.sub(
    r'^Providing (.+?) multiple times has no extra effect\.$',
    r'多次提供 \1 没有额外效果。',
    content, flags=re.M
)

# "Disable it again with <xxx>."
content = re.sub(
    r'^Disable it again with (.+?)\.$',
    r'使用 \1 再次禁用它。',
    content, flags=re.M
)

# "This option is mutually exclusive with <xxx>."
content = re.sub(
    r'^This option is mutually exclusive with (.+?)\.$',
    r'此选项与 \1 互斥。',
    content, flags=re.M
)

# "See also..."
content = re.sub(r'^See also (.+?)\.$', r'另请参见 \1。', content, flags=re.M)

# "Added in X. See also..."
content = re.sub(
    r'^Added in (\d+\.\d+\.\d+)\. See also (.+?)\.$',
    r'在 \1 中添加。另请参见 \2。',
    content, flags=re.M
)

# "Added in X."
content = re.sub(r'^Added in (\d+\.\d+\.\d+)\.$', r'在 \1 中添加。', content, flags=re.M)

# "This option was formerly known as..."
content = re.sub(
    r'^This option was formerly known as (.+?)\.$',
    r'此选项以前被称为 \1。',
    content, flags=re.M
)

# "That option name can still be used but might be removed in a future version."
content = re.sub(
    r'^That option name can still be used but might be removed in a future version\.$',
    r'该选项名称仍然可以使用，但可能会在未来的版本中移除。',
    content, flags=re.M
)

# "This option is global..."
content = re.sub(
    r'^This option is global and does not need to be specified for each use of \\fI\\-\\-next\\fP\.$',
    r'此选项是全局选项，不需要为每次使用 \\fI\\-\\-next\\fP 指定。',
    content, flags=re.M
)

# Write the result
with open('/tmp/man1_zh/curl.1', 'w') as f:
    f.write(content)

lines_out = content.count('\n') + 1
print(f"Written {lines_out} lines to /tmp/man1_zh/curl.1")
