#!/usr/bin/env python3
"""Final QEMU man page translator with expanded vocabulary."""
import os, re, gzip, subprocess

SRC = "/usr/share/man/man1"
DST = "/tmp/man1_zh"
INST = "/usr/share/man/zh_CN/man1"

SH_MAP = {"NAME":"名称","SYNOPSIS":"语法","DESCRIPTION":"描述","OPTIONS":"选项","NOTES":"注释","SEE ALSO":"参见","EXAMPLES":"示例","EXAMPLE":"示例","Author":"作者","Copyright":"版权","BUGS":"缺陷","Multiplexer Keys":"多路复用器按键","Key Sequence":"按键序列","Action":"操作"}
SS_MAP = {"Machine\\-specific options":"机器特定选项","Standard options":"标准选项","Block device options":"块设备选项","USB convenience options":"USB 便捷选项","Display options":"显示选项","i386 target only":"仅限 i386 目标","Network options":"网络选项","Character device options":"字符设备选项","TPM device options":"TPM 设备选项","Boot Image or Kernel specific":"启动映像或内核特定选项","Debug/Expert options":"调试/专家选项","Generic object creation":"通用对象创建","Multiplexer Keys":"多路复用器按键"}

# Comprehensive regex patterns - ordered longest first
RX = [
    # ── Full sentences (must come before word-level) ──
    (r'Display help and exit', '显示帮助并退出'),
    (r'Display this help and exit', '显示此帮助并退出'),
    (r'Display version information and exit', '显示版本信息并退出'),
    (r'Select the emulated machine by name', '按名称选择模拟的机器'),
    (r'Use \\fB\\-machine help\\fP to list available machines', '使用 \\fB\\-machine help\\fP 列出可用的机器'),
    (r'QEMU User Documentation', 'QEMU 用户文档'),
    (r'QEMU disk image utility', 'QEMU 磁盘映像工具'),
    (r'QEMU storage daemon', 'QEMU 存储守护进程'),
    (r'The QEMU PC System emulator simulates the following peripherals:', 'QEMU PC 系统模拟器模拟以下外设：'),
    (r'QEMU uses the PC BIOS from the Seabios project and the Plex86/Bochs LGPL VGA BIOS', 'QEMU 使用来自 Seabios 项目的 PC BIOS 和 Plex86/Bochs LGPL VGA BIOS'),
    (r'QEMU uses YM3812 emulation by Tatsuyuki Satoh', 'QEMU 使用 Tatsuyuki Satoh 编写的 YM3812 模拟'),
    (r'QEMU uses GUS emulation \(GUSEMU32 .*\) by Tibor .+ Schütz', 'QEMU 使用 Tibor "TS" Schütz 编写的 GUS 模拟（GUSEMU32）'),
    (r'Note that, by default, GUS shares IRQ\(7\) with parallel ports and so QEMU must be told to not have parallel ports to have working GUS', '请注意，默认情况下 GUS 与并行端口共享 IRQ(7)，因此必须告知 QEMU 不使用并行端口才能使 GUS 正常工作'),

    # ── Peripherals ──
    (r'i440FX host PCI bridge and PIIX3 PCI to ISA bridge', 'i440FX 主机 PCI 桥和 PIIX3 PCI 到 ISA 桥'),
    (r'Cirrus CLGD 5446 PCI VGA card or dummy VGA card with Bochs VESA extensions \(hardware level, including all non standard modes\)', 'Cirrus CLGD 5446 PCI VGA 卡或带有 Bochs VESA 扩展的虚拟 VGA 卡（硬件级别，包括所有非标准模式）'),
    (r'PS/2 mouse and keyboard', 'PS/2 鼠标和键盘'),
    (r'2 PCI IDE interfaces with hard disk and CD\\-ROM support', '2 个 PCI IDE 接口，支持硬盘和 CD-ROM'),
    (r'Floppy disk', '软盘'),
    (r'PCI and ISA network adapters', 'PCI 和 ISA 网络适配器'),
    (r'Serial ports', '串行端口'),
    (r'IPMI BMC, either and internal or external one', 'IPMI BMC，内部或外部均可'),
    (r'Creative SoundBlaster 16 sound card', 'Creative SoundBlaster 16 声卡'),
    (r'ENSONIQ AudioPCI ES1370 sound card', 'ENSONIQ AudioPCI ES1370 声卡'),
    (r'Intel 82801AA AC97 Audio compatible sound card', 'Intel 82801AA AC97 Audio 兼容声卡'),
    (r'Intel HD Audio Controller and HDA codec', 'Intel HD Audio 控制器和 HDA 编解码器'),
    (r'Adlib \(OPL2\) \\- Yamaha YM3812 compatible chip', 'Adlib (OPL2) - Yamaha YM3812 兼容芯片'),
    (r'Gravis Ultrasound GF1 sound card', 'Gravis Ultrasound GF1 声卡'),
    (r'CS4231A compatible sound card', 'CS4231A 兼容声卡'),
    (r'PC speaker', 'PC 扬声器'),
    (r'PCI UHCI, OHCI, EHCI or XHCI USB controller and a virtual USB\\-1\\.1 hub', 'PCI UHCI、OHCI、EHCI 或 XHCI USB 控制器和虚拟 USB-1.1 集线器'),
    (r'SMP is supported with a large number of virtual CPUs \(upper limit is configuration dependent\)', 'SMP 支持大量虚拟 CPU（上限取决于配置）'),
    (r"CS4231A is the chip used in Windows Sound System and GUSMAX products", "CS4231A 是 Windows Sound System 和 GUSMAX 产品中使用的芯片"),
    (r"The PC speaker audio device can be configured using the pcspk\\-audiodev machine property", "PC 扬声器音频设备可以使用 pcspk-audiodev 机器属性进行配置"),
    (r'It supports the following machine\\-specific options:', '支持以下机器特定选项：'),
    (r'Experimental option to select a particular south bridge', '选择特定南桥的实验性选项'),
    (r'disk_image is a raw hard disk image for IDE hard disk 0', 'disk_image 是用于 IDE 硬盘 0 的原始硬盘映像'),
    (r'Some targets do not need a disk image', '某些目标不需要磁盘映像'),
    (r'When dealing with options parameters as arbitrary strings containing commas', '当处理包含逗号的选项参数字符串时'),
    (r'it\(aqs necessary to double the commas', '需要将逗号加倍'),
    (r'will be parsed as', '将被解析为'),

    # ── Table actions ──
    (r'Toggle full screen', '切换全屏'),
    (r'Enlarge the screen', '放大屏幕'),
    (r'Shrink the screen', '缩小屏幕'),
    (r"Restore the screen\(aqs un\-scaled dimensions", '恢复屏幕的未缩放尺寸'),
    (r'Switch to virtual console', '切换到虚拟控制台'),
    (r'Toggle mouse and keyboard grab', '切换鼠标和键盘捕获'),
    (r'Print this help', '打印此帮助'),
    (r'Exit emulator', '退出模拟器'),
    (r'Save disk data back to file \(if \\-snapshot\)', '将磁盘数据保存回文件（如果使用 -snapshot）'),
    (r'Toggle console timestamps', '切换控制台时间戳'),
    (r'Send break \(magic sysrq in Linux\)', '发送中断信号（Linux 中的 magic sysrq）'),
    (r'Send the escape character to the frontend', '将转义字符发送到前端'),
    (r'Standard console mappings are:', '标准控制台映射：'),
    (r'Target system display', '目标系统显示'),
    (r'Rotate between the frontends connected to the multiplexer \(usually this switches between the monitor and the console\)', '在连接到多路复用器的前端之间切换（通常是在监视器和控制台之间切换）'),
    (r'During the graphical emulation, you can use special key combinations from the following table to change modes', '在图形模拟期间，您可以使用下表中的特殊键组合来切换模式'),
    (r'During emulation, if you are using a character backend multiplexer \(which is the default if you are using .+\) then several commands are available via an escape sequence', '在模拟期间，如果您使用字符后端多路复用器（使用 -nographic 时的默认值），则多个命令可通过转义序列使用'),

    # ── Storage networking ──
    (r"In addition to using normal file images for the emulated storage devices", '除了使用普通文件映像作为模拟存储设备外'),
    (r"QEMU can also use networked resources such as iSCSI devices", 'QEMU 还可以使用 iSCSI 等网络资源'),
    (r"iSCSI support allows QEMU to access iSCSI resources directly and use as images for the guest storage", 'iSCSI 支持允许 QEMU 直接访问 iSCSI 资源并将其用作客户机存储的映像'),
    (r"Syntax for specifying iSCSI LUNs is", '指定 iSCSI LUN 的语法为'),
    (r"By default qemu will use the iSCSI initiator\\-name", '默认情况下 qemu 将使用 iSCSI 发起程序名称'),
    (r"but this can also be set from the command line or a configuration file", '但也可以从命令行或配置文件设置'),
    (r"QEMU supports NBD \(Network Block Devices\) both using TCP protocol as well as Unix Domain Sockets", 'QEMU 支持使用 TCP 协议和 Unix 域套接字的 NBD（网络块设备）'),
    (r"QEMU supports SSH \(Secure Shell\) access to remote disks", 'QEMU 支持通过 SSH（安全外壳协议）访问远程磁盘'),
    (r"Currently authentication must be done using ssh\\-agent", '目前必须通过 ssh-agent 进行身份验证'),
    (r"Other authentication methods may be supported in future", '将来可能支持其他身份验证方法'),
    (r"GlusterFS is a user space distributed file system", 'GlusterFS 是一个用户空间分布式文件系统'),
    (r"QEMU supports the use of GlusterFS volumes for hosting VM disk images using TCP and Unix Domain Sockets transport protocols", 'QEMU 支持使用 GlusterFS 卷通过 TCP 和 Unix 域套接字传输协议来托管 VM 磁盘映像'),
    (r"QEMU supports read\\-only access to files accessed over http\(s\) and ftp\(s\)", 'QEMU 支持通过 http(s) 和 ftp(s) 对文件进行只读访问'),

    # ── qemu-img specific ──
    (r"qemu\\-img allows you to create, convert and modify images offline", 'qemu-img 允许您离线创建、转换和修改映像'),
    (r"It can handle all image formats supported by QEMU", '它可以处理 QEMU 支持的所有映像格式'),
    (r"Never use qemu\\-img to modify images in use by a running virtual machine or any other process; this may destroy the image", '切勿使用 qemu-img 修改正在运行的虚拟机或其他进程正在使用的映像；这可能会损坏映像'),
    (r"Also, be aware that querying an image that is being modified by another process may encounter inconsistent state", '同时请注意，查询另一个进程正在修改的映像可能会遇到不一致的状态'),

    # ── qemu-storage-daemon specific ──
    (r"The daemon offers the following subset of QEMU features:", '该守护进程提供以下 QEMU 功能的子集：'),
    (r"Commands can be sent over a QEMU Monitor Protocol \(QMP\) connection", '命令可以通过 QEMU 监视器协议（QMP）连接发送'),
    (r"The daemon runs until it is stopped using the \\fBquit\\fP QMP command or SIGINT/SIGHUP/SIGTERM", '该守护进程会一直运行，直到使用 \\fBquit\\fP QMP 命令或 SIGINT/SIGHUP/SIGTERM 终止'),
    (r"Never modify images in use by a running virtual machine or any other process; this may destroy the image", '切勿修改正在运行的虚拟机或其他进程正在使用的映像；这可能会损坏映像'),
    (r"provides disk image functionality from QEMU.*controlled via QMP commands without running a virtual machine", '在一个通过 QMP 命令控制的长期运行进程中提供 QEMU、qemu-img 和 qemu-nbd 的磁盘映像功能，而无需运行虚拟机'),

    # ── Verb patterns (standalone) ──
    (r'\bSpecifies\b', '指定'),
    (r'\bspecifies\b', '指定'),
    (r'\bSpecify\b', '指定'),
    (r'\bDetermines\b', '确定'),
    (r'\bdetermines\b', '确定'),
    (r'\bConfigures\b', '配置'),
    (r'\bconfigures\b', '配置'),
    (r'\bProvides\b', '提供'),
    (r'\bprovides\b', '提供'),
    (r'\bRequires\b', '需要'),
    (r'\brequires\b', '需要'),
    (r'\bGenerates\b', '生成'),
    (r'\bgenerates\b', '生成'),
    (r'\bCreates\b', '创建'),
    (r'\bcreates\b', '创建'),
    (r'\bRemoves\b', '移除'),
    (r'\bremoves\b', '移除'),
    (r'\bDeletes\b', '删除'),
    (r'\bdeletes\b', '删除'),
    (r'\bReturns\b', '返回'),
    (r'\breturns\b', '返回'),
    (r'\bIndicates\b', '表示'),
    (r'\bindicates\b', '表示'),
    (r'\bDefines\b', '定义'),
    (r'\bdefines\b', '定义'),
    (r'\bSuggests\b', '建议'),
    (r'\bsuggests\b', '建议'),
    (r'\bAllows\b', '允许'),
    (r'\ballows\b', '允许'),
    (r'\bSupports\b', '支持'),
    (r'\bsupports\b', '支持'),
    (r'\bControls\b', '控制'),
    (r'\bcontrols\b', '控制'),
    (r'\bContains\b', '包含'),
    (r'\bcontains\b', '包含'),
    (r'\bDisplays\b', '显示'),
    (r'\bdisplays\b', '显示'),
    (r'\bShows\b', '显示'),
    (r'\bshows\b', '显示'),
    (r'\bUses\b', '使用'),
    (r'\buses\b', '使用'),
    (r'\bSets\b', '设置'),
    (r'\bsets\b', '设置'),
    (r'\bRuns\b', '运行'),
    (r'\bruns\b', '运行'),
    (r'\bRunning\b', '运行'),
    (r'\bLoads\b', '加载'),
    (r'\bloads\b', '加载'),
    (r'\bEnables\b', '启用'),
    (r'\benables\b', '启用'),
    (r'\bDisables\b', '禁用'),
    (r'\bdisables\b', '禁用'),
    (r'\bEnabled\b', '已启用'),
    (r'\benabled\b', '已启用'),
    (r'\bDisabled\b', '已禁用'),
    (r'\bdisabled\b', '已禁用'),
    (r'\bUsed\b', '用于'),
    (r'\bused\b', '用于'),

    # ── Nouns ──
    (r'\boption\b', '选项'), (r'\bOption\b', '选项'),
    (r'\boptions\b', '选项'), (r'\bOptions\b', '选项'),
    (r'\bcommand\b', '命令'), (r'\bCommand\b', '命令'),
    (r'\bcommands\b', '命令'), (r'\bCommands\b', '命令'),
    (r'\bdevice\b', '设备'), (r'\bDevice\b', '设备'),
    (r'\bdevices\b', '设备'), (r'\bDevices\b', '设备'),
    (r'\bfile\b', '文件'), (r'\bFile\b', '文件'),
    (r'\bfiles\b', '文件'), (r'\bFiles\b', '文件'),
    (r'\bparameter\b', '参数'), (r'\bParameter\b', '参数'),
    (r'\bparameters\b', '参数'), (r'\bParameters\b', '参数'),
    (r'\bproperty\b', '属性'), (r'\bProperty\b', '属性'),
    (r'\bproperties\b', '属性'), (r'\bProperties\b', '属性'),
    (r'\bsupport\b', '支持'), (r'\bSupport\b', '支持'),
    (r'\bbackend\b', '后端'), (r'\bBackend\b', '后端'),
    (r'\bfrontend\b', '前端'),
    (r'\bfront\\-end\b', '前端'),
    (r'\bdriver\b', '驱动'), (r'\bDriver\b', '驱动'),
    (r'\bdrivers\b', '驱动'), (r'\bDrivers\b', '驱动'),
    (r'\bnetwork\b', '网络'), (r'\bNetwork\b', '网络'),
    (r'\bmemory\b', '内存'), (r'\bMemory\b', '内存'),
    (r'\bemulation\b', '模拟'), (r'\bEmulation\b', '模拟'),
    (r'\bemulator\b', '模拟器'), (r'\bEmulator\b', '模拟器'),
    (r'\bconfiguration\b', '配置'), (r'\bConfiguration\b', '配置'),
    (r'\bmigration\b', '迁移'), (r'\bMigration\b', '迁移'),
    (r'\baudio\b', '音频'), (r'\bAudio\b', '音频'),
    (r'\bvideo\b', '视频'), (r'\bVideo\b', '视频'),
    (r'\bsocket\b', '套接字'), (r'\bSocket\b', '套接字'),
    (r'\bport\b', '端口'), (r'\bPort\b', '端口'),
    (r'\bprotocol\b', '协议'), (r'\bProtocol\b', '协议'),
    (r'\binterface\b', '接口'), (r'\bInterface\b', '接口'),
    (r'\bformat\b', '格式'), (r'\bFormat\b', '格式'),
    (r'\bformats\b', '格式'),
    (r'\bsize\b', '大小'), (r'\bSize\b', '大小'),
    (r'\bmode\b', '模式'), (r'\bMode\b', '模式'),
    (r'\bmodes\b', '模式'),
    (r'\btype\b', '类型'), (r'\bType\b', '类型'),
    (r'\btypes\b', '类型'),
    (r'\bvalue\b', '值'), (r'\bValue\b', '值'),
    (r'\bvalues\b', '值'),
    (r'\bname\b', '名称'), (r'\bName\b', '名称'),
    (r'\bnames\b', '名称'),
    (r'\baddress\b', '地址'), (r'\bAddress\b', '地址'),
    (r'\boutput\b', '输出'), (r'\bOutput\b', '输出'),
    (r'\binput\b', '输入'), (r'\bInput\b', '输入'),
    (r'\bhost\b', '主机'), (r'\bHost\b', '主机'),
    (r'\bguest\b', '客户机'), (r'\bGuest\b', '客户机'),
    (r'\bserver\b', '服务器'), (r'\bServer\b', '服务器'),
    (r'\bclient\b', '客户端'), (r'\bClient\b', '客户端'),
    (r'\buser\b', '用户'), (r'\bUser\b', '用户'),
    (r'\bdirectory\b', '目录'), (r'\bDirectory\b', '目录'),
    (r'\bpath\b', '路径'), (r'\bPath\b', '路径'),
    (r'\bimage\b', '映像'), (r'\bImage\b', '映像'),
    (r'\bimages\b', '映像'), (r'\bImages\b', '映像'),
    (r'\bsession\b', '会话'), (r'\bSession\b', '会话'),
    (r'\bprocess\b', '进程'), (r'\bProcess\b', '进程'),
    (r'\berror\b', '错误'), (r'\bError\b', '错误'),
    (r'\bconnection\b', '连接'), (r'\bConnection\b', '连接'),

    # ── Adjectives ──
    (r'\bavailable\b', '可用'), (r'\bAvailable\b', '可用'),
    (r'\brequired\b', '必需'), (r'\bRequired\b', '必需'),
    (r'\boptional\b', '可选'), (r'\bOptional\b', '可选'),
    (r'\bvalid\b', '有效'), (r'\bValid\b', '有效'),
    (r'\binvalid\b', '无效'), (r'\bInvalid\b', '无效'),
    (r'\bexperimental\b', '实验性'), (r'\bExperimental\b', '实验性'),
    (r'\bdeprecated\b', '已弃用'), (r'\bDeprecated\b', '已弃用'),
    (r'\bobsolete\b', '已过时'), (r'\bObsolete\b', '已过时'),

    # ── Adverbs ──
    (r'\bautomatically\b', '自动'), (r'\bAutomatically\b', '自动'),
    (r'\btypically\b', '通常'), (r'\bTypically\b', '通常'),
    (r'\bcurrently\b', '目前'), (r'\bCurrently\b', '目前'),
    (r'\bnormally\b', '通常'), (r'\bNormally\b', '通常'),
    (r'\busually\b', '通常'), (r'\bUsually\b', '通常'),

    # ── Phrases ──
    (r'\band exit\b', '并退出'),
    (r'\bin most cases\b', '在大多数情况下'),
    (r'\bat runtime\b', '在运行时'),
    (r'\bon the command line\b', '在命令行上'),
    (r'\bcommand line\b', '命令行'),
    (r'\bcommand\\-line\b', '命令行'),
    (r'\bvirtual machine\b', '虚拟机'),
    (r'\bvirtual machines\b', '虚拟机'),
    (r'\bdisk image\b', '磁盘映像'),
    (r'\bdisk images\b', '磁盘映像'),
    (r'\bhard disk\b', '硬盘'),
    (r'\bread\\-only\b', '只读'),
    (r'\bread\\-write\b', '读写'),
    (r'\bper second\b', '每秒'),
    (r'\bin seconds\b', '以秒为单位'),
    (r'\bin bytes\b', '以字节为单位'),

    # ── Default patterns ──
    (r'The default is (on|off|none|auto)', r'默认值为 \1'),
    (r'the default is (on|off|none|auto)', r'默认值为 \1'),
    (r'is the default', '是默认值'),
    (r'Default is ([^.]+)', r'默认值为 \1'),
    (r'by default\b', '默认情况下'),
    (r'By default\b', '默认情况下'),
    (r'\(enabled by default\)', '（默认启用）'),
    (r'\(disabled by default\)', '（默认禁用）'),

    # ── Enables/Disables ──
    (r'Enables or disables (.+?) support', r'启用或禁用 \1 支持'),
    (r'Enables or disables (.+)', r'启用或禁用 \1'),

    # ── Enumeration ──
    (r'For example:', '例如：'),
    (r'For instance,', '例如，'),
    (r'for example,', '例如，'),
    (r'Alternatively:', '或者：'),
    (r'Note that, by default,', '请注意，默认情况下'),
    (r'Note that,', '请注意，'),
    (r'Note that', '请注意'),
    (r'Warning:', '警告：'),
    (r'Important:', '重要：'),
    (r'See also', '另请参阅'),
    (r"Described in the CXL 2\\.0 ECN: CEDT CFMWS & QTG _DSM", '在 CXL 2.0 ECN: CEDT CFMWS & QTG _DSM 中描述'),
]

def tr_text(text):
    """Apply all regex replacements in order."""
    result = text
    for pat, rep in RX:
        result = re.sub(pat, rep, result)
    return result

def process_file(basename):
    src_path = os.path.join(SRC, basename + '.1.gz')
    with gzip.open(src_path, 'rt', errors='replace') as f:
        content = f.read()
    
    lines = content.split('\n')
    result = []
    
    for line in lines:
        if line.startswith('.SH '):
            m = re.match(r'^([.]SH\s+)"?([^"]*)"?', line)
            if m:
                sec = m.group(2).strip()
                if sec in SH_MAP:
                    chn = SH_MAP[sec]
                    result.append(f'{m.group(1)}"{chn}"' if '"' in line else f'{m.group(1)}{chn}')
                    continue
            result.append(line)
        elif line.startswith('.SS '):
            m = re.match(r'^([.]SS\s+)"?([^"]*)"?', line)
            if m:
                sec = m.group(2).strip()
                if sec in SS_MAP:
                    chn = SS_MAP[sec]
                    result.append(f'{m.group(1)}"{chn}"' if '"' in line else f'{m.group(1)}{chn}')
                    continue
            result.append(line)
        elif line.startswith('.TH '):
            result.append(line.replace('"User Manual"', '"用户手册"').replace('"User Commands"', '"用户命令"').replace('"General Commands Manual"', '"通用命令手册"'))
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
    
    subprocess.run(['bash', '-c', f'gzip -c {dst_path} | sudo tee {INST}/{basename}.1.gz > /dev/null'], capture_output=True)
    os.unlink(dst_path)
    os.unlink(gz_path)
    return basename

def run():
    unique_files = ["qemu", "qemu-img", "qemu-storage-daemon"]
    system_targets = [
        "qemu-system-aarch64","qemu-system-alpha","qemu-system-arm","qemu-system-avr",
        "qemu-system-hppa","qemu-system-i386","qemu-system-loongarch64","qemu-system-m68k",
        "qemu-system-microblaze","qemu-system-mips","qemu-system-mips64","qemu-system-mips64el",
        "qemu-system-mipsel","qemu-system-or1k","qemu-system-ppc","qemu-system-ppc64",
        "qemu-system-riscv32","qemu-system-riscv64","qemu-system-rx","qemu-system-s390x",
        "qemu-system-sh4","qemu-system-sh4eb","qemu-system-sparc","qemu-system-sparc64",
        "qemu-system-tricore","qemu-system-x86_64","qemu-system-xtensa","qemu-system-xtensaeb",
    ]
    
    os.makedirs(DST, exist_ok=True)
    count = 0
    for f in unique_files:
        process_file(f)
        count += 1
        print(f"  translated: {f}.1")
    
    qemu_trans_path = f"{INST}/qemu.1.gz"
    if os.path.exists(qemu_trans_path):
        with gzip.open(qemu_trans_path, 'rt', errors='replace') as f:
            qemu_content = f.read()
        for target in system_targets:
            tc = qemu_content.replace('.TH "QEMU"', f'.TH "{target.upper()}"')
            dst_path = os.path.join(DST, f"{target}.1")
            with open(dst_path, 'w') as f:
                f.write(tc)
            gz_path = dst_path + '.gz'
            with open(dst_path, 'rb') as fin, gzip.open(gz_path, 'wb') as fout:
                fout.write(fin.read())
            subprocess.run(['bash', '-c', f'gzip -c {dst_path} | sudo tee {INST}/{target}.1.gz > /dev/null'], capture_output=True)
            os.unlink(dst_path)
            os.unlink(gz_path)
            count += 1
            print(f"  installed: {target}.1")
    print(f"qemu done: {count} translations")

if __name__ == '__main__':
    run()
