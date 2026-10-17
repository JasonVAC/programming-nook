#!/usr/bin/env python3
"""Translate misc man page batch 1 (16 tools) from English to Chinese."""
import subprocess
import os
import re

SRC = "/tmp/man1_zh"
DST = "/tmp/man1_zh"
INSTALL_DIR = "/usr/share/man/zh_CN/man1"

SECTION_HEADERS = {
    ".SH NAME": ".SH 名称",
    ".SH SYNOPSIS": ".SH 语法",
    ".SH DESCRIPTION": ".SH 描述",
    ".SH OPTIONS": ".SH 选项",
    ".SH COMMANDS": ".SH 命令",
    ".SH ENVIRONMENT": ".SH 环境变量",
    ".SH SIGNALS": ".SH 信号",
    ".SH NOTES": ".SH 备注",
    ".SH BUGS": ".SH 错误",
    ".SH \"BUGS\"": ".SH 错误",
    ".SH SEE ALSO": ".SH 参见",
    ".SH \"SEE ALSO\"": ".SH 参见",
    ".SH HISTORY": ".SH 历史",
    ".SH AUTHOR": ".SH 作者",
    ".SH AUTHORS": ".SH 作者",
    ".SH \"AUTHORS\"": ".SH 作者",
    ".SH EXAMPLES": ".SH 示例",
    ".SH COPYRIGHT": ".SH 版权",
    ".SH REPORTING BUGS": ".SH 报告错误",
    ".SH \"REPORTING BUGS\"": ".SH 报告错误",
    ".SH AVAILABILITY": ".SH 获取方式",
    ".SH \"AVAILABILITY\"": ".SH 获取方式",
    ".SH HOMEPAGE": ".SH 主页",
    ".SH GETTING STARTED": ".SH 入门",
    ".SH \"GETTING STARTED\"": ".SH 入门",
    ".SH \"COMMAND-LINE OPTIONS\"": ".SH 命令行选项",
    ".SH CONFIGURATION": ".SH 配置",
    ".SH FILE FLAGS": ".SH 文件标志",
    ".SH \"FILE FLAGS\"": ".SH 文件标志",
    ".SH KEY BINDINGS": ".SH 按键绑定",
    ".SH HOMEPAGE": ".SH 主页",
    ".SH \"INFO:\"": ".SH 信息",
    ".SH \"TEXT FORMATTING:\"": ".SH 文本格式",
    ".SH \"COLOR BLOCKS:\"": ".SH 颜色块",
    ".SH \"BARS:\"": ".SH 进度条",
    ".SH \"IMAGE:\"": ".SH 图片",
    ".SH \"OTHERS:\"": ".SH 其他",
    ".SH \"HELP OPTIONS:\"": ".SH 帮助选项",
    ".SH \"Application Options:\"": ".SH 应用程序选项",
    ".SH META OPTIONS": ".SH 元选项",
    ".SH \"META OPTIONS\"": ".SH 元选项",
    ".SH DISPLAY OPTIONS": ".SH 显示选项",
    ".SH \"DISPLAY OPTIONS\"": ".SH 显示选项",
    ".SH FILTERING AND SORTING OPTIONS": ".SH 过滤与排序选项",
    ".SH \"FILTERING AND SORTING OPTIONS\"": ".SH 过滤与排序选项",
    ".SH \"LONG VIEW OPTIONS\"": ".SH 长视图选项",
    ".SH \"GIT OPTIONS\"": ".SH GIT 选项",
    ".SH \"EXAMPLES\"": ".SH 示例",
    ".SH \"KEY BINDINGS\"": ".SH 按键绑定",
}

BOX_TYPES = {
    ".RB A \" yes/no\" \" dialog box": ".RB 一个 \" 是/否\" \" 对话框",
    # More pattern matches will be added inline below
}

def translate_file(name, content):
    """Translate a man page content from English to Chinese."""
    lines = content.split('\n')
    result = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for section headers
        stripped = line.strip()
        
        # Section header translation
        if stripped in SECTION_HEADERS:
            result.append(SECTION_HEADERS[stripped])
            i += 1
            continue
            
        # Subsection headers (.SS)
        if re.match(r'^\.SS\s+"', line):
            # Keep the header as-is for now (most .SS are program names etc)
            result.append(line)
            i += 1
            continue
        if re.match(r'^\.SS\s+', line):
            result.append(line)
            i += 1
            continue
            
        result.append(line)
        i += 1
    
    return '\n'.join(result)


# Now handle each file with specific translations
translations = {}

# ============ sl.1 ============
translations['sl.1'] = """\\\" Copyright 1993,1998,2014 Toyoda Masashi (mtoyoda@acm.org)
.TH SL 1 "March 19, 2019 - Version 5.04"
.SH 名称
sl \\- 显示动画，用于纠正不小心输入 sl 而不是 ls 的用户。
.SH 语法
.B sl
[
.B \\-acdeFlw
]
.SH 描述
.B sl
显示动画，旨在纠正不小心输入 sl 而不是 ls 的用户。SL 代表蒸汽机车（Steam Locomotive）。
.PP
.TP
.B \\-a
发生了事故。人们在呼救。
.TP
.B \\-c
显示 C51 而非 D51。
.TP
.B \\-d
迪斯科模式。动画期间交替变换颜色。
.TP
.B \\-e
退出模式。允许通过 Ctrl+C 中断。
.TP
.B \\-F
像银河铁道999一样飞起来。
.TP
.B \\-G
法式风格（像 Oscar）。
.TP
.B \\-<number of cars>
指定车厢数量，例如 `sl -5`。
.TP
.B \\-l
小号版本。
.TP
.B \\-w
大风天。火车跑得更快。
.TP
.B \\-v
打印版本和最后更新时间。
.PP
.SH 参见
.BR ls (1)
.SH 错误
它有时会列出目录内容。
.SH 作者
Toyoda Masashi (mtoyoda@acm.org)
"""

# ============ cmatrix.1 ============
translations['cmatrix.1'] = """.TH CMatrix 1 "Mon May 3 1999"
.SH 名称
CMatrix \\- 在 Linux 终端中显示类似《黑客帝国》的滚动字符效果
.SH 语法
.B cmatrix
[\\-abBflohnsmVx] [\\-u update] [\\-C color]
.SH 描述
在 Linux 终端中显示类似《黑客帝国》的滚动字符效果。
.SS 选项
.TP
.I "\\-a"
异步滚动
.TP
.I "\\-b"
启用粗体字符
.TP
.I "\\-B"
全部使用粗体字符（覆盖 \\-b）
.TP
.I "\\-f"
强制使用 Linux $TERM 类型
.TP
.I "\\-l"
Linux 模式（在控制台中设置 \"matrix.fnt\" 字体）
.TP
.I "\\-o"
使用旧式滚动
.TP
.I "\\-h, \\-?"
打印帮助信息并退出
.TP
.I "\\-n"
不使用粗体字符（覆盖 \\-b 和 \\-B）
.TP
.I "\\-s"
\"屏幕保护\" 模式，按下任意键即退出
.TP
.I "\\-m"
\"Lambda\" 模式，每个字符都变成 lambda
.TP
.I "\\-x"
X window 模式，如果 xterm 使用 mtx.pcf 时使用
.TP
.I "\\-V"
打印版本信息并退出
.TP
.I "\\-u delay"
屏幕更新延迟 0-9，默认为 4
.TP
.I "\\-C color"
使用此颜色作为矩阵颜色（默认为绿色）。
有效颜色：green、red、blue、white、yellow、cyan、magenta、black。
.SS 按键操作
运行期间可使用以下按键（\\-s 模式下不可用）
.TP
.I "a"
切换异步滚动
.TP
.I "b"
随机粗体字符
.TP
.I "B"
全部粗体字符
.TP
.I "n"
关闭粗体字符
.TP
.I "0\\-9"
调整更新速度
.TP
.I "! @ # $ % ^ & )"
将矩阵颜色更改为对应颜色：
! \\- 红色，@ \\- 绿色，# \\- 黄色，$ \\- 蓝色，% \\- 洋红，^ \\- 青色，
& \\- 白色，) \\- 黑色。
.TP
.I "q"
退出程序
.SH 错误
此程序非常占用 CPU 资源。如果它占用超过 40% 的 CPU 也不必惊讶。
.SH 主页
http://www.github.com/abishekvashok/cmatrix
"""

# ============ write.1 ============
translations['write.1'] = """'\\\" t
.\\\"     Title: write
.\\\"    Author: [see the \"AUTHOR(S)\" section]
.\\\" Generator: Asciidoctor 2.0.26
.\\\"      Date: 2026-06-16
.\\\"    Manual: User Commands
.\\\"    Source: util-linux 2.42.2
.\\\"  Language: English
.\\\"
.TH \"WRITE\" \"1\" \"2026-06-16\" \"util\\-linux 2.42.2\" \"User Commands\"
.ie \\n(.g .ds Aq \\(aq
.el       .ds Aq '
.ss \\n[.ss] 0
.nh
.ad l
.de URL
\\fI\\\\$2\\fP <\\\\$1>\\\\$3
..
.als MTO URL
.if \\n[.g] \\{\\
.  mso www.tmac
.  am URL
.    ad l
.  .
.  am MTO
.    ad l
.  .
.  LINKSTYLE blue R < >
.\\}
.SH 名称
write \\- 向其他用户发送消息
.SH 语法
.sp
\\fBwrite\\fP \\fIuser\\fP [\\fIttyname\\fP]
.SH 描述
.sp
\\fBwrite\\fP 允许你与其他用户通信，通过将你的终端上的行复制到他们的终端上。
.sp
当你运行 \\fBwrite\\fP 命令时，你正在写入的用户会收到如下形式的消息：
.sp
.if n .RS 4
.nf
.fam C
Message from yourname@yourhost on yourtty at hh:mm ...
.fam
.fi
.if n .RE
.sp
你输入的任何后续行都将被复制到指定用户的终端上。如果对方想要回复，也必须运行 \\fBwrite\\fP。
.sp
完成后，输入文件结束符或中断字符。对方将看到消息 \\fBEOF\\fP，表示对话结束。
.sp
你可以使用 \\fBmesg\\fP(1) 命令阻止他人（超级用户除外）向你发送消息。某些命令（例如 \\fBnroff\\fP(1) 和 \\fBpr\\fP(1)）可能会自动禁止写入，以免其产生的输出被覆盖。
.sp
如果你想发送消息的用户在多个终端上登录，可以通过将终端名称作为 \\fBwrite\\fP 命令的第二个操作数来指定写入哪个终端。或者，你可以让 \\fBwrite\\fP 选择其中一个终端 \\- 它会选择空闲时间最短的那个。这样，如果用户既在工作场所登录，又从家中拨号登录，消息将发送到正确的位置。
.sp
传统的写入协议是：字符串 \\fI\\-o\\fP（出现在行尾或单独一行）表示轮到对方发言。字符串 \\fIoo\\fP 表示该人认为对话已结束。
.SH 选项
.sp
\\fB\\-h\\fP, \\fB\\-\\-help\\fP
.RS 4
显示帮助文本并退出。
.RE
.sp
\\fB\\-V\\fP, \\fB\\-\\-version\\fP
.RS 4
显示版本信息并退出。
.RE
.SH 历史
.sp
\\fBwrite\\fP 命令出现在 Version 5 AT&T UNIX（1974 年 6 月）中。
.SH 参见
.sp
\\fBmesg\\fP(1),
\\fBtalk\\fP(1),
\\fBwho\\fP(1)
.SH 报告错误
.sp
如需报告错误，请使用 \\c
.URL \"https://github.com/util\\-linux/util\\-linux/issues\" \"问题跟踪器\" \".\"
.SH 获取方式
.sp
\\fBwrite\\fP 命令是 util\\-linux 软件包的一部分，可以从 \\c
.URL \"https://www.kernel.org/pub/linux/utils/util\\-linux/\" \"Linux Kernel Archive\" \"下载。\"
"""

# ============ notify-send.1 ============
translations['notify-send.1'] = """'\\\" t
.\\\"     Title: notify-send
.\\\"    Author: Andre Filipe de Assuncao e Brito <decko@noisemakers.org>
.\\\" Generator: DocBook XSL Stylesheets v1.79.2 <http://docbook.sf.net/>
.\\\"      Date: November 2005
.\\\"    Manual: User Commands
.\\\"    Source: libnotify
.\\\"  Language: English
.\\\"
.TH \"NOTIFY\\-SEND\" \"1\" \"\" \"libnotify\" \"User Commands\"
.ie \\n(.g .ds Aq \\(aq
.el       .ds Aq '
.nh
.ad l
.SH 名称
notify-send \\- 发送桌面通知的程序
.SH 语法
.HP \\w'\\fBnotify\\-send\\fR\\ 'u
\\fBnotify\\-send\\fR [\\fIOPTIONS\\fR] {\\fIsummary\\fR} [\\fIbody\\fR]
.SH 描述
.PP
通过 \\fBnotify\\-send\\fR，你可以从命令行通过通知守护进程向用户发送桌面通知。这些通知可用于告知用户某个事件或显示某些信息，而不会干扰用户的操作。
.SH 选项
.PP
\\fB\\-?\\fR, \\fB\\-\\-help\\fR
.RS 4
显示帮助信息并退出。
.RE
.PP
\\fB\\-a\\fR, \\fB\\-\\-app\\-name\\fR=\\fIAPP_NAME\\fR
.RS 4
指定通知的应用程序名称。
.RE
.PP
\\fB\\-A\\fR, \\fB\\-\\-action\\fR=[\\fINAME\\fR=]\\fIText\\&.\\&.\\&.\\fR
.RS 4
指定要显示给用户的操作。隐含 \\fB\\-\\-wait\\fR 以等待用户输入。可多次设置。操作的 \\fINAME\\fR 将输出到 stdout。如果未指定 \\fINAME\\fR，则使用选项的数字索引（从 1 开始）。
.RE
.PP
\\fB\\-\\-selected\\-action\\-fd\\fR=\\fIFILE_DESCRIPTOR\\fR
.RS 4
用于写入用户所选操作的文件描述符。
.RE
.PP
\\fB\\-\\-activation\\-token\\-fd\\fR=\\fIFILE_DESCRIPTOR\\fR
.RS 4
用于写入操作激活令牌的文件描述符。守护进程必须支持此功能。
.RE
.PP
\\fB\\-u\\fR, \\fB\\-\\-urgency\\fR=\\fILEVEL\\fR
.RS 4
指定紧急程度（low、normal、critical）。
.RE
.PP
\\fB\\-t\\fR, \\fB\\-\\-expire\\-time\\fR=\\fITIME\\fR
.RS 4
通知在屏幕上显示的持续时间，以毫秒为单位。
.sp
并非所有实现都使用此参数。GNOME Shell 和 Notify OSD 总是忽略它，而 Plasma 则忽略紧急程度为 critical 的通知的此参数。
.RE
.PP
\\fB\\-i\\fR, \\fB\\-\\-icon\\fR=\\fIICON\\fR
.RS 4
指定要显示的图标文件名或内置图标。
.RE
.PP
\\fB\\-n\\fR, \\fB\\-\\-app\\-icon\\fR=\\fIICON\\fR
.RS 4
指定应用程序图标文件名或应用程序图标名称。服务器可能显示也可能不显示。
.RE
.PP
\\fB\\-c\\fR, \\fB\\-\\-category\\fR=\\fITYPE\\fR[,\\fITYPE\\fR\\&...]
.RS 4
指定通知类别。
.RE
.PP
\\fB\\-h\\fR, \\fB\\-\\-hint\\fR=\\fITYPE\\fR:\\fINAME\\fR:\\fIVALUE\\fR
.RS 4
指定要传递的基本额外数据。有效类型有 BOOLEAN、INT、DOUBLE、STRING、BYTE 和 VARIANT。
.RE
.PP
\\fB\\-p\\fR, \\fB\\-\\-print\\-id\\fR
.RS 4
打印通知 ID。
.RE
.PP
\\fB\\-\\-id\\-fd=\\fR\\fB\\fIFILE_DESCRIPTOR\\fR\\fR
.RS 4
用于写入通知 ID 的文件描述符。
.RE
.PP
\\fB\\-r\\fR, \\fB\\-\\-replace\\-id\\fR=\\fIREPLACE_ID\\fR
.RS 4
要替换的通知的 ID。
.RE
.PP
\\fB\\-w\\fR, \\fB\\-\\-wait\\fR
.RS 4
等待通知关闭后再退出。如果设置了 \\fBexpire\\-time\\fR，它将用作最大等待时间。
.RE
.PP
\\fB\\-e\\fR, \\fB\\-\\-transient\\fR
.RS 4
显示临时通知。临时通知会绕过服务器的持久化功能（如果有的话），因此不会被保留直到用户确认。
.RE
.SH 参见
.PP
桌面通知规范参见 \\m[blue]\\fBhttps://specifications\\&.freedesktop\\&.org/notification\\-spec/\\fR\\m[]。
.SH 作者
.PP
\\fBAndre Filipe de Assuncao e Brito\\fR <\\&decko@noisemakers\\&.org\\&>
.RS 4
原作者
.RE
.PP
\\fBPaul van Tilburg\\fR <\\&paulvt@debian\\&.org\\&>
.RS 4
原作者
.RE
.PP
\\fBRiccardo Setti\\fR <\\&giskard@debian\\&.org\\&>
.RS 4
原作者
.RE
"""

# ============ btop.1 ============
translations['btop.1'] = """.TH \"btop\" \"1\" \"2025-05-01\" \"\" \"User Commands\"
.SH 名称
.LP
btop \\- 资源监视器，显示处理器、内存、磁盘、网络和进程的使用情况和统计信息。
.SH 语法
.LP
\\fBbtop\\fR [\\fB\\-c\\fR \\fIfile\\fR] [\\fB\\-d\\fR] [\\fB\\-f\\fR \\fIfilter\\fR] [\\fB\\-l\\fR] [\\fB\\-p\\fR \\fIid\\fR] [\\fB\\-t\\fR] [\\fB\\-u\\fR \\fIms\\fR] [\\fB\\-\\-force-utf\\fR] [\\fB\\-\\-themes-dir\\fR \\fIdir\\fR]
.PP
\\fBbtop\\fR [\\fB\\-\\-default-config\\fR | {\\fB\\-h\\fR | \\fB\\-\\-help\\fR} | {\\fB\\-V\\fR | \\fB\\-\\-version\\fR}]
.SH 描述
.LP
\\fBbtop\\fR 是一个显示处理器、内存、磁盘、网络和进程使用情况及统计信息的程序。
.SH 选项
.LP
该程序遵循通常的 GNU 命令行语法，长选项以两个破折号开头。以下是选项摘要。
.TP 3
\\fB\\-c\\fR, \\fB\\-\\-config \\f(BIfile\\fB\\fR
配置文件的路径。
.TP 3
\\fB\\-d\\fR, \\fB\\-\\-debug\\fR
以调试模式启动，包含额外的日志和指标。
.TP 3
\\fB\\-f\\fR, \\fB\\-\\-filter \\f(BIfilter\\fB\\fR
设置初始进程过滤器。
.TP 3
\\fB\\-\\-force-utf\\fR
强制启动，即使未检测到 UTF-8 区域设置。
.TP 3
\\fB\\-l\\fR, \\fB\\-\\-low-color\\fR
禁用真彩色，仅使用 256 色。
.TP 3
\\fB\\-p\\fR, \\fB\\-\\-preset \\f(BIid\\fB\\fR
使用预设（0-9）启动。
.TP 3
\\fB\\-t\\fR, \\fB\\-\\-tty\\fR
强制 tty 模式，仅使用 ANSI 图形符号和 16 色。
.TP 3
\\fB\\-\\-no-tty\\fR
强制禁用 tty 模式。
.TP 3
\\fB\\-\\-themes-dir \\f(BIdir\\fB\\fR
自定义主题目录的路径。指定后，此目录优先于默认主题搜索路径。
.TP 3
\\fB\\-u\\fR, \\fB\\-\\-update \\f(BIms\\fB\\fR
设置初始更新速率（毫秒）。
.TP 3
\\fB\\-\\-default-config\\fR
将默认配置打印到标准输出。
.TP 3
\\fB\\-h\\fR, \\fB\\-\\-help\\fR
显示选项摘要。
.TP 3
\\fB\\-V\\fR, \\fB\\-\\-version\\fR
显示程序版本。
.SH 错误
.LP
上游错误跟踪器请访问 \\c
.UR https://github.com/aristocratos/btop/issues
.UE \\c
。
.SH 参见
.LP
\\fBtop\\fR(1), \\fBhtop\\fR(1)
.SH 作者
.LP
\\fBbtop\\fR 由 Jakob P. Liljenberg（又名 \"Aristocratos\"）编写。
"""

# ============ gdu.1 ============
translations['gdu.1'] = """.\\\" Automatically generated by Pandoc 3.5
.\\\"
.TH \"gdu\" \"1\" \"2026\\-03\\-31\" \"\"
.SH 名称
gdu \\- 用 Go 编写的相当快速的磁盘使用分析器
.SH 语法
\\f[B]gdu [flags] [directory_to_scan]\\f[R]
.SH 描述
用 Go 编写的相当快速的磁盘使用分析器。
.PP
Gdu 主要用于 SSD 磁盘，可以充分利用并行处理。
不过 HDD 也能正常工作，但性能提升没有那么大。
.SH 选项
\\f[B]\\-h\\f[R], \\f[B]\\-\\-help\\f[R][=false] gdu 的帮助信息
.PP
\\f[B]\\-i\\f[R], \\f[B]\\-\\-ignore\\-dirs\\f[R]=[/proc,/dev,/sys,/run] 要忽略的路径（用逗号分隔）。支持绝对路径和相对路径。
.PP
\\f[B]\\-I\\f[R], \\f[B]\\-\\-ignore\\-dirs\\-pattern\\f[R] 要忽略的路径模式（用逗号分隔）。支持绝对和相对路径模式。
.PP
\\f[B]\\-X\\f[R], \\f[B]\\-\\-ignore\\-from\\f[R] 从文件中读取要忽略的路径模式。支持绝对和相对路径模式。
.PP
\\f[B]\\-T\\f[R], \\f[B]\\-\\-type\\f[R] 要包含的文件类型（例如 \\-\\-type yaml,json）
.PP
\\f[B]\\-E\\f[R], \\f[B]\\-\\-exclude\\-type\\f[R] 要排除的文件类型（例如 \\-\\-exclude\\-type yaml,json）
.PP
\\f[B]\\-\\-max\\-age\\f[R] 包含 mtime 不早于 DURATION 的文件（例如 7d、2h30m、1y2mo）
.PP
\\f[B]\\-\\-min\\-age\\f[R] 包含 mtime 至少为 DURATION 之前的文件（例如 30d、1w）
.PP
\\f[B]\\-\\-since\\f[R] 包含 mtime >= WHEN 的文件。WHEN 接受 RFC3339 时间戳或仅日期 YYYY\\-MM\\-DD（按日历日比较，包含整天）
.PP
\\f[B]\\-\\-until\\f[R] 包含 mtime <= WHEN 的文件。WHEN 接受 RFC3339 时间戳或仅日期 YYYY\\-MM\\-DD
.PP
\\f[B]\\-l\\f[R], \\f[B]\\-\\-log\\-file\\f[R]=\\\"\\/dev\\/null\\\" 日志文件路径
.PP
\\f[B]\\-m\\f[R], \\f[B]\\-\\-max\\-cores\\f[R] 设置 Gdu 将使用的最大 CPU 核心数。
.PP
\\f[B]\\-c\\f[R], \\f[B]\\-\\-no\\-color\\f[R][=false] 不使用彩色输出
.PP
\\f[B]\\-x\\f[R], \\f[B]\\-\\-no\\-cross\\f[R][=false] 不跨越文件系统边界
.PP
\\f[B]\\-H\\f[R], \\f[B]\\-\\-no\\-hidden\\f[R][=false] 忽略隐藏目录（以点开头的目录）
.PP
\\f[B]\\-L\\f[R], \\f[B]\\-\\-follow\\-symlinks\\f[R][=false] 跟踪文件的符号链接，即显示符号链接指向的文件大小（目录的符号链接不会被跟踪）
.PP
\\f[B]\\-n\\f[R], \\f[B]\\-\\-non\\-interactive\\f[R][=false] 不以交互模式运行
.PP
\\f[B]\\-\\-interactive\\f[R][=false] 即使输出不是 TTY 也强制使用交互模式
.PP
\\f[B]\\-p\\f[R], \\f[B]\\-\\-no\\-progress\\f[R][=false] 在非交互模式下不显示进度
.PP
\\f[B]\\-u\\f[R], \\f[B]\\-\\-no\\-unicode\\f[R][=false] 不使用 Unicode 符号（用于大小条）
.PP
\\f[B]\\-s\\f[R], \\f[B]\\-\\-summarize\\f[R][=false] 在非交互模式下仅显示总计
.PP
\\f[B]\\-t\\f[R], \\f[B]\\-\\-top\\f[R][=0] 在非交互模式下仅显示前 X 个最大文件
.PP
\\f[B]\\-d\\f[R], \\f[B]\\-\\-show\\-disks\\f[R][=false] 显示所有已挂载的磁盘
.PP
\\f[B]\\-a\\f[R], \\f[B]\\-\\-show\\-apparent\\-size\\f[R][=false] 显示表面大小
.PP
\\f[B]\\-C\\f[R], \\f[B]\\-\\-show\\-item\\-count\\f[R][=false] 显示目录中的项目数
.PP
\\f[B]\\-k\\f[R], \\f[B]\\-\\-show\\-in\\-kib\\f[R][=false] 在非交互模式下以 KiB（或 kB，如果使用 \\-\\-si）显示大小
.PP
\\f[B]\\-M\\f[R], \\f[B]\\-\\-show\\-mtime\\f[R][=false] 显示目录中项目的最新修改时间
.PP
\\f[B]\\-\\-archive\\-browsing\\f[R][=false] 允许浏览 zip/jar/tar 存档（tar、tar.gz、tar.bz2、tar.xz）
.PP
\\f[B]\\-\\-depth\\f[R][=0] 在非交互模式下显示目录结构直到指定深度（0 表示忽略此标志）
.PP
\\f[B]\\-\\-collapse\\-path\\f[R][=false] 折叠单子目录链
.PP
\\f[B]\\-\\-mouse\\f[R][=false] 使用鼠标
.PP
\\f[B]\\-\\-si\\f[R][=false] 使用十进制 SI 前缀（kB、MB、GB）而不是二进制前缀（KiB、MiB、GiB）显示大小
.PP
\\f[B]\\-\\-no\\-prefix\\f[R][=false] 在非交互模式下以原始数字显示大小，不带任何前缀
.PP
\\f[B]\\-\\-no\\-spawn\\-shell\\f[R][=false] 不允许生成 shell
.PP
\\f[B]\\-\\-no\\-delete\\f[R][=false] 不允许删除
.PP
\\f[B]\\-\\-no\\-view\\-file\\f[R][=false] 不允许查看文件内容
.PP
\\f[B]\\-f\\f[R], \\f[B]\\-\\-input\\-file\\f[R] 从 JSON 文件导入分析。如果文件是 \"\\-\"，则从标准输入读取。
.PP
\\f[B]\\-o\\f[R], \\f[B]\\-\\-output\\-file\\f[R] 将所有信息导出为 JSON 文件。如果文件是 \"\\-\"，则写入标准输出。
.PP
\\f[B]\\-\\-config\\-file\\f[R]=\\\"\\$HOME/.gdu.yaml\\\" 从文件读取配置
.PP
\\f[B]\\-\\-write\\-config\\f[R][=false] 将当前配置写入文件（默认为 $HOME/.gdu.yaml）
.PP
\\f[B]\\-\\-enable\\-profiling\\f[R][=false] 启用性能分析数据收集，并在 http://localhost:6060/debug/pprof/ 上提供
.PP
\\f[B]\\-D\\f[R], \\f[B]\\-\\-db\\f[R] 将分析结果存储在数据库中（SQLite 使用 .sqlite，BadgerDB 使用 .badger）
.PP
\\f[B]\\-r\\f[R], \\f[B]\\-\\-read\\-from\\-storage\\f[R][=false] 使用现有数据库而不是重新扫描
.PP
\\f[B]\\-v\\f[R], \\f[B]\\-\\-version\\f[R][=false] 打印版本
.SH 文件标志
文件和目录可能以一个字符的标志作为前缀，含义如下：
.TP
\\f[B]!\\f[R]
读取此目录时发生错误。
.TP
\\f[B].\\f[R]
读取子目录时发生错误，大小可能不正确。
.TP
\\f[B]@\\f[R]
文件是符号链接或套接字。
.TP
\\f[B]H\\f[R]
相同的文件已被计数（硬链接）。
.TP
\\f[B]e\\f[R]
目录为空。
"""

# ============ pg.1 ============
translations['pg.1'] = """'\\\" t
.\\\"     Title: pg
.\\\"    Author: [see the \"AUTHOR(S)\" section]
.\\\" Generator: Asciidoctor 2.0.26
.\\\"      Date: 2026-06-16
.\\\"    Manual: User Commands
.\\\"    Source: util-linux 2.42.2
.\\\"  Language: English
.\\\"
.TH \"PG\" \"1\" \"2026-06-16\" \"util\\-linux 2.42.2\" \"User Commands\"
.ie \\n(.g .ds Aq \\(aq
.el       .ds Aq '
.ss \\n[.ss] 0
.nh
.ad l
.de URL
\\fI\\\\$2\\fP <\\\\$1>\\\\$3
..
.als MTO URL
.if \\n[.g] \\{\\
.  mso www.tmac
.  am URL
.    ad l
.  .
.  am MTO
.    ad l
.  .
.  LINKSTYLE blue R < >
.\\}
.SH 名称
pg \\- 逐页浏览文本文件
.SH 语法
.sp
\\fBpg\\fP \\fB\\-*\\fIamount\\fP *\\-p\\fP \\fIprompt\\fP \\fB\\-cefnrs\\fP +line +/pattern/ file_ .\\|.\\|.
.SH 描述
.sp
\\fBpg\\fP 在 CRT 上一次显示一屏文本文件的内容。每页之后会显示一个提示符。用户可以按回车键查看下一页，或按下述键之一。
.sp
如果命令行中没有给出文件名，\\fBpg\\fP 从标准输入读取。如果标准输出不是终端，\\fBpg\\fP 的行为类似 \\fBcat\\fP(1)，但如果文件超过一个，会在每个文件前面加上文件名。
.sp
如果输入来自管道，\\fBpg\\fP 在读取时将数据存储在缓冲区文件中，以便进行导航。
.SH 选项
.sp
\\fBpg\\fP 接受以下选项：
.sp
\\fB+\\fP\\fInumber\\fP
.RS 4
从给定的行号开始。
.RE
.sp
\\fB+/\\fP\\fIpattern\\fP*/*
.RS 4
从包含给定基本正则表达式 \\fIpattern\\fP 的行开始。
.RE
.sp
\\fB\\-\\fP\\fInumber\\fP
.RS 4
每页的行数。默认情况下，这是 CRT 行数减一。
.RE
.sp
\\fB\\-c\\fP
.RS 4
如果终端的 terminfo 条目提供了此功能，则在显示页面之前清除屏幕。
.RE
.sp
\\fB\\-e\\fP
.RS 4
在文件末尾不暂停，不显示 \\fI(EOF)\\fP。
.RE
.sp
\\fB\\-f\\fP
.RS 4
不拆分长行。
.RE
.sp
\\fB\\-n\\fP
.RS 4
不使用此选项时，命令必须用换行符结束。
.sp
使用此选项时，\\fBpg\\fP 在输入命令字母后立即前进。
.RE
.sp
\\fB\\-p\\fP \\fIstring\\fP
.RS 4
显示 \\fIstring\\fP 而不是正常的提示符 \\fI:\\fP。如果 \\fIstring\\fP 包含 \\fB%d\\fP，它的第一次出现将被当前页号替换。
.RE
.sp
\\fB\\-r\\fP
.RS 4
禁止 shell 转义。
.RE
.sp
\\fB\\-s\\fP
.RS 4
如果终端的 terminfo 条目提供了此功能，则以 \\fI高亮\\fP 模式打印消息。
.RE
.sp
\\fB\\-h\\fP, \\fB\\-\\-help\\fP
.RS 4
显示帮助文本并退出。
.RE
.sp
\\fB\\-V\\fP, \\fB\\-\\-version\\fP
.RS 4
显示版本信息并退出。
.RE
.SH 命令
.sp
可以在提示符处输入以下命令。本文档中以 \\fIi\\fP 为前缀的命令接受一个正数或负数作为参数。如果此参数以 \\fB+\\fP 或 \\fB\\-\\fP 开头，则相对于输入文件中的当前位置进行解释，否则相对于文件开头。
.sp
\\fIi\\fP\\fB<Enter>\\fP
.RS 4
显示下一页或指定页。
.RE
.sp
\\fIi\\fP\\fBd\\fP 或 \\fB^D\\fP
.RS 4
显示下半页。如果给出了 \\fIi\\fP，它始终相对于当前位置解释。
.RE
.sp
\\fIi\\fP\\fBl\\fP
.RS 4
显示下一行或指定行。
.RE
.sp
\\fIi\\fP\\fBf\\fP
.RS 4
向前跳一页。\\fIi\\fP 必须为正数，并且始终相对于当前位置解释。
.RE
.sp
\\fIi\\fP\\fBw\\fP 或 \\fIi\\fP\\fBz\\fP
.RS 4
与 \\fB<Enter>\\fP 相同，但 \\fIi\\fP 成为新的页面大小。
.RE
.sp
\\fB.\\fP 或 \\fB^L\\fP
.RS 4
重绘屏幕。
.RE
.sp
\\fB$\\fP
.RS 4
前进到输入文件的最后一行。
.RE
.sp
\\fIi\\fP\\fB/\\fP\\fIpattern\\fP\\fB/\\fP
.RS 4
向前搜索，直到找到基本正则表达式 \\fIpattern\\fP 的第一次或第 \\fIi\\fP 次出现。搜索从当前页之后开始，到文件末尾停止。不进行回绕。\\fIi\\fP 必须为正数。
.RE
.sp
\\fIi\\fP\\fB?\\fP\\fIpattern\\fP\\fB?\\fP 或 \\fIi\\fP\\fB\\fP\\fIpattern\\fP\\fB\\fP
.RS 4
向后搜索，直到找到基本正则表达式 \\fIpattern\\fP 的第一次或第 \\fIi\\fP 次出现。搜索从当前页之前开始，到文件开头停止。不进行回绕。\\fIi\\fP 必须为正数。
.RE
.sp
搜索命令接受一个附加字母。如果给出 \\fBt\\fP，包含模式的行显示在屏幕顶部，这是默认设置。\\fBm\\fP 选择屏幕中间，\\fBb\\fP 选择屏幕底部。所选位置也会用于后续搜索。
.sp
\\fIi\\fP\\fBn\\fP
.RS 4
前进到下一个文件或向前 \\fIi\\fP 个文件。
.RE
.sp
\\fIi\\fP\\fBp\\fP
.RS 4
重新读取上一个文件或向后 \\fIi\\fP 个文件。
.RE
.sp
\\fBs\\fP \\fIfilename\\fP
.RS 4
将当前文件保存到给定的 \\fIfilename\\fP。
.RE
.sp
\\fBh\\fP
.RS 4
显示命令摘要。
.RE
.sp
\\fB!\\fP\\fIcommand\\fP
.RS 4
使用 shell 执行 \\fIcommand\\fP。
.RE
.sp
\\fBq\\fP 或 \\fBQ\\fP
.RS 4
退出。
.RE
.sp
如果用户在 \\fBpg\\fP 从输入文件读取或向终端写入时按下中断键或退出键，\\fBpg\\fP 将立即显示提示符。在所有其他情况下，这些键将终止 \\fBpg\\fP。
.SH 环境变量
.sp
以下环境变量会影响 \\fBpg\\fP 的行为：
.sp
\\fBCOLUMNS\\fP
.RS 4
如果设置，覆盖系统提供的列数。
.RE
.sp
\\fBLANG\\fP, \\fBLC_ALL\\fP, \\fBLC_COLLATE\\fP, \\fBLC_CTYPE\\fP, \\fBLC_MESSAGES\\fP
.RS 4
参见 \\fBlocale\\fP(7)。
.RE
.sp
\\fBLINES\\fP
.RS 4
如果设置，覆盖系统提供的行数。
.RE
.sp
\\fBSHELL\\fP
.RS 4
由 \\fB!\\fP 命令使用。
.RE
.sp
\\fBTERM\\fP
.RS 4
确定终端类型。
.RE
.SH 备注
.sp
\\fBpg\\fP 期望终端制表符设置为每 8 个位置一个。
.sp
包含 NUL 字符的文件无法由 \\fBpg\\fP 显示。
.SH 参见
.sp
\\fBcat\\fP(1),
\\fBmore\\fP(1),
\\fBsh\\fP(1p),
\\fBterminfo\\fP(5),
\\fBlocale\\fP(7),
\\fBregex\\fP(7),
\\fBterm\\fP(7)
.SH 报告错误
.sp
如需报告错误，请使用 \\c
.URL \"https://github.com/util\\-linux/util\\-linux/issues\" \"问题跟踪器\" \".\"
.SH 获取方式
.sp
\\fBpg\\fP 命令是 util\\-linux 软件包的一部分，可以从 \\c
.URL \"https://www.kernel.org/pub/linux/utils/util\\-linux/\" \"Linux Kernel Archive\" \"下载。\"
"""

# ============ script.1 ============
translations['script.1'] = """'\\\" t
.\\\"     Title: script
.\\\"    Author: [see the \"AUTHOR(S)\" section]
.\\\" Generator: Asciidoctor 2.0.26
.\\\"      Date: 2026-06-16
.\\\"    Manual: User Commands
.\\\"    Source: util-linux 2.42.2
.\\\"  Language: English
.\\\"
.TH \"SCRIPT\" \"1\" \"2026-06-16\" \"util\\-linux 2.42.2\" \"User Commands\"
.ie \\n(.g .ds Aq \\(aq
.el       .ds Aq '
.ss \\n[.ss] 0
.nh
.ad l
.de URL
\\fI\\\\$2\\fP <\\\\$1>\\\\$3
..
.als MTO URL
.if \\n[.g] \\{\\
.  mso www.tmac
.  am URL
.    ad l
.  .
.  am MTO
.    ad l
.  .
.  LINKSTYLE blue R < >
.\\}
.SH 名称
script \\- 制作终端会话的打字稿
.SH 语法
.sp
\\fBscript\\fP [options] [\\fIfile\\fP] [\\fB\\-\\-\\fP \\fIcommand\\fP [\\fIargument\\fP.\\|.\\|.]]
.SH 描述
.sp
\\fBscript\\fP 制作你的终端会话中所有内容的打字稿。终端数据以原始形式存储到日志文件中，时序信息存储到另一个（可选的）结构化日志文件中。时序日志文件是稍后通过 \\fBscriptreplay\\fP(1) 回放会话以及存储有关会话的附加信息所必需的。
.sp
从版本 2.35 开始，\\fBscript\\fP 支持多流，并允许将输入和输出记录到单独的文件或同一个文件中。此版本还支持一种新的时序文件，该文件记录了额外的信息。命令 \\fBscriptreplay \\-\\-summary\\fP 会提供所有这些信息。
.sp
如果给出了参数 \\fIfile\\fP 或选项 \\fB\\-\\-log\\-out\\fP \\fIfile\\fP，\\fBscript\\fP 将对话保存在此 \\fIfile\\fP 中。如果没有给出文件名，对话将保存在文件 \\fItypescript\\fP 中。
.sp
请注意，使用 \\fB\\-\\-log\\-in\\fP 或 \\fB\\-\\-log\\-io\\fP 记录输入可能会记录安全敏感信息，因为日志文件包含所有终端会话输入（例如密码），与终端回显标志设置无关。
.SH 选项
.sp
下面，\\fIsize\\fP 参数后面可以跟乘法后缀 KiB (=1024)、MiB (=1024*1024) 等，适用于 GiB、TiB、PiB、EiB、ZiB 和 YiB（\"iB\" 是可选的，例如 \"K\" 与 \"KiB\" 含义相同），或者后缀 KB (=1000)、MB (=1000*1000) 等，适用于 GB、TB、PB、EB、ZB 和 YB。
.sp
\\fB\\-a\\fP, \\fB\\-\\-append\\fP
.RS 4
将输出追加到 \\fIfile\\fP 或 \\fItypescript\\fP，保留之前的内容。
.RE
.sp
\\fB\\-c\\fP, \\fB\\-\\-command\\fP \\fIcommand\\fP
.RS 4
运行 \\fIcommand\\fP 而不是交互式 shell。这使得脚本可以轻松捕获在 stdout 不是 tty 时行为不同的程序的输出。除了使用 \\fB\\-c\\fP 选项外，\\fIcommand\\fP 也可以在双破折号（\\fB\\-\\-\\fP）之后指定。
.RE
.sp
\\fB\\-E\\fP, \\fB\\-\\-echo\\fP \\fIwhen\\fP
.RS 4
此选项控制会话伪终端从端的 \\fBECHO\\fP 标志。支持的模式有 \\fIalways\\fP、\\fInever\\fP 或 \\fIauto\\fP。
.sp
默认值是 \\fIauto\\fP \\-\\- 在这种情况下，为伪终端从端启用 \\fBECHO\\fP；如果当前标准输入是终端，则为其禁用 \\fBECHO\\fP 以防止双重回显；如果当前标准输入不是终端（例如管道：\\fBecho date | script\\fP），则为伪终端从端保持 \\fBECHO\\fP 启用，使得标准输入数据可以在记录到会话日志的同时显示在屏幕上。
.sp
请注意，\\*(Aqnever\\*(Aq 模式会影响会话输出日志的内容，因为用户输入不会在输出中重复。
.RE
.sp
\\fB\\-e\\fP, \\fB\\-\\-return\\fP
.RS 4
返回子进程的退出状态。使用与 bash 信号终止相同的格式（即退出状态为 128 + 信号编号）。子进程的退出状态也会始终存储在打字稿文件中。
.RE
.sp
\\fB\\-f\\fP, \\fB\\-\\-flush\\fP
.RS 4
每次写入后刷新输出。这对远程协作很方便：一个人执行 \\fBmkfifo\\fP \\fIfoo\\fP；\\fBscript \\-f\\fP \\fIfoo\\fP，另一个人可以使用 \\fBcat\\fP \\fIfoo\\fP 实时监控正在做的事情。请注意，刷新会影响性能；可以使用 \\fBSIGUSR1\\fP 按需刷新日志。
.RE
.sp
\\fB\\-\\-force\\fP
.RS 4
允许默认输出文件 \\fItypescript\\fP 是硬链接或符号链接。该命令会跟随符号链接。
.RE
.sp
\\fB\\-B\\fP, \\fB\\-\\-log\\-io\\fP \\fIfile\\fP
.RS 4
将输入和输出记录到同一个 \\fIfile\\fP 中。注意，此选项仅在同时指定 \\fB\\-\\-log\\-timing\\fP 时才有意义，否则无法从日志文件中分离出输出和输入流。
.RE
.sp
\\fB\\-I\\fP, \\fB\\-\\-log\\-in\\fP \\fIfile\\fP
.RS 4
将输入记录到 \\fIfile\\fP 中。如果仅指定了 \\fB\\-\\-log\\-in\\fP，则日志输出被禁用。
.sp
请小心使用此日志功能，因为它会记录所有输入，包括终端禁用回显标志时的输入（例如密码输入）。
.RE
.sp
\\fB\\-O\\fP, \\fB\\-\\-log\\-out\\fP \\fIfile\\fP
.RS 4
将输出记录到 \\fIfile\\fP 中。默认情况下，如果未给出 \\fB\\-\\-log\\-out\\fP 或 \\fB\\-\\-log\\-in\\fP 选项，则输出记录到名为 \\fItypescript\\fP 的文件中。如果仅指定了 \\fB\\-\\-log\\-in\\fP，则日志输出被禁用。
.RE
.sp
\\fB\\-T\\fP, \\fB\\-\\-log\\-timing\\fP \\fIfile\\fP
.RS 4
将时序信息记录到 \\fIfile\\fP 中。目前支持两种时序文件格式。当仅启用一个流（输入或输出）记录时，使用经典格式。当使用 \\fB\\-\\-log\\-io\\fP 或同时使用 \\fB\\-\\-log\\-in\\fP 和 \\fB\\-\\-log\\-out\\fP 时，使用多流格式。另请参见 \\fB\\-\\-logging\\-format\\fP。
.RE
.sp
\\fB\\-m\\fP, \\fB\\-\\-logging\\-format\\fP \\fIformat\\fP
.RS 4
强制使用 \\fIadvanced\\fP 或 \\fIclassic\\fP 时序日志格式。默认是仅记录输出时使用经典格式，当请求同时记录输入和输出时使用高级格式。
.sp
\\fB经典格式\\fP
.RS 4
时序日志包含两个字段，以空格分隔。第一个字段表示自上次输出以来经过的时间。第二个字段表示此次输出的字符数。
.RE
.sp
\\fB高级（多流）格式\\fP
.RS 4
第一个字段是条目类型标识符（\\*(AqI\\*(Aq 输入，\\*(AqO\\*(Aq 输出，\\*(AqH\\*(Aq 头部，\\*(AqS\\*(Aq 信号）。第二个字段是自上一个条目以来经过的时间，条目的其余部分是与类型相关的数据。
.RE
.RE
.sp
\\fB\\-o\\fP, \\fB\\-\\-output\\-limit\\fP \\fIsize\\fP
.RS 4
将打字稿和时序文件的大小限制为 \\fIsize\\fP，并在超出此大小后停止子进程。计算的文件大小不包括 \\fBscript\\fP 命令在子进程输出前后添加的开始和完成消息。由于缓冲，生成的输出文件可能大于指定值。
.RE
.sp
\\fB\\-q\\fP, \\fB\\-\\-quiet\\fP
.RS 4
安静模式（不将开始和完成消息写入标准输出）。
.RE
.sp
\\fB\\-t\\fP[\\fIfile\\fP], \\fB\\-\\-timing\\fP[\\fB=\\fP\\fIfile\\fP]
.RS 4
将时序数据输出到标准错误，如果给定 \\fIfile\\fP 则输出到该文件。此选项已弃用，建议使用 \\fB\\-\\-log\\-timing\\fP，其中 \\fIfile\\fP 参数不是可选的。
.RE
.sp
\\fB\\-h\\fP, \\fB\\-\\-help\\fP
.RS 4
显示帮助文本并退出。
.RE
.sp
\\fB\\-V\\fP, \\fB\\-\\-version\\fP
.RS 4
显示版本信息并退出。
.RE
.SH 信号
.sp
收到 \\fBSIGUSR1\\fP 后，\\fBscript\\fP 会立即刷新输出文件。
.SH 环境变量
.sp
\\fBscript\\fP 使用以下环境变量：
.sp
\\fBSHELL\\fP
.RS 4
如果变量 \\fBSHELL\\fP 存在，\\fBscript\\fP 派生的 shell 将是该 shell。如果未设置 \\fBSHELL\\fP，则假定使用 Bourne shell。（大多数 shell 会自动设置此变量）。
.RE
.SH 备注
.sp
当派生的 shell 退出时脚本结束（对于 Bourne shell（\\fBsh\\fP(1p)）使用 \\fIcontrol\\-D\\fP，对于 C-shell（\\fBcsh\\fP(1)）使用 \\fIexit\\fP、\\fIlogout\\fP 或 \\fIcontrol\\-d\\fP（如果未设置 \\fIignoreeof\\fP））。
.sp
某些交互式命令（例如 \\fBvi\\fP(1)）会在打字稿文件中产生垃圾数据。\\fBscript\\fP 最适合与不操作屏幕的命令一起使用，其结果旨在模拟硬拷贝终端。
.sp
不建议在非交互式 shell 中运行 \\fBscript\\fP。\\fBscript\\fP 的内部 shell 始终是交互式的，这可能导致意外结果。如果在 shell 初始化文件中使用 \\fBscript\\fP，必须避免进入无限循环。例如，可以使用仅由登录 shell 读取的 \\fB.profile\\fP 文件：
.sp
.if n .RS 4
.nf
.fam C
if test -t 0 ; then
    script
    exit
fi
.fam
.fi
.if n .RE
.sp
还应避免在命令管道中使用 \\fBscript\\fP，因为 \\fBscript\\fP 可能读取比预期更多的输入。
.SH 历史
.sp
\\fBscript\\fP 命令出现在 3.0BSD 中。
.SH 错误
.sp
\\fBscript\\fP 将 \\fI所有内容\\fP 放入日志文件中，包括换行符和退格符。这不是天真用户所期望的。
.sp
\\fBscript\\fP 主要设计用于交互式终端会话。当 stdin 不是终端时（例如：\\fBecho foo | script\\fP），会话可能会挂起，因为脚本会话内的交互式 shell 缺乏 EOF，而 \\fBscript\\fP 不知道何时关闭会话。有关更多信息，请参阅 \\fB备注\\fP 部分。
.SH 参见
.sp
\\fBcsh\\fP(1)（用于 \\fIhistory\\fP 机制），
\\fBscriptreplay\\fP(1),
\\fBscriptlive\\fP(1)
.SH 报告错误
.sp
如需报告错误，请使用 \\c
.URL \"https://github.com/util\\-linux/util\\-linux/issues\" \"问题跟踪器\" \".\"
.SH 获取方式
.sp
\\fBscript\\fP 命令是 util\\-linux 软件包的一部分，可以从 \\c
.URL \"https://www.kernel.org/pub/linux/utils/util\\-linux/\" \"Linux Kernel Archive\" \"下载。\"
"""

# ============ scriptreplay.1 ============
translations['scriptreplay.1'] = """'\\\" t
.\\\"     Title: scriptreplay
.\\\"    Author: [see the \"AUTHOR(S)\" section]
.\\\" Generator: Asciidoctor 2.0.26
.\\\"      Date: 2026-06-16
.\\\"    Manual: User Commands
.\\\"    Source: util-linux 2.42.2
.\\\"  Language: English
.\\\"
.TH \"SCRIPTREPLAY\" \"1\" \"2026-06-16\" \"util\\-linux 2.42.2\" \"User Commands\"
.ie \\n(.g .ds Aq \\(aq
.el       .ds Aq '
.ss \\n[.ss] 0
.nh
.ad l
.de URL
\\fI\\\\$2\\fP <\\\\$1>\\\\$3
..
.als MTO URL
.if \\n[.g] \\{\\
.  mso www.tmac
.  am URL
.    ad l
.  .
.  am MTO
.    ad l
.  .
.  LINKSTYLE blue R < >
.\\}
.SH 名称
scriptreplay \\- 使用时序信息回放打字稿
.SH 语法
.sp
\\fBscriptreplay\\fP [options] \\fItimingfile\\fP [\\fItypescript\\fP [\\fIdivisor\\fP]]
.SH 描述
.sp
该程序回放打字稿，使用时序信息确保输出以与最初记录脚本时相同的节奏进行。
.sp
回放仅仅是再次显示信息；记录打字稿时运行的程序 \\fB不会再次运行\\fP。由于只是显示相同的信息，\\fBscriptreplay\\fP 只有在与记录打字稿时使用的终端类型相同的终端上运行时才能保证正常工作。否则，打字稿中的任何转义字符可能会被 \\fBscriptreplay\\fP 发送到的终端以不同方式解释。
.sp
时序信息是 \\fBscript\\fP(1) 通过 \\fB\\-\\-log\\-timing\\fP 选项输出到文件的内容。
.sp
默认情况下，要显示的 \\fItypescript\\fP 假定名为 \\fBtypescript\\fP，但可以通过第二个参数或 \\fB\\-\\-log\\-out\\fP 选项指定其他文件名。
.sp
如果指定了第三个参数或 \\fB\\-\\-divisor\\fP，它将用作加速乘数。例如，加速 2 使 \\fBscriptreplay\\fP 快两倍，减速 0.1 使其比原始会话慢十倍。
.sp
在回放期间，你可以使用上箭头、下箭头、空格和右箭头键交互式地加速、减速、暂停或单步播放。
.SH 选项
.sp
\\fB\\-I\\fP, \\fB\\-\\-log\\-in\\fP \\fIfile\\fP
.RS 4
包含 \\fBscript\\fP 终端输入的文件。
.RE
.sp
\\fB\\-O\\fP, \\fB\\-\\-log\\-out\\fP \\fIfile\\fP
.RS 4
包含 \\fBscript\\fP 终端输出的文件。
.RE
.sp
\\fB\\-B\\fP, \\fB\\-\\-log\\-io\\fP \\fIfile\\fP
.RS 4
包含 \\fBscript\\fP 终端输出和输入的文件。
.RE
.sp
\\fB\\-t\\fP, \\fB\\-\\-timing\\fP \\fIfile\\fP
.RS 4
包含 \\fBscript\\fP 时序输出的文件。此选项替代 \\fItimingfile\\fP 位置参数。
.RE
.sp
\\fB\\-T\\fP, \\fB\\-\\-log\\-timing\\fP \\fIfile\\fP
.RS 4
这是 \\fB\\-t\\fP 的别名，为了与 \\fBscript\\fP(1) 命令行选项保持兼容而保留。
.RE
.sp
\\fB\\-s\\fP, \\fB\\-\\-typescript\\fP \\fIfile\\fP
.RS 4
已弃用的 \\fB\\-\\-log\\-out\\fP 别名。
.RE
.sp
\\fB\\-c\\fP, \\fB\\-\\-cr\\-mode\\fP \\fImode\\fP
.RS 4
指定如何处理日志文件中的 CR（回车，0x0D）字符。默认模式是 \\fBauto\\fP，在这种情况下，stdin 日志中的 CR 会被替换为换行符，否则 \\fBscriptreplay\\fP 会覆盖同一行。其他模式是 \\fBnever\\fP 和 \\fBalways\\fP。
.RE
.sp
\\fB\\-d\\fP, \\fB\\-\\-divisor\\fP \\fInumber\\fP
.RS 4
以 \\fInumber\\fP 倍的加速比回放。参数是浮点数。之所以称为 divisor，是因为它用此因子除时序。此选项覆盖旧式参数。
.RE
.sp
\\fB\\-m\\fP, \\fB\\-\\-maxdelay\\fP \\fInumber\\fP
.RS 4
将更新之间的最大延迟设置为 \\fInumber\\fP 秒。参数是浮点数。这可用于避免打字稿回放中的长暂停。
.RE
.sp
\\fB\\-\\-summary\\fP
.RS 4
显示指定时序文件中记录的会话详细信息并退出。会话必须使用 \\fBadvanced\\fP 格式记录（有关更多详细信息，请参见 \\fBscript\\fP(1) 选项 \\fB\\-\\-logging\\-format\\fP）。
.RE
.sp
\\fB\\-x\\fP, \\fB\\-\\-stream\\fP \\fItype\\fP
.RS 4
强制 \\fBscriptreplay\\fP 仅打印指定的流。支持的流类型有 \\fBin\\fP、\\fBout\\fP、\\fBsignal\\fP 和 \\fBinfo\\fP。此选项推荐用于多流日志（通过 \\fB\\-\\-log\\-io\\fP 创建），以便仅打印所需数据。
.RE
.sp
\\fB\\-h\\fP, \\fB\\-\\-help\\fP
.RS 4
显示帮助文本并退出。
.RE
.sp
\\fB\\-V\\fP, \\fB\\-\\-version\\fP
.RS 4
显示版本信息并退出。
.RE
.SH 示例
.sp
.if n .RS 4
.nf
.fam C
% script \\-\\-log\\-timing file.tm \\-\\-log\\-out script.out
Script started, file is script.out
% ls
<etc, etc>
% exit
Script done, file is script.out
% scriptreplay \\-\\-log\\-timing file.tm \\-\\-log\\-out script.out
.fam
.fi
.if n .RE
.SH 按键绑定
.sp
以下按键控制脚本的播放：
.sp
.RS 4
.ie n \\{\\
\\h'-04'\\(bu\\h'+03'\\c
.\\}
.el \\{\\
.  sp -1
.  IP \\(bu 2.3
.\\}
\\fBSpace\\fP：切换暂停和继续。按此键暂停播放，再按一次继续。
.RE
.sp
.RS 4
.ie n \\{\\
\\h'-04'\\(bu\\h'+03'\\c
.\\}
.el \\{\\
.  sp -1
.  IP \\(bu 2.3
.\\}
\\fBUp Arrow\\fP：增加播放速度。每按一次此键，脚本回放速度加快 x0.1。
.RE
.sp
.RS 4
.ie n \\{\\
\\h'-04'\\(bu\\h'+03'\\c
.\\}
.el \\{\\
.  sp -1
.  IP \\(bu 2.3
.\\}
\\fBDown Arrow\\fP：降低播放速度。每按一次此键，脚本回放速度减慢 x0.1。
.RE
.sp
.RS 4
.ie n \\{\\
\\h'-04'\\(bu\\h'+03'\\c
.\\}
.el \\{\\
.  sp -1
.  IP \\(bu 2.3
.\\}
\\fBRight Arrow\\fP：单步前进播放。每按一次此键，立即显示当前步骤，而不是等待其指定的延迟。
.RE
.SH 作者
.sp
原始的 \\fBscriptreplay\\fP 程序由 \\c
.MTO \"joey\\(atkitenet.net\" \"Joey Hess\" \"编写。\"
该程序由 \\c
.MTO \"jay\\(atgnu.org\" \"James Youngman\" \"\"
和 \\c
.MTO \"kzak\\(atredhat.com\" \"Karel Zak\" \"\"
用 C 语言重写。
.SH 版权
.sp
Copyright \\u00A9 2008 James Youngman
.sp
Copyright \\u00A9 2008\\-2019 Karel Zak
.sp
Copyright \\u00A9 2024 Jonathan Ketchker
.sp
这是自由软件；有关复制条件，请参见源代码。不提供任何担保；甚至不保证适销性或特定用途的适用性。
.sp
根据 GNU General Public License version 2 或更高版本发布。
.SH 参见
.sp
\\fBscript\\fP(1),
\\fBscriptlive\\fP(1)
.SH 报告错误
.sp
如需报告错误，请使用 \\c
.URL \"https://github.com/util\\-linux/util\\-linux/issues\" \"问题跟踪器\" \".\"
.SH 获取方式
.sp
\\fBscriptreplay\\fP 命令是 util\\-linux 软件包的一部分，可以从 \\c
.URL \"https://www.kernel.org/pub/linux/utils/util\\-linux/\" \"Linux Kernel Archive\" \"下载。\"
"""

print("Translation strings prepared for 10 of 16 files.")
print("Now writing translated files and installing...")
