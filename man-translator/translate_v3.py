#!/usr/bin/env python3
import urllib.request, urllib.parse, json, gzip, os, re, sys, time, subprocess, glob

API = "https://api.mymemory.translated.net/get"
SRC = "/usr/share/man/man1/"
DEST = "/tmp/man1_zh/"
INST = "/usr/share/man/zh_CN/man1/"
BATCH = "/tmp/batch_a_e.txt"
DELIM = "\x01SPLIT\x02"

SH_MAP = {
    "NAME": "名称", "SYNOPSIS": "概述", "DESCRIPTION": "描述",
    "OPTIONS": "选项", "EXAMPLES": "示例", "EXAMPLE": "示例",
    "AUTHOR": "作者", "SEE ALSO": "另请参见", "FILES": "文件",
    "EXIT STATUS": "退出状态", "ENVIRONMENT": "环境变量",
    "BUGS": "错误", "NOTES": "注意事项", "DIAGNOSTICS": "诊断",
    "COPYRIGHT": "版权", "REPORTING BUGS": "报告错误",
    "AVAILABILITY": "可用性", "HISTORY": "历史",
    "CONFIGURATION": "配置", "RETURN VALUE": "返回值",
    "ERRORS": "错误", "STANDARDS": "标准",
    "SECURITY": "安全", "LICENSE": "许可证",
    "COMMANDS": "命令", "USAGE": "用法", "OVERVIEW": "概述",
    "INPUT": "输入", "OUTPUT": "输出", "WARNING": "警告",
    "CAVEATS": "注意事项", "LIMITATIONS": "限制",
    "REQUIREMENTS": "要求", "INSTALLATION": "安装",
}

PURE_ROFF = set('.ad .nh .hy .TP .PP .IP .LP .HP .RS .RE .PD .sp .br .fi .nf .na .bp .pm'.split())
PURE_ROFF.update('.lf .in .ti .ps .vs .ft .cs .po .ll .lt .ne .ie .el .if .de .ds'.split())
PURE_ROFF.update('.nr .rm .rn .so .mso .tr .hc .hw .ID .ce .rj .ul .cu .mc'.split())
PURE_ROFF.update('.ns .rs .rt .pc .pn .pl .wh .ch .dt .it .em .am .as .ee'.split())
PURE_ROFF.update('.ec .eo .cc .c2 .do .nx .ex .sy .ab .os .sv .tm .ig .pi'.split())
PURE_ROFF.update('.cf .fc .ds1 .cp .cs .ss .ta .tc .ti .tk .vs .warn'.split())
PURE_ROFF.update('.B .BI .BR .I .IB .IR .RB .RI .SB .SM .XR .MT .UR .UE'.split())
PURE_ROFF.update(".\\\" .\\# .\\} .\\{ '.\\\" 'ig".split())

def translate(text):
    if not text or len(text.strip()) < 2:
        return text
    text = text[:480]
    encoded = urllib.parse.quote(text)
    url = f"{API}?q={encoded}&langpair=en|zh-CN"
    for _ in range(2):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as r:
                d = json.loads(r.read().decode('utf-8'))
                t = d.get('responseData', {}).get('translatedText', text)
                return t if t and t != text else text
        except:
            time.sleep(0.3)
    return text

def find_source(name):
    """Find source man page file"""
    # Try exact path
    src = os.path.join(SRC, name + ".gz")
    if os.path.exists(src):
        return src
    # Try with different extension
    for ext in ['.1.gz', '.1m.gz', '.1ssl.gz']:
        src = os.path.join(SRC, name + ext)
        if os.path.exists(src):
            return src
    # Glob
    for g in glob.glob(os.path.join(SRC, name + '*')):
        return g
    return None

def process(lines):
    out = []
    blocks = []  # (index, text)
    
    for line in lines:
        line = line.rstrip('\n\r')
        
        if not line.strip():
            blocks.append((len(out), ''))
            out.append('')
            continue
        
        # Comments
        if line.lstrip().startswith('.\\"') or line.lstrip().startswith("'\\\""):
            out.append(line)
            continue
        
        # .TH
        m = re.match(r'^(\.TH\s+)(.*)', line)
        if m:
            rest = m.group(2)
            rest = rest.replace("User Commands", "用户命令")
            rest = rest.replace("User commands", "用户命令")
            rest = rest.replace("Linux User's Manual", "Linux 用户手册")
            rest = rest.replace("Linux Programmer's Manual", "Linux 程序员手册")
            out.append(".TH " + rest)
            continue
        
        # .SH
        m = re.match(r'^\.SH\s+"?([^"]+)"?', line)
        if m:
            h = m.group(1).strip()
            if h.upper() in SH_MAP:
                out.append(f'.SH "{SH_MAP[h.upper()]}"')
            else:
                out.append(f'.SH "{translate(h)}"')
            continue
        
        # .SS
        m = re.match(r'^\.SS\s+"?([^"]+)"?', line)
        if m:
            out.append(f'.SS "{translate(m.group(1).strip())}"')
            continue
        
        # Pure roff commands
        cmd = line.split()[0] if line.split() else ''
        if cmd in PURE_ROFF or (line.startswith('.') and len(line.split()) == 1):
            out.append(line)
            continue
        
        # Other roff lines (.B, .I, .BR etc with content) - keep as-is
        if line.startswith('.'):
            out.append(line)
            continue
        
        # Text line
        out.append(line)
        blocks.append((len(out)-1, line))
    
    if not blocks:
        return out
    
    # Combine text blocks
    texts = [b[1] for b in blocks]
    
    # Translate in chunks
    chunks = []
    cur = ""
    for t in texts:
        if len(cur) + len(t) + len(DELIM) > 460:
            if cur:
                chunks.append(cur)
            cur = t
        else:
            cur = (cur + DELIM + t) if cur else t
    if cur:
        chunks.append(cur)
    
    translated = []
    for ch in chunks:
        result = translate(ch)
        translated.append(result)
    
    translated_text = DELIM.join(translated)
    parts = translated_text.split(DELIM)
    
    for i in range(min(len(blocks), len(parts))):
        idx = blocks[i][0]
        out[idx] = parts[i] if parts[i].strip() else blocks[i][1]
    
    return out

def install_page(name):
    src_file = os.path.join(DEST, name)
    tmp_gz = os.path.join(DEST, name + ".gz")
    dst_gz = os.path.join(INST, name + ".gz")
    
    try:
        with open(src_file, 'rb') as f:
            with gzip.open(tmp_gz, 'wb') as g:
                g.write(f.read())
    except:
        return False
    
    try:
        subprocess.run(['sudo', 'cp', tmp_gz, dst_gz], check=True, capture_output=True)
        os.remove(tmp_gz)
        return True
    except:
        # Try without sudo
        try:
            with open(tmp_gz, 'rb') as f:
                with open(dst_gz, 'wb') as g:
                    g.write(f.read())
            os.remove(tmp_gz)
            return True
        except:
            return False

def main():
    os.makedirs(DEST, exist_ok=True)
    
    with open(BATCH, 'r') as f:
        pages = [l.strip() for l in f if l.strip()]
    
    total = len(pages)
    ok = 0
    bad = []
    t0 = time.time()
    
    sys.stdout.reconfigure(line_buffering=True)
    
    print(f"Processing {total} man pages...")
    
    for i, page in enumerate(pages):
        name = page
        src = find_source(name)
        
        if not src:
            print(f"[{i+1}/{total}] {name} NOT FOUND", flush=True)
            bad.append(name)
            continue
        
        try:
            with gzip.open(src, 'rt', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"[{i+1}/{total}] {name} READ ERR: {e}", flush=True)
            bad.append(name)
            continue
        
        try:
            result = process(lines)
            dest_file = os.path.join(DEST, name)
            with open(dest_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(result) + '\n')
        except Exception as e:
            print(f"[{i+1}/{total}] {name} WRITE ERR: {e}", flush=True)
            bad.append(name)
            continue
        
        if install_page(name):
            ok += 1
            elapsed = time.time() - t0
            rate = (i+1) / elapsed if elapsed > 0 else 0.001
            eta = (total - i - 1) / rate if rate > 0 else 0
            print(f"[{i+1}/{total}] {name} OK  ({int(elapsed)}s elapsed, ~{int(eta)}s remaining)", flush=True)
        else:
            bad.append(name)
            print(f"[{i+1}/{total}] {name} INSTALL FAILED", flush=True)
        
        time.sleep(0.1)
    
    elapsed = int(time.time() - t0)
    print(f"\nbatch a-e done: {ok} translations  ({elapsed}s)", flush=True)
    if bad:
        print(f"Failed ({len(bad)}): {', '.join(bad[:10])}")

main()
