#!/usr/bin/env python3
"""Fast pattern-based man page translator for remaining pages."""
import gzip, os, re, sys, subprocess, glob

SRC = "/usr/share/man/man1/"
DEST = "/tmp/man1_zh/"
INST = "/usr/share/man/zh_CN/man1/"

SH_MAP = {
    "NAME": "名称", "SYNOPSIS": "概述", "DESCRIPTION": "描述",
    "OPTIONS": "选项", "EXAMPLES": "示例", "EXAMPLE": "示例",
    "AUTHOR": "作者", "AUTHORS": "作者", "SEE ALSO": "另请参见",
    "FILES": "文件", "EXIT STATUS": "退出状态", "ENVIRONMENT": "环境变量",
    "BUGS": "错误", "NOTES": "注意事项", "DIAGNOSTICS": "诊断",
    "COPYRIGHT": "版权", "REPORTING BUGS": "报告错误",
    "AVAILABILITY": "可用性", "HISTORY": "历史",
    "CONFIGURATION": "配置", "RETURN VALUE": "返回值",
    "ERRORS": "错误", "STANDARDS": "标准",
    "SECURITY": "安全", "LICENSE": "许可证", "LICENSE": "许可证",
    "COMMANDS": "命令", "USAGE": "用法", "OVERVIEW": "概述",
    "INPUT": "输入", "OUTPUT": "输出", "WARNING": "警告",
    "CAVEATS": "注意事项", "LIMITATIONS": "限制",
    "REQUIREMENTS": "要求", "INSTALLATION": "安装",
    "DEPENDENCIES": "依赖", "COMPATIBILITY": "兼容性",
    "OPERANDS": "操作数", "SUBCOMMANDS": "子命令",
    "TROUBLESHOOTING": "故障排除", "REFERENCES": "参考",
    "COMMENTS": "备注", "ADDITIONAL INFORMATION": "附加信息",
    "SEE ALSO": "另请参见", "FORMATS": "格式",
    "DEFAULTS": "默认值", "ALGORITHM": "算法",
    "PROTOCOL": "协议", "SIGNALS": "信号",
    "STDIN": "标准输入", "STDOUT": "标准输出",
    "RETURNED VALUE": "返回值",
}

# Common man page phrase translations (longest first for greedy matching)
PHRASES = [
    ("Display this help and exit", "显示此帮助并退出"),
    ("display this help and exit", "显示此帮助并退出"),
    ("display help and exit", "显示帮助并退出"),
    ("Display help message", "显示帮助消息"),
    ("print this help and exit", "打印此帮助并退出"),
    ("print this help, then exit", "打印此帮助并退出"),
    ("Print help and exit", "打印帮助并退出"),
    ("print help and exit", "打印帮助并退出"),
    ("output version information and exit", "输出版本信息并退出"),
    ("Output version information and exit", "输出版本信息并退出"),
    ("display version and copyright information and exit", "显示版本和版权信息并退出"),
    ("Display version and exit", "显示版本信息并退出"),
    ("display version and exit", "显示版本信息并退出"),
    ("print version number, then exit", "打印版本号并退出"),
    ("Print version and exit", "打印版本并退出"),
    ("print version and exit", "打印版本并退出"),
    ("Show version information", "显示版本信息"),
    ("Show version information.", "显示版本信息。"),
    ("show version information", "显示版本信息"),
    ("Show this help message", "显示此帮助消息"),
    ("Show help", "显示帮助"),
    ("show help", "显示帮助"),
    ("Display brief usage message", "显示简要用法消息"),
    ("display brief usage message", "显示简要用法消息"),
    ("Show program version", "显示程序版本"),
    ("Show program version.", "显示程序版本。"),
    ("Print information on", "打印相关信息"),
    ("print information on", "打印相关信息"),
    ("Show extra output", "显示额外输出"),
    ("Show extra output.", "显示额外输出。"),
    ("Enable verbose mode", "启用详细模式"),
    ("Enable verbose mode.", "启用详细模式。"),
    ("enable verbose mode", "启用详细模式"),
    ("More verbose output", "更详细的输出"),
    ("More verbose output.", "更详细的输出。"),
    ("do not", "不"),
    ("Do not", "不"),
    ("Don't show any output", "不显示任何输出"),
    ("Don't produce warning output", "不产生警告输出"),
    ("Don't produce warning output.", "不产生警告输出。"),
    ("This manual page documents briefly the", "本手册页简要记录了"),
    ("This manual page documents", "本手册页记录了"),
    ("This manual page was written by", "本手册页由"),
    ("This man page was written by", "本手册页由"),
    ("This man page was written using", "本手册页使用"),
    ("Written by", "由"),
    ("written by", "由"),
    ("checks the syntax only", "仅检查语法"),
    ("checks the syntax only.", "仅检查语法。"),
    ("output file", "输出文件"),
    ("Output file", "输出文件"),
    ("Output file.", "输出文件。"),
    ("input file", "输入文件"),
    ("Input file", "输入文件"),
    ("Input file.", "输入文件。"),
    ("Report bugs to", "报告错误至"),
    ("report bugs to", "报告错误至"),
    ("Please send bug reports to", "请将错误报告发送至"),
    ("please report these on", "请将其报告至"),
    ("If you find bugs", "如果您发现错误"),
    ("Report bugs", "报告错误"),
    ("report bugs", "报告错误"),
    ("No effect", "无效果"),
    ("No effect.", "无效果。"),
    ("none known", "目前没有已知错误"),
    ("None known", "目前没有已知错误"),
    ("None known.", "目前没有已知错误。"),
    ("not yet supported", "尚不支持"),
    ("NOT YET SUPPORTED", "尚不支持"),
    ("This is free software", "这是自由软件"),
    ("You are free to change and redistribute it", "您可以自由修改和重新分发它"),
    ("you are free to change and redistribute it", "您可以自由修改和重新分发它"),
    ("There is NO WARRANTY", "不提供任何担保"),
    ("There is NO WARRANTY, to the extent permitted by law", "在法律允许的范围内，不提供任何担保"),
    ("there is NO WARRANTY", "不提供任何担保"),
    ("to the extent permitted by law", "在法律允许的范围内"),
    ("License GPLv2+", "许可证 GPLv2+"),
    ("License GPLv3+", "许可证 GPLv3+"),
    ("GNU GPL version 2 or later", "GNU GPL 版本 2 或更高版本"),
    ("GNU GPL version 3 or later", "GNU GPL 版本 3 或更高版本"),
    ("GNU General Public License", "GNU 通用公共许可证"),
    ("GNU Lesser General Public License", "GNU 宽通用公共许可证"),
    ("All rights reserved", "保留所有权利"),
    ("all rights reserved", "保留所有权利"),
    ("Generates a", "生成"),
    ("generates a", "生成"),
    ("Generates", "生成"),
    ("generates", "生成"),
    ("Generate", "生成"),
    ("generate", "生成"),
    ("Decodes", "解码"),
    ("decodes", "解码"),
    ("Prints", "打印"),
    ("prints", "打印"),
    ("Print", "打印"),
    ("print", "打印"),
    ("Dumps", "转储"),
    ("dumps", "转储"),
    ("Loads", "加载"),
    ("loads", "加载"),
    ("Sets", "设置"),
    ("sets", "设置"),
    ("Set", "设置"),
    ("Specify", "指定"),
    ("specify", "指定"),
    ("Specifies", "指定"),
    ("specifies", "指定"),
    ("Displays", "显示"),
    ("displays", "显示"),
    ("Display", "显示"),
    ("display", "显示"),
    ("Reads", "读取"),
    ("reads", "读取"),
    ("Read", "读取"),
    ("read", "读取"),
    ("Write", "写入"),
    ("write", "写入"),
    ("Writes", "写入"),
    ("writes", "写入"),
    ("Returns", "返回"),
    ("returns", "返回"),
    ("Return", "返回"),
    ("return", "返回"),
    ("Sends", "发送"),
    ("sends", "发送"),
    ("Creates", "创建"),
    ("creates", "创建"),
    ("Create", "创建"),
    ("create", "创建"),
    ("Converts", "转换"),
    ("converts", "转换"),
    ("Convert", "转换"),
    ("convert", "转换"),
    ("Copies", "复制"),
    ("copies", "复制"),
    ("Copy", "复制"),
    ("copy", "复制"),
    ("Removes", "移除"),
    ("removes", "移除"),
    ("Remove", "移除"),
    ("remove", "移除"),
    ("Deletes", "删除"),
    ("deletes", "删除"),
    ("Delete", "删除"),
    ("delete", "删除"),
    ("Checks", "检查"),
    ("checks", "检查"),
    ("Check", "检查"),
    ("check", "检查"),
    ("Add", "添加"),
    ("add", "添加"),
    ("Adds", "添加"),
    ("adds", "添加"),
    ("Lists", "列出"),
    ("lists", "列出"),
    ("List", "列出"),
    ("list", "列出"),
    ("Updates", "更新"),
    ("updates", "更新"),
    ("Update", "更新"),
    ("update", "更新"),
    ("Verifies", "验证"),
    ("verifies", "验证"),
    ("Verify", "验证"),
    ("verify", "验证"),
    ("Resolves", "解析"),
    ("resolves", "解析"),
    ("Resolve", "解析"),
    ("resolve", "解析"),
    ("Enable", "启用"),
    ("enable", "启用"),
    ("Disable", "禁用"),
    ("disable", "禁用"),
    ("Force", "强制"),
    ("force", "强制"),
    ("Pause", "暂停"),
    ("pause", "暂停"),
    ("Resume", "恢复"),
    ("resume", "恢复"),
    ("Exit", "退出"),
    ("exit", "退出"),
    ("Start", "启动"),
    ("start", "启动"),
    ("Stop", "停止"),
    ("stop", "停止"),
    ("Browse", "浏览"),
    ("browse", "浏览"),
    ("Browse for", "浏览"),
    ("browse for", "浏览"),
    ("Show a", "显示"),
    ("show a", "显示"),
    ("Modify", "修改"),
    ("modify", "修改"),
    ("Handle", "处理"),
    ("handle", "处理"),
    ("Force overwriting", "强制覆盖"),
    ("force overwriting of files that already exist", "强制覆盖已存在的文件"),
    ("print modifications but don't perform them", "打印修改但不执行"),
    ("Copyright", "版权"),
    ("copyright", "版权"),
    ("No CD-ROM device found", "未找到 CD-ROM 设备"),
    ("No CD\-ROM device found.", "未找到 CD\-ROM 设备。"),
    ("See", "参见"),
    ("For further information visit", "有关更多信息，请访问"),
    ("for more information about the big picture", "了解更多关于全局架构的信息"),
    ("If given no arguments", "如果未提供参数"),
    ("if given no arguments", "如果未提供参数"),
    ("Optionally", "可选地"),
    ("optionally", "可选地"),
    ("Defaults to", "默认为"),
    ("defaults to", "默认为"),
    ("Default", "默认"),
    ("default", "默认"),
    ("Not specified", "未指定"),
    ("not specified", "未指定"),
    ("If omitted", "如果省略"),
    ("if omitted", "如果省略"),
    ("If not given", "如果未指定"),
    ("if not given", "如果未指定"),
    ("Must be run as root", "必须以 root 身份运行"),
    ("must be run as root", "必须以 root 身份运行"),
    ("Will fail otherwise", "否则将失败"),
    ("will fail otherwise", "否则将失败"),
    ("will fail otherwise.", "否则将失败。"),
    ("Successful program execution", "程序执行成功"),
    ("Successful program execution.", "程序执行成功。"),
    ("The operation failed or the command syntax was not valid", "操作失败或命令语法无效"),
    ("The operation failed or the command syntax was not valid.", "操作失败或命令语法无效。"),
    ("returns 0 on success", "成功时返回 0"),
    ("returns 0 on success,", "成功时返回 0，"),
    ("returns 1 if a file could not be read", "文件无法读取时返回 1"),
    ("if a file could not be read", "如果文件无法读取"),
    ("could not be read", "无法读取"),
    ("if the arguments are invalid", "如果参数无效"),
    ("arguments are invalid", "参数无效"),
    ("arguments is invalid", "参数无效"),
    ("arguments is invalid.", "参数无效。"),
    ("on success", "成功时"),
    ("Beware of special chars", "请注意特殊字符"),
    ("The same warning applies to", "同样的警告也适用于"),
    ("please read your shell manual", "请阅读您的 shell 手册"),
    ("Please read your shell manual", "请阅读您的 shell 手册"),
    ("should be protected by", "应该通过"),
    ("surrounding arguments by quotes", "在参数周围加上引号"),
    ("using single backslashes", "使用反斜杠"),
    ("is a utility for", "是一个用于"),
    ("is a tool for", "是一个用于"),
    ("is a program for", "是一个用于"),
    ("is a command line tool", "是一个命令行工具"),
    ("command-line tool", "命令行工具"),
    ("command line tool", "命令行工具"),
    ("is a tool", "是一个工具"),
    ("tool to manipulate", "用于操作"),
    ("tool to", "用于"),
    ("program to", "用于"),
    ("program can be used to", "程序可用于"),
    ("The program then prints", "程序随后打印"),
    ("the program prints", "程序打印"),
    ("You simply pass as the first command line argument", "您只需将第一个命令行参数传入"),
    ("It is crucial", "这是至关重要的"),
    ("in order to avoid shell substitutions", "为了避免 shell 替换"),
    ("to enclose both the expression and the strings in single quotes", "将表达式和字符串都用单引号括起来"),
    ("the what[0] part represents the whole match", "what[0] 部分表示整个匹配"),
    ("the what[i] part represents the i-th marked subexpression that matched", "what[i] 部分表示匹配的第 i 个标记子表达式"),
    ("The program also prints possible prefix and suffix", "程序还会打印可能的前缀和后缀"),
    ("The program also prints possible prefix and suffix.", "程序还会打印可能的前缀和后缀。"),
    ("A summary of options is included below", "以下是选项摘要"),
    ("A summary of options is included below.", "以下是选项摘要。"),
    ("This program follows the usual GNU command line syntax", "本程序遵循通常的 GNU 命令行语法"),
    ("with long options starting with two dashes", "长选项以两个破折号开头"),
    ("a text mode image viewer", "一个文本模式图像查看器"),
    ("a lightweight text mode image viewer", "一个轻量级文本模式图像查看器"),
    ("It renders images using colour", "它使用彩色"),
    ("ASCII characters", "ASCII 字符"),
    ("switches to the next file", "切换到下一个文件"),
    ("switches to previous file", "切换到上一个文件"),
    ("exit the program", "退出程序"),
    ("exits the program", "退出程序"),
    ("pauses and resumes the program", "暂停和恢复程序"),
    ("forces an effect transition to happen", "强制进行效果过渡"),
    ("fullscreen mode", "全屏模式"),
    ("toggle the dithering mode", "切换抖动模式"),
    ("no dithering", "无抖动"),
    ("4x4 ordered dithering", "4x4 有序抖动"),
    ("8x8 ordered dithering", "8x8 有序抖动"),
    ("random dithering", "随机抖动"),
    ("zoom in and out", "放大和缩小"),
    ("reset the zoom level to normal", "将缩放级别重置为正常"),
    ("reset the zoom level", "重置缩放级别"),
    ("switch to next image", "切换到下一张图像"),
    ("switch to previous image", "切换到上一张图像"),
    ("scroll the image around", "滚动图像"),
    ("show the help screen", "显示帮助屏幕"),
    ("hide/show menu and status bars", "隐藏/显示菜单和状态栏"),
    ("menu and status bars", "菜单和状态栏"),
    ("There is no support for aspect ratio yet", "目前尚不支持宽高比"),
    ("is completely useless when run without an argument", "当不带参数运行时完全无用"),
    ("loads a", "加载"),
    ("load", "加载"),
    ("requires", "需要"),
    ("Requires", "需要"),
    ("from the command line", "从命令行"),
    ("at the command line", "在命令行"),
    ("on the command line", "在命令行"),
    ("on the command line.", "在命令行。"),
    ("on the given certificate", "给定证书"),
    ("interactively or non interactively", "交互式或非交互式"),
    ("by specifying the template command line option", "通过指定模板命令行选项"),
    ("The tool accepts files or supported URIs via the --infile option", "该工具通过 --infile 选项接受文件或支持的 URI"),
    ("the --infile option", "--infile 选项"),
    ("you can provide it using the environment variables", "您可以使用环境变量提供它"),
    ("This option takes an integer number", "此选项接受一个整数"),
    ("This option takes an integer number as its argument", "此选项接受一个整数作为其参数"),
    ("This option takes an integer number as its argument.", "此选项接受一个整数作为其参数。"),
    ("as its argument", "作为其参数"),
    ("The value is constrained to being", "该值被限制为"),
    ("in the range", "在范围"),
    ("network services running on the local LAN", "本地局域网上运行的网络服务"),
    ("local network", "本地网络"),
    ("local network.", "本地网络。"),
    ("shows them in a GUI for the user to select one", "在 GUI 中显示供用户选择"),
    ("calls ssh/vncviewer after a selection was made", "在选择完成后调用 ssh/vncviewer"),
    ("if the binary is called as", "如果以以下名称调用二进制文件"),
    ("only ssh servers will be shown", "仅显示 SSH 服务器"),
    ("only VNC servers will be shown", "仅显示 VNC 服务器"),
    ("both VNC and SSH servers are shown", "同时显示 VNC 和 SSH 服务器"),
    ("the default browsing domain", "默认浏览域"),
    ("will browse in the default browsing domain", "将在默认浏览域中浏览"),
    ("Browse in the specified domain", "在指定的域中浏览"),
    ("browse in the specified domain", "在指定的域中浏览"),
    ("Enable debugging", "启用调试"),
    ("Set debugging to LEVEL", "将调试级别设置为 LEVEL"),
    ("show only info about", "仅显示相关信息"),
    ("only info about", "仅关于"),
    ("Display version and copyright information", "显示版本和版权信息"),
    ("Display version", "显示版本"),
    ("was written by", "由"),
    ("is maintained as a Texinfo manual", "以 Texinfo 手册形式维护"),
    ("is maintained as a Texinfo manual.", "以 Texinfo 手册形式维护。"),
    ("should give you access to the complete manual", "应该能让您访问完整的手册"),
    ("should give you access to the complete manual.", "应该能让您访问完整的手册。"),
    ("If the info and", "如果 info 和"),
    ("programs are properly installed at your site", "程序在您的系统上正确安装"),
    ("the command", "以下命令"),
    ("Report bugs in the bug tracker at", "通过以下地址的错误跟踪器报告错误："),
    ("or by email to", "或发送电子邮件至"),
    ("GNU home page", "GNU 主页"),
    ("General help using GNU software", "使用 GNU 软件的一般帮助"),
    ("General help using GNU software:", "使用 GNU 软件的一般帮助："),
    ("Please report any bugs you find to", "请将发现的任何错误报告至"),
    ("is covered by the", "采用"),
    ("is a port of", "是以下项目的移植版本："),
    ("written and put in the public domain by", "编写并发布到公共领域"),
    ("was made by", "由"),
    ("with a lot of help from others", "并获得了很多其他人的帮助"),
    ("See the Help/Credits menu", "请参见帮助/鸣谢菜单"),
    ("Also Known As", "也被称为"),
    ("Also known as", "也被称为"),
    ("When using evim you are expected to take a handkerchief", "使用 evim 时，您应该拿一条手帕"),
    ("make a knot in each corner and wear it on your head", "在每个角打结并戴在头上"),
    ("a graphical disk usage analyzer", "一个图形磁盘使用分析器"),
    ("a.k.a.", "又名"),
    ("is able to scan either specific folders", "能够扫描特定文件夹"),
    ("in order to give the user a tree representation", "以便向用户提供树形表示"),
    ("A graphical representation is also provided", "还会提供图形化表示"),
    ("for any selected folder", "对于任何选定的文件夹"),
    ("auto-detects any mounted/unmounted device", "自动检测任何已挂载/未挂载的设备"),
    ("Do not skip directories on different file systems", "不跳过不同文件系统上的目录"),
    ("Ignored if DIRECTORY is not specified", "如果未指定 DIRECTORY 则忽略"),
    ("Show command line options", "显示命令行选项"),
    ("Bugs should be reported to", "错误应报告至"),
    ("the GNOME issue tracker at", "GNOME 问题跟踪器："),
    ("mandatory arguments to long options are mandatory for short options too", "长选项的必选参数对于短选项也是必选的"),
    ("mandatory arguments", "必选参数"),
    ("long options", "长选项"),
    ("short options", "短选项"),
    ("Mandatory arguments to long options are mandatory for short options too", "长选项的必选参数对于短选项也是必选的"),
    ("a graphical disk usage analyzer for the GNOME desktop", "用于 GNOME 桌面的图形磁盘使用分析器"),
    ("Substitutes the values of environment variables", "替换环境变量的值"),
    ("Substitutes the values of environment variables.", "替换环境变量的值。"),
    ("substitutes environment variables in shell format strings", "替换 shell 格式字符串中的环境变量"),
    ("In normal operation mode", "在正常操作模式下"),
    ("standard input is copied to standard output", "标准输入被复制到标准输出"),
    ("with references to environment variables of the form", "其中形式为以下的环境变量引用"),
    ("being replaced with the corresponding values", "被替换为相应的值"),
    ("only those environment variables that are referenced", "仅替换那些被引用的环境变量"),
    ("are substituted", "被替换"),
    ("otherwise all environment variables references occurring in standard input are substituted", "否则，标准输入中出现的所有环境变量引用都将被替换"),
    ("standard input is ignored", "标准输入被忽略"),
    ("the output consists of the environment variables that are referenced", "输出由引用的环境变量组成"),
    ("one per line", "每行一个"),
    ("one per line.", "每行一个。"),
    ("will read its data from the standard input", "将从标准输入读取数据"),
    ("If no file argument is provided", "如果没有提供文件参数"),
    ("is used", "被使用"),
    ("If no file argument is provided or", "如果没有提供文件参数或使用"),
    ("will read its data from", "将从"),
    ("Pause and resume the program", "暂停和恢复程序"),
    ("pause and resume the program", "暂停和恢复程序"),
    ("Force an effect transition to happen", "强制进行效果过渡"),
    ("force an effect transition to happen", "强制进行效果过渡"),
    ("Exit the program", "退出程序"),
    ("exit the program", "退出程序"),
    ("Pauses and resumes the program", "暂停和恢复程序"),
    ("Forces an effect transition to happen", "强制进行效果过渡"),
    ("Exits the program", "退出程序"),
    ("can load the most widespread image formats", "可以加载最常见的图像格式"),
    ("You can zoom and scroll the image", "您可以缩放和滚动图像"),
    ("You can zoom and scroll the image around for more details", "您可以缩放和滚动图像以查看更多细节"),
    ("choose four different dithering modes", "选择四种不同的抖动模式"),
    ("All commands are accessible through a single key press", "所有命令都通过单键按下即可访问"),
    ("It is a powerful add-on to famous console programs", "它是著名控制台程序的强大附加组件"),
    ("such as the mutt email client", "如 mutt 电子邮件客户端"),
    ("the slrn newsreader", "slrn 新闻阅读器"),
    ("the links or w3m web browsers", "links 或 w3m Web 浏览器"),
    ("still no way to load an image from", "目前还没有办法从"),
    ("it is completely useless when run without an argument", "当不带参数运行时它完全无用"),
    ("There is no support for aspect ratio yet.", "目前尚不支持宽高比。"),
    ("Also, since there is no way yet to load an image from", "另外，由于目前还没有办法从"),
    ("it is completely useless", "它完全无用"),
    ("when run without an argument", "当不带参数运行时"),
    ("Cleans up unused", "清理未使用的"),
    ("cleans up unused", "清理未使用的"),
    ("connection sockets", "连接套接字"),
    ("cleans up sockets in the standard default socket directory", "清理标准默认套接字目录中的套接字"),
    ("for the per-user-login-session message bus", "每个用户登录会话消息总线"),
    ("you can pass a different directory on the command line", "您可以在命令行上传递不同的目录"),
    ("On Linux, this program is essentially useless", "在 Linux 上，该程序基本上无用"),
    ("because D-Bus defaults to using", "因为 D-Bus 默认使用"),
    ("abstract sockets", "抽象套接字"),
    ("that exist only in memory", "它们仅存在于内存中"),
    ("don't have a corresponding file in", "在"),

    ("On most other flavors of UNIX", "在大多数其他 UNIX 变体上"),
    ("it's possible for the socket files to leak", "套接字文件可能会泄漏"),
    ("when programs using D-Bus exit abnormally", "当使用 D-Bus 的程序异常退出时"),
    ("or without closing their D-Bus connections", "或在未关闭其 D-Bus 连接的情况下"),
    ("Thus, it might be interesting to run", "因此，运行"),
    ("in a cron job to mop up any leaked sockets", "在 cron 作业中清理任何泄漏的套接字"),
    ("mop up any leaked sockets", "清理任何泄漏的套接字"),
    ("Or you can just ignore the leaked sockets", "或者您可以忽略泄漏的套接字"),
    ("they aren't really hurting anything", "它们并不会真正造成任何损害"),
    ("other than cluttering the output of", "只是会让"),
    ("was adapted by", "由"),
    ("from", "从"),
    ("D-Bus mailing list or bug tracker", "D-Bus 邮件列表或错误跟踪器"),
    ("Provides enumeration and provisioning commands", "提供枚举和配置命令"),
    ("for CXL platforms", "为 CXL 平台"),
    ("for the CXL devices managed by the Linux kernel", "为 Linux 内核管理的 CXL 设备"),
    ("Display the version of the", "显示"),
    ("utility", "工具"),
    ("Run the", "运行"),
    ("command", "命令"),
    ("Provides enumeration", "提供枚举"),
    ("and provisioning commands", "和配置命令"),
    ("is set to be able to type text directly", "被设置以能够直接键入文本"),
    ("Mappings are setup to make Copy and Paste work with the MS-Windows keys", "设置映射以使复制和粘贴与 MS-Windows 按键配合使用"),
    ("CTRL-X cuts text", "CTRL-X 剪切文本"),
    ("CTRL-C copies text", "CTRL-C 复制文本"),
    ("CTRL-V pastes text", "CTRL-V 粘贴文本"),
    ("Use CTRL-Q to obtain the original meaning of CTRL-V", "使用 CTRL-Q 获取 CTRL-V 的原始含义"),
    ("starts Vim and sets options to make it behave like a modeless editor", "启动 Vim 并设置选项使其行为类似于无模式编辑器"),
    ("This is still Vim but used as a point-and-click editor", "这仍然是 Vim，但用作点击式编辑器"),
    ("This feels a lot like using Notepad on MS-Windows", "感觉很像在 MS-Windows 上使用记事本"),
    ("will always run in the GUI, to enable the use of menus and toolbar", "始终在 GUI 中运行，以启用菜单和工具栏的使用"),
    ("Only to be used for people who really can't work with Vim in the normal way", "仅适用于那些确实无法以正常方式使用 Vim 的人"),
    ("Editing will be much less efficient", "编辑效率会大大降低"),
    ("is the same, but starts in read-only mode", "相同，但以只读模式启动"),
    ("It works just like", "它的工作方式与"),
    ("See vim(1) for details about Vim, options, etc", "有关 Vim、选项等的详细信息，请参见 vim(1)"),
    ("The script loaded to initialize eVim", "加载以初始化 eVim 的脚本"),
    ("is short version number", "是短版本号"),
    ("for Vim", "对于 Vim"),
]

def find_source(name):
    """Find source man page file"""
    src = os.path.join(SRC, name + ".gz")
    if os.path.exists(src):
        return src
    for ext in ['.1.gz', '.1m.gz', '.1ssl.gz']:
        src = os.path.join(SRC, name + ext)
        if os.path.exists(src):
            return src
    for g in glob.glob(os.path.join(SRC, name + '*')):
        return g
    return None

def translate_text(text):
    """Apply known phrase translations"""
    if not text or len(text) < 3:
        return text
    result = text
    for en, zh in PHRASES:
        # Only replace at word boundaries or standalone
        if en in result:
            result = result.replace(en, zh)
    return result

def process(lines):
    out = []
    
    for line in lines:
        line = line.rstrip('\n\r')
        
        if not line.strip():
            out.append(line)
            continue
        
        # Comments - preserve
        if line.lstrip().startswith('.\\"'):
            out.append(line)
            continue
        
        # .TH header
        m = re.match(r'^(\.TH\s+)(.*)', line)
        if m:
            rest = m.group(2)
            rest = rest.replace("User Commands", "用户命令")
            rest = rest.replace("User commands", "用户命令")
            rest = rest.replace("Linux User's Manual", "Linux 用户手册")
            rest = rest.replace("Linux Programmer's Manual", "Linux 程序员手册")
            out.append(".TH " + rest)
            continue
        
        # .SH section headers
        m = re.match(r'^\.SH\s+"?([^"]+)"?', line)
        if m:
            h = m.group(1).strip()
            if h.upper() in SH_MAP:
                out.append(f'.SH "{SH_MAP[h.upper()]}"')
            else:
                t = translate_text(h)
                out.append(f'.SH "{t}"')
            continue
        
        # .SS subsection headers
        m = re.match(r'^\.SS\s+"?([^"]+)"?', line)
        if m:
            h = m.group(1).strip()
            t = translate_text(h)
            out.append(f'.SS "{t}"')
            continue
        
        # DocBook .Sh style
        m = re.match(r'^\.Sh\s+"?([^"]+)"?', line)
        if m:
            h = m.group(1).strip()
            if h.upper() in SH_MAP:
                out.append(f'.Sh "{SH_MAP[h.upper()]}"')
            else:
                out.append(f'.Sh "{translate_text(h)}"')
            continue
        
        # Pure roff formatting lines - pass through
        if line.startswith('.') and len(line.split()) >= 1:
            cmd = line.split()[0]
            pure = {'.ad','.nh','.hy','.TP','.PP','.IP','.LP','.HP','.RS','.RE',
                    '.PD','.sp','.br','.fi','.nf','.na','.bp','.pm','.lf',
                    '.in','.ti','.ps','.vs','.ft','.cs','.po','.ll','.lt',
                    '.ne','.ie','.el','.if','.de','.ds','.nr','.rm','.rn',
                    '.so','.mso','.tr','.hc','.hw','.ID','.ce','.rj','.ul',
                    '.cu','.mc','.ns','.rs','.rt','.pc','.pn','.pl','.wh',
                    '.ch','.dt','.it','.em','.am','.as','.ee','.ec','.eo',
                    '.cc','.c2','.do','.nx','.ex','.sy','.ab','.os','.sv',
                    '.tm','.ig','.pi','.cf','.fc','.ds1','.NOP','.HP',
                    '.Dd','.Dt','.Os','.Sh','.Nm','.Nd','.Op','.Dl','.Pp',
                    '.Xr','.Ed','.Bd','.Lb','.In','.Fn','.Fo','.Fc','.Ft',
                    '.Fa','.Vt','.Bl','.El','.It','.Cd','.Fd','.Ss',
                    '.TS','.TE','.T{','.T}',
                    '.URL','.als','.MTO','.mso','.LINKSTYLE',
                    '.B','.BI','.BR','.I','.IB','.IR','.RB','.RI',
                    '.SB','.SM','.XR','.MT','.UR','.UE',
                    }
            if cmd in pure:
                out.append(line)
                continue
            # Other roff commands - pass through
            if line.startswith('.') and (cmd.startswith('.f') or cmd.startswith('.F') or
                                          cmd.startswith('.B') or cmd.startswith('.I') or
                                          cmd.startswith('.R') or cmd.startswith('.S') or
                                          cmd.startswith('.N') or cmd.startswith('.U') or
                                          cmd.startswith('.M') or cmd.startswith('.X') or
                                          cmd.startswith('.D') or cmd.startswith('.O') or
                                          cmd.startswith('.P') or cmd.startswith('.L') or
                                          cmd.startswith('.A') or cmd.startswith('.E') or
                                          cmd.startswith('.T') or cmd.startswith('.C') or
                                          cmd.startswith('.W') or cmd.startswith('.\\')):
                out.append(line)
                continue
        
        # Text line - translate
        translated = translate_text(line)
        out.append(translated)
    
    return out

def install_page(name):
    src_file = os.path.join(DEST, name)
    tmp_gz = os.path.join(DEST, name + ".gz")
    dst_gz = os.path.join(INST, name + ".gz")
    
    try:
        with open(src_file, 'rb') as f:
            with gzip.open(tmp_gz, 'wb') as g:
                g.write(f.read())
        subprocess.run(['sudo', 'cp', tmp_gz, dst_gz], check=True, capture_output=True)
        os.remove(tmp_gz)
        return True
    except:
        return False

def main():
    os.makedirs(DEST, exist_ok=True)
    
    # Get remaining pages
    batch = "/tmp/batch_a_e.txt"
    with open(batch, 'r') as f:
        all_pages = [l.strip() for l in f if l.strip()]
    
    remaining = [p for p in all_pages if not os.path.exists(os.path.join(INST, p + ".gz"))]
    
    ok = 0
    bad = []
    
    sys.stdout.reconfigure(line_buffering=True)
    
    for i, page in enumerate(remaining):
        name = page
        src = find_source(name)
        
        if not src:
            print(f"[{i+1}/{len(remaining)}] {name} NOT FOUND", flush=True)
            bad.append(name)
            continue
        
        try:
            with gzip.open(src, 'rt', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"[{i+1}/{len(remaining)}] {name} READ ERR: {e}", flush=True)
            bad.append(name)
            continue
        
        try:
            result = process(lines)
            dest_file = os.path.join(DEST, name)
            with open(dest_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(result) + '\n')
        except Exception as e:
            print(f"[{i+1}/{len(remaining)}] {name} WRITE ERR: {e}", flush=True)
            bad.append(name)
            continue
        
        if install_page(name):
            ok += 1
            if (i+1) % 10 == 0:
                print(f"[{i+1}/{len(remaining)}] ... {ok} ok", flush=True)
        else:
            print(f"[{i+1}/{len(remaining)}] {name} INSTALL FAILED", flush=True)
            bad.append(name)
    
    print(f"\nbatch a-e done: {ok} translations", flush=True)
    if bad:
        print(f"Failed ({len(bad)}): {', '.join(bad[:10])}")

if __name__ == "__main__":
    main()
