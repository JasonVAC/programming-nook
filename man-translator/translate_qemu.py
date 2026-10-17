#!/usr/bin/env python3
"""
Translate QEMU man pages to Chinese, preserving all roff formatting.
Handles: qemu.1, qemu-img.1, qemu-storage-daemon.1
"""
import os, re, gzip, subprocess

SRC = "/usr/share/man/man1"
DST = "/tmp/man1_zh"
INST = "/usr/share/man/zh_CN/man1"

# ── .SH / .SS header translations ──
SEC_MAP = {
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
    "AUTHOR": "作者",
    "AUTHORS": "作者",
}

SUBSEC_MAP = {
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
    "Machine-specific options": "机器特定选项",
    "Multiplexer Keys": "多路复用器按键",
    "Snapshotting during live migration": "在线迁移期间的快照",
    "Online Metadata Checking": "在线元数据检查",
}

# ── Common phrase translations (longest first) ──
PHRASES = [
    ("Enables or disables memory merge support", "启用或禁用内存合并支持"),
    ("When dealing with options parameters as arbitrary strings containing", "当使用包含"),
    ("This is used to enable an accelerator", "用于启用加速器"),
    ("Enables emulation of VMWare IO port, for vmmouse etc", "启用 VMWare IO 端口模拟，用于 vmmouse 等"),
    ("select the value based on accel", "根据加速器和"),
    ("Include guest memory in a core dump", "在核心转储中包含客户机内存"),
    ("Specify tracing options", "指定跟踪选项"),
    ("Immediately enable events matching", "立即启用匹配的"),
    ("either event name or a globbing pattern", "事件名或通配模式"),
    ("available if QEMU has been compiled with the", "仅在 QEMU 编译时启用了"),
    ("tracing backend", "跟踪后端时可用"),
    ("To specify multiple events or patterns,", "要指定多个事件或模式，"),
    ("Use \\fB\\-trace help\\fP to print a list of names of trace points", "使用 \\fB\\-trace help\\fP 打印跟踪点名称列表"),
    ("Immediately enable events listed in", "立即启用在"),
    ("The file must contain one event name", "文件中列出的"),
    ("per line; globbing patterns are accepted too", "事件，每行一个事件名称；也接受通配模式"),
    ("Log output traces to", "将输出跟踪日志写入"),
    ("Display this help and exit", "显示此帮助并退出"),
    ("Display version information and exit", "显示版本信息并退出"),
    ("Display help and exit", "显示帮助并退出"),
    ("The default is on", "默认启用"),
    ("The default is off", "默认禁用"),
    ("The default is none", "默认无"),
    ("the default is on", "默认启用"),
    ("the default is off", "默认禁用"),
    ("Default:", "默认值："),
    ("Enables or disables NVDIMM support", "启用或禁用 NVDIMM 支持"),
    ("Enables or disables ACPI Heterogeneous Memory Attribute Table", "启用或禁用 ACPI 异构内存属性表"),
    ("Enables or disables ACPI Serial Port Console Redirection Table", "启用或禁用 ACPI 串行端口控制台重定向表"),
    ("Allocate auxiliary guest RAM as an anonymous file that is", "分配辅助客户机 RAM 作为可共享的"),
    ("shareable with an external process", "匿名文件，可与外部进程共享"),
    ("This option applies to", "此选项适用于"),
    ("memory allocated as a side effect of creating various devices", "因创建各种设备而分配的内存"),
    ("It does not apply to memory-backend-objects, whether explicitly", "它不适用于内存后端对象，无论是显式指定的"),
    ("specified on the command line, or implicitly created by the", "还是由命令行选项隐式创建的"),
    ("command line option", "命令行选项"),
    ("To use the cpr-transfer migration mode, you must set", "要使用 cpr-transfer 迁移模式，必须设置"),
    ("An alternative to legacy", "传统"),
    ("Allows to use a memory backend as main RAM", "允许使用内存后端作为主 RAM"),
    ("For example:", "例如："),
    ("Example:", "示例："),
    ("Migration compatibility note:", "迁移兼容性注意事项："),
    ("as backend id one shall use value of", "在后端 id 中应使用"),
    ("advertised by machine type", "所公告的值"),
    ("if migration to/from old QEMU", "如果预期迁移到/从旧版 QEMU"),
    ("is expected", "如果期望"),
    ("for machine types 4.0 and older, user shall", "对于 4.0 及更早的机器类型，用户应"),
    ("backend option", "后端选项"),
    ("Define a CXL Fixed Memory Window", "定义一个 CXL 固定内存窗口"),
    ("Described in the CXL 2.0 ECN: CEDT CFMWS & QTG _DSM", "在 CXL 2.0 ECN: CEDT CFMWS & QTG _DSM 中描述"),
    ("They are regions of Host Physical Addresses", "它们是主机物理地址的区域"),
    ("which may be interleaved across one or more CXL host bridges", "可以跨越一个或多个 CXL 主机桥进行交错"),
    ("The system software will assign particular devices into these windows", "系统软件将特定设备分配到这些窗口"),
    ("configure the downstream Host-managed Device Memory", "并配置下游主机管理的设备内存"),
    ("decoders in root ports, switch ports and devices appropriately", "适当配置根端口、交换机端口和设备中的解码器"),
    ("to meet the interleave requirements before enabling the memory devices", "以满足交错要求后再启用内存设备"),
    ("provides the mapping to CXL host bridges", "提供到 CXL 主机桥的映射"),
    ("which may be identified by the id provided in the -device entry", "可通过 -device 条目中提供的 id 来标识"),
    ("Multiple entries are needed to specify all the targets", "需要多个条目来指定所有目标"),
    ("the fixed memory window represents interleaved memory", "固定内存窗口表示交错内存"),
    ("is the target index from", "是目标索引，从"),
    ("sets the size of the CFMW", "设置 CFMW 的大小"),
    ("This must be a multiple of", "必须是"),
    ("The region will be aligned to", "区域将对齐到"),
    ("but the location is platform and configuration dependent", "但位置取决于平台和配置"),
    ("sets the granularity of interleave", "设置交错粒度"),
    ("Only", "仅支持"),
    ("granularities supported", "粒度"),
    ("Define an SGX EPC section", "定义一个 SGX EPC 分区"),
    ("Define cache properties for SMP system", "定义 SMP 系统的缓存属性"),
    ("specifies the cache that the properties will be applied on", "指定将应用属性的缓存"),
    ("This field is the combination of cache level and cache type", "此字段是缓存级别和缓存类型的组合"),
    ("It supports", "它支持"),
    ("L1 data cache", "L1 数据缓存"),
    ("L1 instruction cache", "L1 指令缓存"),
    ("L2 unified cache", "L2 统一缓存"),
    ("L3 unified cache", "L3 统一缓存"),
    ("sets the cache topology level", "设置缓存拓扑级别"),
    ("CPU topology levels including", "CPU 拓扑级别，包括"),
    ("a special value", "一个特殊值"),
    ("then the cache topology will follow the architecture's", "则缓存拓扑将遵循架构的"),
    ("default cache topology model", "默认缓存拓扑模型"),
    ("If another topology level is set, the cache", "如果设置了其他拓扑级别，缓存"),
    ("will be shared at corresponding CPU topology level", "将在相应的 CPU 拓扑级别共享"),
    ("makes the cache shared by all threads within a core", "使缓存在核心内的所有线程之间共享"),
    ("will default to using the", "将默认使用"),
    ("The default cache topology model for an i386 PC machine is as follows", "i386 PC 机器的默认缓存拓扑模型如下"),
    ("caches are per", "缓存是每个"),
    ("cache is per", "缓存是每个"),
    ("Display help", "显示帮助"),
    ("Display version information", "显示版本信息"),
    ("Select the emulated machine by name", "按名称选择模拟的机器"),
    ("list available machines", "列出可用的机器"),
    ("For architectures which aim to support live migration compatibility", "对于旨在支持跨版本在线迁移兼容性的架构"),
    ("each release will introduce a new versioned machine type", "每个版本都会引入一个新的带版本号的机器类型"),
    ("For example, the 2.8.0 release introduced machine types", "例如，2.8.0 版本引入了机器类型"),
    ("To allow live migration of guests from", "为了允许将客户机从"),
    ("version must support the", "版本必须支持"),
    ("machines too", "机器"),
    ("To allow users live migrating VMs to", "为了允许用户"),
    ("skip multiple intermediate releases when upgrading", "在升级时跳过多个中间版本"),
    ("new releases of QEMU will support machine types from many previous versions", "新版本的 QEMU 将支持许多先前版本的机器类型"),
    ("Supported machine properties are:", "支持的机器属性有："),
    ("Depending on the target architecture", "根据目标架构"),
    ("can be available", "可能可用"),
    ("tcg is used", "使用 tcg"),
    ("If there is more than one accelerator specified", "如果指定了多个加速器"),
    ("the next one is used if the previous one fails to initialize", "如果前一个初始化失败，则使用下一个"),
    ("auto says to select the value based on accel and i8042", "auto 表示根据 accel 和 i8042 选择值"),
    ("For accel=xen or i8042=off the default is off otherwise the default is on", "对于 accel=xen 或 i8042=off，默认值为 off，否则默认值为 on"),
    ("This feature, when supported by the host, de-duplicates identical memory pages among VMs instances", "此功能在主机支持时，可对 VM 实例之间相同的内存页进行去重"),
    ("enabled by default", "默认启用"),
    ("disabled by default", "默认禁用"),
    ("Enables or disables AES key wrapping support on s390-ccw hosts", "启用或禁用 s390-ccw 主机上的 AES 密钥封装支持"),
    ("This feature controls whether AES wrapping keys will be created", "此功能控制是否创建 AES 封装密钥"),
    ("to allow execution of AES cryptographic functions", "以允许执行 AES 加密函数"),
    ("Enables or disables DEA key wrapping support on s390-ccw hosts", "启用或禁用 s390-ccw 主机上的 DEA 密钥封装支持"),
    ("This feature controls whether DEA wrapping keys will be created", "此功能控制是否创建 DEA 封装密钥"),
    ("to allow execution of DEA cryptographic functions", "以允许执行 DEA 加密函数"),
    ("Memory encryption object to use", "要使用的内存加密对象"),
    ("HMAT support", "HMAT 支持"),
    ("SPCR support", "SPCR 支持"),
    ("Define a block device", "定义一个块设备"),
    ("Sets the drive sector size", "设置驱动器扇区大小"),
    ("disk_image is a raw hard disk image for IDE hard disk 0", "disk_image 是用于 IDE 硬盘 0 的原始硬盘映像"),
    ("Some targets do not need a disk image", "某些目标不需要磁盘映像"),
    ("such as in", "例如在"),
    ("it's necessary to double the commas", "需要将逗号加倍"),
    ("will be parsed as", "将被解析为"),
    ("The QEMU PC System emulator simulates the following peripherals:", "QEMU PC 系统模拟器模拟以下外设："),
    ("i440FX host PCI bridge and PIIX3 PCI to ISA bridge", "i440FX 主机 PCI 桥和 PIIX3 PCI 到 ISA 桥"),
    ("Cirrus CLGD 5446 PCI VGA card or dummy VGA card with Bochs VESA extensions", "Cirrus CLGD 5446 PCI VGA 卡或带有 Bochs VESA 扩展的虚拟 VGA 卡"),
    ("hardware level, including all non standard modes", "硬件级别，包括所有非标准模式"),
    ("PS/2 mouse and keyboard", "PS/2 鼠标和键盘"),
    ("2 PCI IDE interfaces with hard disk and CD-ROM support", "2 个 PCI IDE 接口，支持硬盘和 CD-ROM"),
    ("Floppy disk", "软盘"),
    ("PCI and ISA network adapters", "PCI 和 ISA 网络适配器"),
    ("Serial ports", "串行端口"),
    ("IPMI BMC, either and internal or external one", "IPMI BMC，内部或外部"),
    ("Creative SoundBlaster 16 sound card", "Creative SoundBlaster 16 声卡"),
    ("ENSONIQ AudioPCI ES1370 sound card", "ENSONIQ AudioPCI ES1370 声卡"),
    ("Intel 82801AA AC97 Audio compatible sound card", "Intel 82801AA AC97 Audio 兼容声卡"),
    ("Intel HD Audio Controller and HDA codec", "Intel HD Audio 控制器和 HDA 编解码器"),
    ("Adlib (OPL2) - Yamaha YM3812 compatible chip", "Adlib (OPL2) - Yamaha YM3812 兼容芯片"),
    ("Gravis Ultrasound GF1 sound card", "Gravis Ultrasound GF1 声卡"),
    ("CS4231A compatible sound card", "CS4231A 兼容声卡"),
    ("PC speaker", "PC 扬声器"),
    ("PCI UHCI, OHCI, EHCI or XHCI USB controller and a virtual USB-1.1 hub", "PCI UHCI、OHCI、EHCI 或 XHCI USB 控制器和虚拟 USB-1.1 集线器"),
    ("SMP is supported with a large number of virtual CPUs", "SMP 支持大量虚拟 CPU"),
    ("upper limit is configuration dependent", "上限取决于配置"),
    ("QEMU uses the PC BIOS from the Seabios project and the Plex86/Bochs LGPL VGA BIOS", "QEMU 使用来自 Seabios 项目的 PC BIOS 和 Plex86/Bochs LGPL VGA BIOS"),
    ("QEMU uses YM3812 emulation by Tatsuyuki Satoh", "QEMU 使用 Tatsuyuki Satoh 编写的 YM3812 模拟"),
    ("Note that, by default, GUS shares IRQ(7) with parallel ports", "注意，默认情况下 GUS 与并行端口共享 IRQ(7)"),
    ("QEMU must be told to not have parallel ports to have working GUS", "必须告知 QEMU 不使用并行端口才能使 GUS 正常工作"),
    ("Alternatively:", "或者："),
    ("Or some other unclaimed IRQ", "或其他未占用的 IRQ"),
    ("CS4231A is the chip used in Windows Sound System and GUSMAX products", "CS4231A 是 Windows Sound System 和 GUSMAX 产品中使用的芯片"),
    ("The PC speaker audio device can be configured using the pcspk-audiodev machine property", "PC 扬声器音频设备可以使用 pcspk-audiodev 机器属性进行配置"),
    ("It supports the following machine-specific options:", "它支持以下机器特定选项："),
    ("Experimental option to select a particular south bridge", "选择特定南桥的实验性选项"),
    ("commands are supported:", "支持以下命令："),
    ("The following commands are supported:", "支持以下命令："),
    ("a raw hard disk image for IDE hard disk 0", "用于 IDE 硬盘 0 的原始硬盘映像"),
    ("from the following table", "从下表中"),
    ("the modifier is", "修饰键是"),
    ("used in the table below", "在下表中使用"),
    ("which can be changed with", "可以使用"),
    ("suboption", "子选项"),
    ("where appropriate", "在适用的情况下"),
    ("changes the modifier key to", "将修饰键更改为"),
    ("changes it to the right", "将其更改为右侧"),
    ("Toggle full screen", "切换全屏"),
    ("Enlarge the screen", "放大屏幕"),
    ("Shrink the screen", "缩小屏幕"),
    ("Restore the screen's un-scaled dimensions", "恢复屏幕的未缩放尺寸"),
    ("Switch to virtual console", "切换到虚拟控制台"),
    ("Standard console mappings are:", "标准控制台映射："),
    ("Target system display", "目标系统显示"),
    ("Monitor", "监视器"),
    ("Serial port", "串行端口"),
    ("Toggle mouse and keyboard grab", "切换鼠标和键盘捕获"),
    ("During the graphical emulation, you can use special key combinations", "在图形模拟期间，您可以使用特殊键组合"),
    ("By default the modifier is", "默认修饰键是"),
    ("to change modes", "来切换模式"),
    ("you can use", "您可以使用"),
    ("to move in the back log", "在后台日志中导航"),
    ("During emulation, if you are using a character backend multiplexer", "在模拟期间，如果您使用字符后端多路复用器"),
    ("which is the default if you are using", "这是使用"),
    ("then several commands are available via an escape sequence", "时的默认值）多个命令可通过转义序列使用"),
    ("These key sequences all start with an escape character, which is", "这些按键序列都以转义字符开头，默认是"),
    ("by default, but can be changed with", "但可以通过以下方式更改"),
    ("The list below assumes you're using the default", "以下列表假设您使用默认值"),
    ("Print this help", "打印此帮助"),
    ("Exit emulator", "退出模拟器"),
    ("Save disk data back to file (if -snapshot)", "将磁盘数据保存回文件（如果使用 -snapshot）"),
    ("Toggle console timestamps", "切换控制台时间戳"),
    ("Send break (magic sysrq in Linux)", "发送中断信号（Linux 中的 magic sysrq）"),
    ("Rotate between the frontends connected to the multiplexer", "在连接到多路复用器的前端之间切换"),
    ("usually this switches between the monitor and the console", "通常这是在监视器和控制台之间切换"),
    ("Send the escape character to the frontend", "将转义字符发送到前端"),
    ("In addition to using normal file images for the emulated storage devices", "除了使用普通文件映像作为模拟存储设备外"),
    ("QEMU can also use networked resources such as iSCSI devices", "QEMU 还可以使用 iSCSI 设备等网络资源"),
    ("These are specified using a special URL syntax", "这些使用特殊的 URL 语法指定"),
    ("iSCSI support allows QEMU to access iSCSI resources directly and use as images for the guest storage", "iSCSI 支持允许 QEMU 直接访问 iSCSI 资源并将其用作客户机存储的映像"),
    ("Both disk and cdrom images are supported", "支持磁盘和 cdrom 映像"),
    ("Syntax for specifying iSCSI LUNs is", "指定 iSCSI LUN 的语法是"),
    ("By default qemu will use the iSCSI initiator-name", "默认情况下，qemu 将使用 iSCSI 发起程序名称"),
    ("but this can also be set from the command line or a configuration file", "但也可以从命令行或配置文件设置"),
    ("Since version", "自从版本"),
    ("it is possible to specify a iSCSI request timeout to detect stalled requests", "可以指定 iSCSI 请求超时以检测停滞的请求"),
    ("and force a reestablishment of the session", "并强制重新建立会话"),
    ("The timeout is specified in seconds", "超时以秒为单位指定"),
    ("means no timeout", "表示无超时"),
    ("or greater is required for this feature", "或更高版本才能使用此功能"),
    ("Example (without authentication):", "示例（无身份验证）："),
    ("Example (CHAP username/password via URL):", "示例（通过 URL 进行 CHAP 用户名/密码验证）："),
    ("Example (CHAP username/password via environment variables):", "示例（通过环境变量进行 CHAP 用户名/密码验证）："),
    ("QEMU supports NBD (Network Block Devices) both using TCP protocol as well as Unix Domain Sockets", "QEMU 支持使用 TCP 协议和 Unix 域套接字的 NBD（网络块设备）"),
    ("With TCP, the default port is", "使用 TCP 时，默认端口是"),
    ("Syntax for specifying a NBD device using TCP, in preferred URI form:", "使用 TCP 指定 NBD 设备的语法（首选 URI 格式）："),
    ("Syntax for specifying a NBD device using Unix Domain Sockets;", "使用 Unix 域套接字指定 NBD 设备的语法；"),
    ("remember that", "请记住"),
    ("is a shell glob character and may need quoting:", "是 shell 通配符，可能需要引号："),
    ("Older syntax that is also recognized:", "也支持的旧语法："),
    ("Example for TCP", "TCP 示例"),
    ("Example for Unix Domain Sockets", "Unix 域套接字示例"),
    ("QEMU supports SSH (Secure Shell) access to remote disks", "QEMU 支持通过 SSH（安全外壳）访问远程磁盘"),
    ("Currently authentication must be done using ssh-agent", "目前必须使用 ssh-agent 进行身份验证"),
    ("Other authentication methods may be supported in future", "将来可能支持其他身份验证方法"),
    ("GlusterFS is a user space distributed file system", "GlusterFS 是一个用户空间分布式文件系统"),
    ("QEMU supports the use of GlusterFS volumes for hosting VM disk images", "QEMU 支持使用 GlusterFS 卷来托管 VM 磁盘映像"),
    ("using TCP and Unix Domain Sockets transport protocols", "使用 TCP 和 Unix 域套接字传输协议"),
    ("Syntax for specifying a VM disk image on GlusterFS volume is", "在 GlusterFS 卷上指定 VM 磁盘映像的语法为"),
    ("QEMU supports read-only access to files accessed over http(s) and ftp(s)", "QEMU 支持对通过 http(s) 和 ftp(s) 访问的文件进行只读访问"),
    ("Syntax using a single filename:", "使用单个文件名的语法："),
]

def tr_sh(line):
    """Translate .SH section headers."""
    m = re.match(r'^([.]SH\s+)"?([^"]*)"?', line)
    if m:
        prefix = m.group(1)
        sec = m.group(2).strip()
        for eng, chn in sorted(SEC_MAP.items(), key=lambda x: -len(x[0])):
            if sec == eng or sec.upper() == eng.upper():
                return f'{prefix}"{chn}"' if '"' in line else f'{prefix}{chn}'
    return line

def tr_ss(line):
    """Translate .SS subsection headers."""
    m = re.match(r'^([.]SS\s+)"?([^"]*)"?', line)
    if m:
        prefix = m.group(1)
        sec = m.group(2).strip()
        for eng, chn in sorted(SUBSEC_MAP.items(), key=lambda x: -len(x[0])):
            if sec == eng:
                return f'{prefix}"{chn}"' if '"' in line else f'{prefix}{chn}'
    return line

def tr_th(line):
    """Translate .TH header text."""
    line = line.replace('"User Manual"', '"用户手册"')
    line = line.replace('"User Commands"', '"用户命令"')
    line = line.replace('"General Commands Manual"', '"通用命令手册"')
    return line

def tr_text(text):
    """Translate English body text to Chinese using phrase mapping."""
    result = text
    for eng, chn in sorted(PHRASES, key=lambda x: -len(x[0])):
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
        # Handle roff commands
        if line.startswith('.SH '):
            result.append(tr_sh(line))
        elif line.startswith('.SS '):
            result.append(tr_ss(line))
        elif line.startswith('.TH '):
            result.append(tr_th(line))
        elif line.startswith('.'):
            # Pass other roff commands through unchanged
            result.append(line)
        elif line.startswith("'"):
            # roff comment/control
            result.append(line)
        elif not line.strip():
            result.append(line)
        else:
            # Body text - translate
            result.append(tr_text(line))
    
    output = '\n'.join(result)
    dst_path = os.path.join(DST, basename)
    
    with open(dst_path, 'w') as f:
        f.write(output)
    
    # Gzip
    gz_path = dst_path + '.gz'
    with open(dst_path, 'rb') as fin, gzip.open(gz_path, 'wb') as fout:
        fout.write(fin.read())
    
    # Install using the user's preferred method
    subprocess.run(['bash', '-c', 
        f'gzip -c {dst_path} | sudo tee {INST}/{basename}.1.gz > /dev/null'],
        capture_output=True)
    
    # Cleanup
    os.unlink(dst_path)
    os.unlink(gz_path)
    return basename

def run():
    # The three unique files
    unique_files = [
        "qemu",
        "qemu-img",
        "qemu-storage-daemon",
    ]
    
    # All system emulator variants (all point to the same content)
    system_targets = [
        "qemu-system-aarch64",
        "qemu-system-alpha",
        "qemu-system-arm",
        "qemu-system-avr",
        "qemu-system-hppa",
        "qemu-system-i386",
        "qemu-system-loongarch64",
        "qemu-system-m68k",
        "qemu-system-microblaze",
        "qemu-system-mips",
        "qemu-system-mips64",
        "qemu-system-mips64el",
        "qemu-system-mipsel",
        "qemu-system-or1k",
        "qemu-system-ppc",
        "qemu-system-ppc64",
        "qemu-system-riscv32",
        "qemu-system-riscv64",
        "qemu-system-rx",
        "qemu-system-s390x",
        "qemu-system-sh4",
        "qemu-system-sh4eb",
        "qemu-system-sparc",
        "qemu-system-sparc64",
        "qemu-system-tricore",
        "qemu-system-x86_64",
        "qemu-system-xtensa",
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
    
    # For system emulator variants, copy the translated qemu.1 with .TH fix
    qemu_trans_path = f"{INST}/qemu.1.gz"
    if os.path.exists(qemu_trans_path):
        with gzip.open(qemu_trans_path, 'rt', errors='replace') as f:
            qemu_content = f.read()
        
        for target in system_targets:
            # Replace .TH QEMU -> .TH <TARGET>
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
