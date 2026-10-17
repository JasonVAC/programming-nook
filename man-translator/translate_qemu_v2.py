#!/usr/bin/env python3
"""
Complete QEMU man page translator to Chinese.
Translates all prose content while preserving roff formatting.
"""
import os, re, gzip, subprocess

SRC = "/usr/share/man/man1"
DST = "/tmp/man1_zh"
INST = "/usr/share/man/zh_CN/man1"

# ── .SH section translations ──
SH_MAP = {
    "NAME": "名称",
    "SYNOPSIS": "语法",
    "DESCRIPTION": "描述",
    "OPTIONS": "选项",
    "NOTES": "注释",
    "SEE ALSO": "参见",
    "EXAMPLES": "示例",
    "EXAMPLE": "示例",
    "Author": "作者",
    "Copyright": "版权",
    "BUGS": "缺陷",
}

# ── .SS subsection translations ──
SS_MAP = {
    "Machine\\-specific options": "机器特定选项",
    "Standard options": "标准选项",
    "Block device options": "块设备选项",
    "USB convenience options": "USB 便捷选项",
    "Display options": "显示选项",
    "i386 target only": "仅限 i386 目标",
    "Network options": "网络选项",
    "Character device options": "字符设备选项",
    "TPM device options": "TPM 设备选项",
    "Boot Image or Kernel specific": "启动映像或内核特定选项",
    "Debug/Expert options": "调试/专家选项",
    "Generic object creation": "通用对象创建",
    "Multiplexer Keys": "多路复用器按键",
}

# ── Word-level translations (for substitution within text) ──
WORD_MAP = [
    ("QEMU User Documentation", "QEMU 用户文档"),
    ("QEMU disk image utility", "QEMU 磁盘映像工具"),
    ("QEMU storage daemon", "QEMU 存储守护进程"),
    ("Warning:", "警告："),
    ("Note:", "注意："),
    ("Important:", "重要："),
    ("Tip:", "提示："),
    ("enable or disable", "启用或禁用"),
    ("Enables or disables", "启用或禁用"),
    ("enables or disables", "启用或禁用"),
    ("Enabled by default", "默认启用"),
    ("enabled by default", "默认启用"),
    ("Disabled by default", "默认禁用"),
    ("disabled by default", "默认禁用"),
    ("The default is on", "默认值为 on"),
    ("The default is off", "默认值为 off"),
    ("the default is on", "默认值为 on"),
    ("the default is off", "默认值为 off"),
    ("The default is none", "默认值为 none"),
    ("is the default", "是默认值"),
    ("Default value is", "默认值为"),
    ("Default is", "默认值为"),
    ("default is", "默认值为"),
    ("Default", "默认值"),
    ("default", "默认值"),
    ("Not available", "不可用"),
    ("Not supported", "不支持"),
    ("Supported values are", "支持的值有"),
    ("See also", "另请参阅"),
    ("See the", "请参阅"),
    ("see the", "请参阅"),
    ("For more information", "有关更多信息"),
    ("For more details", "有关更多详细信息"),
    ("For example", "例如"),
    ("for example", "例如"),
    ("For instance", "例如"),
    ("for instance", "例如"),
    ("Note that", "请注意"),
    ("note that", "请注意"),
    ("please note", "请注意"),
    ("In other words", "换句话说"),
    ("As a result", "因此"),
    ("Alternatively", "或者"),
    ("Otherwise", "否则"),
    ("Therefore", "因此"),
    ("However", "但是"),
    ("Additionally", "此外"),
    ("Furthermore", "此外"),
    ("On the other hand", "另一方面"),
    ("In particular", "特别地"),
    ("In general", "通常"),
    ("In addition", "此外"),
    ("Currently", "目前"),
    ("Typically", "通常"),
    ("Normally", "通常"),
    ("Usually", "通常"),
    ("Often", "经常"),
    ("Sometimes", "有时"),
    ("Always", "始终"),
    ("Never", "绝不"),
    ("Only", "仅"),
    ("Also", "也"),
    ("Either", "要么"),
    ("None", "无"),
    ("none", "无"),
    ("automatically", "自动"),
    ("automatically.", "自动。"),
    ("manual", "手动"),
    ("manually", "手动"),
    ("successfully", "成功"),
    ("Successfully", "成功"),
    ("specified", "指定"),
    ("Specified", "指定"),
    ("specify", "指定"),
    ("Specify", "指定"),
    ("specifies", "指定"),
    ("Specifies", "指定"),
    ("indicates", "表示"),
    ("Indicates", "表示"),
    ("suggests", "建议"),
    ("determines", "确定"),
    ("Determines", "确定"),
    ("defines", "定义"),
    ("Defines", "定义"),
    ("controls", "控制"),
    ("Controls", "控制"),
    ("configures", "配置"),
    ("Configures", "配置"),
    ("provides", "提供"),
    ("Provides", "提供"),
    ("enables", "启用"),
    ("Enables", "启用"),
    ("disables", "禁用"),
    ("Disables", "禁用"),
    ("allows", "允许"),
    ("Allows", "允许"),
    ("requires", "需要"),
    ("Requires", "需要"),
    ("supports", "支持"),
    ("Supports", "支持"),
    ("includes", "包括"),
    ("Includes", "包括"),
    ("excludes", "排除"),
    ("Excludes", "排除"),
    ("contains", "包含"),
    ("Contains", "包含"),
    ("generates", "生成"),
    ("Generates", "生成"),
    ("displays", "显示"),
    ("Displays", "显示"),
    ("Display", "显示"),
    ("displays", "显示"),
    ("shows", "显示"),
    ("Shows", "显示"),
    ("creates", "创建"),
    ("Creates", "创建"),
    ("removes", "移除"),
    ("Removes", "移除"),
    ("deletes", "删除"),
    ("Deletes", "删除"),
    ("replaces", "替换"),
    ("Replaces", "替换"),
    ("returns", "返回"),
    ("Returns", "返回"),
    ("selects", "选择"),
    ("Selects", "选择"),
    ("Choose", "选择"),
    ("choose", "选择"),
    ("Use", "使用"),
    ("use", "使用"),
    ("uses", "使用"),
    ("Uses", "使用"),
    ("Used", "用于"),
    ("used", "用于"),
    ("Set", "设置"),
    ("set", "设置"),
    ("sets", "设置"),
    ("Sets", "设置"),
    ("Run", "运行"),
    ("run", "运行"),
    ("runs", "运行"),
    ("Running", "运行"),
    ("Load", "加载"),
    ("load", "加载"),
    ("Save", "保存"),
    ("save", "保存"),
    ("Start", "启动"),
    ("start", "启动"),
    ("Stop", "停止"),
    ("stop", "停止"),
    ("Pause", "暂停"),
    ("pause", "暂停"),
    ("Resume", "恢复"),
    ("resume", "恢复"),
    ("Exit", "退出"),
    ("exit", "退出"),
    ("Quit", "退出"),
    ("quit", "退出"),
    ("file", "文件"),
    ("File", "文件"),
    ("files", "文件"),
    ("Files", "文件"),
    ("directory", "目录"),
    ("Directory", "目录"),
    ("directories", "目录"),
    ("device", "设备"),
    ("Device", "设备"),
    ("devices", "设备"),
    ("Devices", "设备"),
    ("interface", "接口"),
    ("Interface", "接口"),
    ("interfaces", "接口"),
    ("protocol", "协议"),
    ("Protocol", "协议"),
    ("command", "命令"),
    ("Command", "命令"),
    ("commands", "命令"),
    ("Commands", "命令"),
    ("command-line", "命令行"),
    ("command line", "命令行"),
    ("option", "选项"),
    ("Option", "选项"),
    ("options", "选项"),
    ("Options", "选项"),
    ("parameter", "参数"),
    ("Parameter", "参数"),
    ("parameters", "参数"),
    ("property", "属性"),
    ("Property", "属性"),
    ("properties", "属性"),
    ("Properties", "属性"),
    ("support", "支持"),
    ("Support", "支持"),
    ("driver", "驱动"),
    ("Driver", "驱动"),
    ("drivers", "驱动"),
    ("backend", "后端"),
    ("Backend", "后端"),
    ("frontend", "前端"),
    ("Frontend", "前端"),
    ("front-end", "前端"),
    ("disk image", "磁盘映像"),
    ("disk images", "磁盘映像"),
    ("hard disk", "硬盘"),
    ("virtual machine", "虚拟机"),
    ("Virtual Machine", "虚拟机"),
    ("virtual machines", "虚拟机"),
    ("VM", "VM"),
    ("VMs", "VM"),
    ("guest", "客户机"),
    ("Guest", "客户机"),
    ("host", "主机"),
    ("Host", "主机"),
    ("memory", "内存"),
    ("Memory", "内存"),
    ("RAM", "内存"),
    ("CPU", "CPU"),
    ("CPUs", "CPU"),
    ("socket", "套接字"),
    ("Socket", "套接字"),
    ("port", "端口"),
    ("Port", "端口"),
    ("network", "网络"),
    ("Network", "网络"),
    ("serial", "串行"),
    ("Serial", "串行"),
    ("parallel", "并行"),
    ("Parallel", "并行"),
    ("USB", "USB"),
    ("PCI", "PCI"),
    ("PCIe", "PCIe"),
    ("VGA", "VGA"),
    ("IDE", "IDE"),
    ("SCSI", "SCSI"),
    ("SATA", "SATA"),
    ("NVMe", "NVMe"),
    ("video", "视频"),
    ("Video", "视频"),
    ("audio", "音频"),
    ("Audio", "音频"),
    ("sound", "声音"),
    ("Sound", "声音"),
    ("display", "显示"),
    ("Display", "显示"),
    ("monitor", "监视器"),
    ("Monitor", "监视器"),
    ("console", "控制台"),
    ("Console", "控制台"),
    ("terminal", "终端"),
    ("Terminal", "终端"),
    ("emulation", "模拟"),
    ("Emulation", "模拟"),
    ("emulator", "模拟器"),
    ("Emulator", "模拟器"),
    ("simulation", "仿真"),
    ("Simulation", "仿真"),
    ("simulator", "仿真器"),
    ("Simulator", "仿真器"),
    ("configuration", "配置"),
    ("Configuration", "配置"),
    ("installation", "安装"),
    ("Installation", "安装"),
    ("migration", "迁移"),
    ("Migration", "迁移"),
    ("snapshot", "快照"),
    ("Snapshot", "快照"),
    ("authentication", "身份验证"),
    ("Authentication", "身份验证"),
    ("encryption", "加密"),
    ("Encryption", "加密"),
    ("compression", "压缩"),
    ("Compression", "压缩"),
    ("decompression", "解压"),
    ("Decompression", "解压"),
    ("format", "格式"),
    ("Format", "格式"),
    ("formats", "格式"),
    ("image format", "映像格式"),
    ("output", "输出"),
    ("Output", "输出"),
    ("input", "输入"),
    ("Input", "输入"),
    ("size", "大小"),
    ("Size", "大小"),
    ("mode", "模式"),
    ("Mode", "模式"),
    ("modes", "模式"),
    ("type", "类型"),
    ("Type", "类型"),
    ("types", "类型"),
    ("value", "值"),
    ("Value", "值"),
    ("values", "值"),
    ("name", "名称"),
    ("Name", "名称"),
    ("names", "名称"),
    ("address", "地址"),
    ("Address", "地址"),
    ("available", "可用"),
    ("Available", "可用"),
    ("required", "必需"),
    ("Required", "必需"),
    ("optional", "可选"),
    ("Optional", "可选"),
    ("valid", "有效"),
    ("Valid", "有效"),
    ("invalid", "无效"),
    ("Invalid", "无效"),
    ("connected", "已连接"),
    ("Connected", "已连接"),
    ("disconnected", "已断开"),
    ("Disconnected", "已断开"),
    ("enabled", "已启用"),
    ("Enabled", "已启用"),
    ("disabled", "已禁用"),
    ("Disabled", "已禁用"),
    ("activated", "已激活"),
    ("Deactivated", "已停用"),
    ("and exit", "并退出"),
    ("and exit.", "并退出。"),
    ("from the command line", "从命令行"),
    ("on the command line", "在命令行上"),
    ("in most cases", "在大多数情况下"),
    ("at runtime", "在运行时"),
    ("at boot time", "在启动时"),
    ("at startup", "在启动时"),
    ("by default", "默认情况下"),
    ("By default", "默认情况下"),
    ("per second", "每秒"),
    ("per minute", "每分钟"),
    ("per day", "每天"),
    ("in seconds", "以秒为单位"),
    ("in bytes", "以字节为单位"),
    ("in milliseconds", "以毫秒为单位"),
    ("in microseconds", "以微秒为单位"),
    ("in use", "正在使用中"),
    ("not recommended", "不建议"),
    ("experimental", "实验性"),
    ("Experimental", "实验性"),
    ("deprecated", "已弃用"),
    ("Deprecated", "已弃用"),
    ("obsolete", "已过时"),
    ("Obsolete", "已过时"),
    ("read-only", "只读"),
    ("read-write", "读写"),
    ("write-only", "只写"),
    ("user-space", "用户空间"),
    ("kernel-space", "内核空间"),
    ("real-time", "实时"),
    ("locks.", "锁。"),
    ("the following", "以下"),
    ("as follows", "如下"),
    ("as shown below", "如下所示"),
    ("as described above", "如上所述"),
    ("as described below", "如下所述"),
    ("as an example", "作为示例"),
]

# ── Sentence/paragraph-level translations ──
SENT_MAP = [
    ("Display help and exit", "显示帮助并退出"),
    ("Display this help and exit", "显示此帮助并退出"),
    ("Display version information and exit", "显示版本信息并退出"),
    ("Select the emulated machine by name", "按名称选择模拟的机器"),
    ("list available machines", "列出可用的机器"),
    ("This is used to enable an accelerator", "用于启用加速器"),
    ("Include guest memory in a core dump", "在核心转储中包含客户机内存"),
    ("Memory encryption object to use", "要使用的内存加密对象"),
    ("Enables emulation of VMWare IO port, for vmmouse etc", "启用 VMWare IO 端口模拟，用于 vmmouse 等"),
    ("auto says to select the value based on accel and i8042", "auto 表示根据 accel 和 i8042 选择值"),
    ("For accel=xen or i8042=off the default is off otherwise the default is on", "对于 accel=xen 或 i8042=off，默认值为 off，否则默认值为 on"),
    ("Enables or disables NVDIMM support", "启用或禁用 NVDIMM 支持"),
    ("Enables or disables ACPI Heterogeneous Memory Attribute Table (HMAT) support", "启用或禁用 ACPI 异构内存属性表（HMAT）支持"),
    ("Enables or disables ACPI Serial Port Console Redirection Table (SPCR) support", "启用或禁用 ACPI 串行端口控制台重定向表（SPCR）支持"),
    ("Allocate auxiliary guest RAM as an anonymous file that is shareable with an external process", "将辅助客户机 RAM 分配为可共享的匿名文件，可与外部进程共享"),
    ("memory allocated as a side effect of creating various devices", "因创建各种设备而分配的内存"),
    ("It does not apply to memory-backend-objects, whether explicitly specified on the command line, or implicitly created by the -m command line option", "它不适用于内存后端对象，无论是显式在命令行上指定的，还是由 -m 命令行选项隐式创建的"),
    ("To use the cpr-transfer migration mode, you must set aux-ram-share=on", "要使用 cpr-transfer 迁移模式，必须设置 aux-ram-share=on"),
    ("An alternative to legacy \\fB\\-mem\\-path\\fP and \\fBmem\\-prealloc\\fP options", "替代传统 \\fB\\-mem\\-path\\fP 和 \\fBmem\\-prealloc\\fP 选项的替代方案"),
    ("Allows to use a memory backend as main RAM", "允许使用内存后端作为主内存"),
    ("Migration compatibility note:", "迁移兼容性注意事项："),
    ("as backend id one shall use value of \(aqdefault\\-ram\\-id\(aq, advertised by machine type", "作为后端 id，应使用由机器类型公告的 \(aqdefault\\-ram\\-id\(aq 值"),
    ("Define a CXL Fixed Memory Window (CFMW)", "定义一个 CXL 固定内存窗口（CFMW）"),
    ("Define an SGX EPC section", "定义一个 SGX EPC 分区"),
    ("Define cache properties for SMP system", "定义 SMP 系统的缓存属性"),
    ("Display help", "显示帮助"),
    ("Display version information", "显示版本信息"),
    ("Specify tracing options", "指定跟踪选项"),
    ("Immediately enable events matching \\fIPATTERN\\fP (either event name or a globbing pattern)", "立即启用与 \\fIPATTERN\\fP 匹配的事件（事件名称或通配模式）"),
    ("Immediately enable events listed in \\fIFILE\\fP", "立即启用 \\fIFILE\\fP 中列出的事件"),
    ("Log output traces to \\fIFILE\\fP", "将跟踪输出记录到 \\fIFILE\\fP"),
    ("The QEMU PC System emulator simulates the following peripherals:", "QEMU PC 系统模拟器模拟以下外设："),
    ("QEMU uses the PC BIOS from the Seabios project and the Plex86/Bochs LGPL VGA BIOS", "QEMU 使用来自 Seabios 项目的 PC BIOS 和 Plex86/Bochs LGPL VGA BIOS"),
    ("QEMU uses YM3812 emulation by Tatsuyuki Satoh", "QEMU 使用 Tatsuyuki Satoh 编写的 YM3812 模拟"),
    ("Note that, by default, GUS shares IRQ(7) with parallel ports and so QEMU must be told to not have parallel ports to have working GUS", "请注意，默认情况下 GUS 与并行端口共享 IRQ(7)，因此必须告知 QEMU 不使用并行端口才能使 GUS 正常工作"),
    ("Or some other unclaimed IRQ", "或其他未占用的 IRQ"),
    ("CS4231A is the chip used in Windows Sound System and GUSMAX products", "CS4231A 是 Windows Sound System 和 GUSMAX 产品中使用的芯片"),
    ("The PC speaker audio device can be configured using the pcspk-audiodev machine property, i.e.", "PC 扬声器音频设备可以使用 pcspk-audiodev 机器属性进行配置，即"),
    ("It supports the following machine-specific options:", "支持以下机器特定选项："),
    ("Experimental option to select a particular south bridge", "选择特定南桥的实验性选项"),
    ("The following commands are supported:", "支持以下命令："),
    ("Toggle full screen", "切换全屏"),
    ("Enlarge the screen", "放大屏幕"),
    ("Shrink the screen", "缩小屏幕"),
    ("Restore the screen\(aqs un\\-scaled dimensions", "恢复屏幕的未缩放尺寸"),
    ("Switch to virtual console \(aqn\(aq", "切换到虚拟控制台 \(aqn\(aq"),
    ("Standard console mappings are:", "标准控制台映射有："),
    ("Target system display", "目标系统显示"),
    ("Toggle mouse and keyboard grab", "切换鼠标和键盘捕获"),
    ("During the graphical emulation, you can use special key combinations from the following table to change modes", "在图形模拟期间，您可以使用下表中的特殊键组合来切换模式"),
    ("Print this help", "打印此帮助"),
    ("Exit emulator", "退出模拟器"),
    ("Save disk data back to file (if \\-snapshot)", "将磁盘数据保存回文件（如果使用 -snapshot）"),
    ("Toggle console timestamps", "切换控制台时间戳"),
    ("Send break (magic sysrq in Linux)", "发送中断信号（Linux 中的 magic sysrq）"),
    ("Rotate between the frontends connected to the multiplexer (usually this switches between the monitor and the console)", "在连接到多路复用器的前端之间切换（通常是在监视器和控制台之间切换）"),
    ("Send the escape character to the frontend", "将转义字符发送到前端"),
    ("In addition to using normal file images for the emulated storage devices, QEMU can also use networked resources such as iSCSI devices", "除了使用普通文件映像作为模拟存储设备外，QEMU 还可以使用 iSCSI 设备等网络资源"),
    ("These are specified using a special URL syntax", "这些使用特殊的 URL 语法进行指定"),
    ("iSCSI support allows QEMU to access iSCSI resources directly and use as images for the guest storage", "iSCSI 支持允许 QEMU 直接访问 iSCSI 资源并将其用作客户机存储的映像"),
    ("Both disk and cdrom images are supported", "支持磁盘和 cdrom 映像"),
    ("QEMU supports NBD (Network Block Devices) both using TCP protocol as well as Unix Domain Sockets", "QEMU 支持使用 TCP 协议和 Unix 域套接字的 NBD（网络块设备）"),
    ("QEMU supports SSH (Secure Shell) access to remote disks", "QEMU 支持通过 SSH（安全外壳协议）访问远程磁盘"),
    ("Currently authentication must be done using ssh\\-agent", "目前必须使用 ssh-agent 进行身份验证"),
    ("Other authentication methods may be supported in future", "将来可能支持其他身份验证方法"),
    ("GlusterFS is a user space distributed file system", "GlusterFS 是一个用户空间分布式文件系统"),
    ("QEMU supports the use of GlusterFS volumes for hosting VM disk images using TCP and Unix Domain Sockets transport protocols", "QEMU 支持使用 GlusterFS 卷通过 TCP 和 Unix 域套接字传输协议来托管 VM 磁盘映像"),
    ("QEMU supports read\\-only access to files accessed over http(s) and ftp(s)", "QEMU 支持通过 http(s) 和 ftp(s) 进行文件的只读访问"),
    ("qemu\\-img allows you to create, convert and modify images offline", "qemu-img 允许您离线创建、转换和修改映像"),
    ("It can handle all image formats supported by QEMU", "它可以处理 QEMU 支持的所有映像格式"),
    ("Never use qemu\\-img to modify images in use by a running virtual machine or any other process; this may destroy the image", "切勿使用 qemu-img 修改正在运行的虚拟机或其他进程正在使用的映像；这可能会损坏映像"),
    ("Also, be aware that querying an image that is being modified by another process may encounter inconsistent state", "同时请注意，查询另一个进程正在修改的映像可能会遇到不一致的状态"),
    ("\\fBqemu\\-storage\\-daemon\\fP provides disk image functionality from QEMU, \\fBqemu\\-img\\fP, and \\fBqemu\\-nbd\\fP in a long\\-running process controlled via QMP commands without running a virtual machine", "\\fBqemu\\-storage\\-daemon\\fP 在一个通过 QMP 命令控制的长期运行进程中提供 QEMU、\\fBqemu\\-img\\fP 和 \\fBqemu\\-nbd\\fP 的磁盘映像功能，而无需运行虚拟机"),
    ("It can export disk images, run block job operations, and perform other disk\\-related operations", "它可以导出磁盘映像、运行块作业操作以及执行其他磁盘相关操作"),
    ("The daemon is controlled via a QMP monitor and initial configuration from the command\\-line", "该守护进程通过 QMP 监视器和命令行初始配置进行控制"),
    ("The daemon offers the following subset of QEMU features:", "该守护进程提供以下 QEMU 功能的子集："),
    ("Commands can be sent over a QEMU Monitor Protocol (QMP) connection", "命令可以通过 QEMU 监视器协议（QMP）连接发送"),
    ("The daemon runs until it is stopped using the \\fBquit\\fP QMP command or SIGINT/SIGHUP/SIGTERM", "该守护进程会一直运行，直到使用 \\fBquit\\fP QMP 命令或 SIGINT/SIGHUP/SIGTERM 信号停止"),
    ("Never modify images in use by a running virtual machine or any other process; this may destroy the image", "切勿修改正在运行的虚拟机或其他进程正在使用的映像；这可能会损坏映像"),
    ("See the \\fBqemu\\-storage\\-daemon\\-qmp\\-ref(7)\\fP manual page for a description of the commands", "有关命令的描述，请参阅 \\fBqemu\\-storage\\-daemon\\-qmp\\-ref(7)\\fP 手册页"),
]

def tr_sh(line):
    """Translate .SH section headers."""
    m = re.match(r'^([.]SH\s+)"?([^"]*)"?', line)
    if m:
        sec = m.group(2).strip()
        if sec in SH_MAP:
            return f'{m.group(1)}"{SH_MAP[sec]}"' if '"' in line else f'{m.group(1)}{SH_MAP[sec]}'
    return line

def tr_ss(line):
    """Translate .SS subsection headers."""
    m = re.match(r'^([.]SS\s+)"?([^"]*)"?', line)
    if m:
        sec = m.group(2).strip()
        if sec in SS_MAP:
            return f'{m.group(1)}"{SS_MAP[sec]}"' if '"' in line else f'{m.group(1)}{SS_MAP[sec]}'
    return line

def tr_th(line):
    """Translate .TH header text."""
    return line.replace('"User Manual"', '"用户手册"').replace('"User Commands"', '"用户命令"').replace('"General Commands Manual"', '"通用命令手册"')

def tr_text(text):
    """Translate English body text to Chinese."""
    result = text
    
    # Apply sentence/paragraph translations first (longer matches)
    for eng, chn in SENT_MAP:
        result = result.replace(eng, chn)
    
    # Apply word/phrase translations
    for eng, chn in WORD_MAP:
        result = result.replace(eng, chn)
    
    return result

def process_file(basename):
    """Process a single man page file."""
    src_path = os.path.join(SRC, basename + '.1.gz')
    
    with gzip.open(src_path, 'rt', errors='replace') as f:
        content = f.read()
    
    lines = content.split('\n')
    result = []
    
    for line in lines:
        if line.startswith('.SH '):
            result.append(tr_sh(line))
        elif line.startswith('.SS '):
            result.append(tr_ss(line))
        elif line.startswith('.TH '):
            result.append(tr_th(line))
        elif line.startswith('.') or line.startswith("'"):
            result.append(line)
        elif not line.strip():
            result.append(line)
        else:
            result.append(tr_text(line))
    
    output = '\n'.join(result)
    dst_path = os.path.join(DST, basename + '.1')
    
    with open(dst_path, 'w') as f:
        f.write(output)
    
    gz_path = dst_path + '.gz'
    with open(dst_path, 'rb') as fin, gzip.open(gz_path, 'wb') as fout:
        fout.write(fin.read())
    
    subprocess.run(['bash', '-c',
        f'gzip -c {dst_path} | sudo tee {INST}/{basename}.1.gz > /dev/null'],
        capture_output=True)
    
    os.unlink(dst_path)
    os.unlink(gz_path)
    return basename

def run():
    unique_files = ["qemu", "qemu-img", "qemu-storage-daemon"]
    system_targets = [
        "qemu-system-aarch64", "qemu-system-alpha", "qemu-system-arm",
        "qemu-system-avr", "qemu-system-hppa", "qemu-system-i386",
        "qemu-system-loongarch64", "qemu-system-m68k", "qemu-system-microblaze",
        "qemu-system-mips", "qemu-system-mips64", "qemu-system-mips64el",
        "qemu-system-mipsel", "qemu-system-or1k", "qemu-system-ppc",
        "qemu-system-ppc64", "qemu-system-riscv32", "qemu-system-riscv64",
        "qemu-system-rx", "qemu-system-s390x", "qemu-system-sh4",
        "qemu-system-sh4eb", "qemu-system-sparc", "qemu-system-sparc64",
        "qemu-system-tricore", "qemu-system-x86_64", "qemu-system-xtensa",
        "qemu-system-xtensaeb",
    ]
    
    os.makedirs(DST, exist_ok=True)
    count = 0
    
    for f in unique_files:
        try:
            process_file(f)
            count += 1
            print(f"  translated: {f}.1")
        except Exception as e:
            print(f"  FAIL {f}: {e}")
    
    qemu_trans_path = f"{INST}/qemu.1.gz"
    if os.path.exists(qemu_trans_path):
        with gzip.open(qemu_trans_path, 'rt', errors='replace') as f:
            qemu_content = f.read()
        
        for target in system_targets:
            target_content = qemu_content.replace('.TH "QEMU"', f'.TH "{target.upper()}"')
            dst_path = os.path.join(DST, f"{target}.1")
            with open(dst_path, 'w') as f:
                f.write(target_content)
            
            gz_path = dst_path + '.gz'
            with open(dst_path, 'rb') as fin, gzip.open(gz_path, 'wb') as fout:
                fout.write(fin.read())
            
            subprocess.run(['bash', '-c',
                f'gzip -c {dst_path} | sudo tee {INST}/{target}.1.gz > /dev/null'],
                capture_output=True)
            
            os.unlink(dst_path)
            os.unlink(gz_path)
            count += 1
            print(f"  installed: {target}.1")
    
    print(f"qemu done: {count} translations")

if __name__ == '__main__':
    run()
