#!/usr/bin/env python3
"""Quick man page translator - translate all text in a page as one block, then reassemble."""
import urllib.request, urllib.parse, json, gzip, os, re, sys, time

API = "https://api.mymemory.translated.net/get"
SRC = "/usr/share/man/man1/"
DEST = "/tmp/man1_zh/"
INST = "/usr/share/man/zh_CN/man1/"
BATCH = "/tmp/batch_a_e.txt"
DELIM = "@@SPLIT@@"

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
}

def translate_chunk(text):
    """Translate text via API"""
    if not text or len(text.strip()) < 3:
        return text
    encoded = urllib.parse.quote(text[:480])
    url = f"{API}?q={encoded}&langpair=en|zh-CN"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            d = json.loads(r.read().decode('utf-8'))
            t = d.get('responseData', {}).get('translatedText', text)
            return t if t else text
    except:
        return text

def is_roff_cmd(line):
    """Check if line is purely a roff command (no text to translate)"""
    if not line.startswith('.'):
        return False
    cmd = line.split()[0] if line.split() else line
    pure_cmds = {'.ad', '.nh', '.hy', '.TP', '.PP', '.IP', '.LP', '.HP', '.RS', '.RE',
                 '.PD', '.sp', '.br', '.fi', '.nf', '.na', '.bp', '.pm', '.lf',
                 '.in', '.ti', '.ps', '.vs', '.ft', '.cs', '.po', '.ll', '.lt',
                 '.ne', '.ie', '.el', '.if', '.de', '.ds', '.nr', '.rm', '.rn',
                 '.so', '.mso', '.tr', '.hc', '.hw', '.ID', '.ce', '.rj', '.ul',
                 '.cu', '.mc', '.ns', '.rs', '.rt', '.pc', '.pn', '.pl', '.wh',
                 '.ch', '.dt', '.it', '.em', '.am', '.as', '.ee', '.ec', '.eo',
                 '.cc', '.c2', '.do', '.nx', '.ex', '.sy', '.ab', '.os', '.sv',
                 '.tm', '.ig', '.pi', '.cf', '.fc', '.lb', '.nm', '.nn', '.ds1'}
    return cmd in pure_cmds or (cmd.startswith('\\"') or cmd.startswith('\''))

def process_page(lines):
    """Process a man page: extract text blocks, translate, reassemble"""
    # Pass 1: handle .TH, .SH, .SS headers and identify text blocks
    out = []
    text_blocks = []  # list of (index_in_out, text)
    
    for line in lines:
        line = line.rstrip('\n\r')
        
        # Comments
        if re.match(r'^\.\\"', line):
            out.append(line)
            continue
        
        # .TH header
        th = re.match(r'^\.TH\s+(.*)', line)
        if th:
            rest = th.group(1).replace("User Commands", "用户命令")
            rest = rest.replace("User commands", "用户命令")
            out.append(".TH " + rest)
            continue
        
        # .SH section headers
        sh = re.match(r'^\.SH\s+"?([^"]+)"?$', line)
        if sh:
            hdr = sh.group(1).strip()
            if hdr.upper() in SH_MAP:
                out.append(f'.SH "{SH_MAP[hdr.upper()]}"')
            else:
                tr = translate_chunk(hdr)
                out.append(f'.SH "{tr}"')
            continue
        
        # .SS subsection headers
        ss = re.match(r'^\.SS\s+(.+)', line)
        if ss:
            hdr = ss.group(1).strip().strip('"')
            tr = translate_chunk(hdr)
            out.append(f'.SS "{tr}"')
            continue
        
        # Pure roff commands
        if is_roff_cmd(line):
            out.append(line)
            continue
        
        # Lines with roff markers like .B, .I, .BR etc - keep as-is
        if line.startswith('.'):
            out.append(line)
            continue
        
        # Text line - add to blocks
        out.append(line)
        text_blocks.append((len(out) - 1, line))
    
    # If no text to translate, return
    if not text_blocks:
        return out
    
    # Concatenate all text blocks with delimiter
    combined = DELIM.join(t[1] for t in text_blocks)
    
    # Translate in chunks if needed
    if len(combined) > 450:
        # Split into chunks
        chunks = []
        current = ""
        for block in text_blocks:
            txt = block[1]
            if len(current) + len(txt) + len(DELIM) > 450:
                if current:
                    chunks.append(current)
                current = txt
            else:
                current = (current + DELIM + txt) if current else txt
        if current:
            chunks.append(current)
        
        translated_chunks = [translate_chunk(c) for c in chunks]
        combined_translated = DELIM.join(translated_chunks)
    else:
        combined_translated = translate_chunk(combined)
    
    translated_parts = combined_translated.split(DELIM)
    
    # Reassemble
    reinsert_count = min(len(text_blocks), len(translated_parts))
    for i in range(reinsert_count):
        idx = text_blocks[i][0]
        out[idx] = translated_parts[i]
    
    return out

def install(name, dest_file):
    """Gzip and install"""
    gz = dest_file + ".gz"
    ipath = os.path.join(INST, name + ".gz")
    try:
        with open(dest_file, 'rb') as f:
            with gzip.open(gz, 'wb') as g:
                g.write(f.read())
        with open(gz, 'rb') as f:
            with open(ipath, 'wb') as g:
                g.write(f.read())
        os.remove(gz)
        return True
    except Exception as e:
        print(f"  INSTALL ERR: {e}")
        return False

def main():
    os.makedirs(DEST, exist_ok=True)
    
    with open(BATCH, 'r') as f:
        pages = [l.strip() for l in f if l.strip()]
    
    total = len(pages)
    ok = 0
    bad = []
    
    print(f"Translating {total} man pages...")
    t0 = time.time()
    
    for i, page in enumerate(pages):
        name = page
        src = os.path.join(SRC, name + ".gz" if name.endswith('.1') else f"{name}.1.gz")
        
        # Try without .1 if needed
        if not os.path.exists(src):
            src = os.path.join(SRC, name + ".gz")
        if not os.path.exists(src):
            # Look for file matching
            import glob as gl
            candidates = gl.glob(os.path.join(SRC, name + "*"))
            src = candidates[0] if candidates else None
        
        if not src or not os.path.exists(src):
            print(f"[{i+1}/{total}] {name} - NOT FOUND")
            bad.append(name)
            continue
        
        dest = os.path.join(DEST, name)
        
        try:
            with gzip.open(src, 'rt', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
        except:
            print(f"[{i+1}/{total}] {name} - READ ERR")
            bad.append(name)
            continue
        
        try:
            result = process_page(lines)
            with open(dest, 'w', encoding='utf-8') as f:
                f.write('\n'.join(result) + '\n')
        except Exception as e:
            print(f"[{i+1}/{total}] {name} - WRITE ERR: {e}")
            bad.append(name)
            continue
        
        # Install
        if install(name, dest):
            ok += 1
            elapsed = time.time() - t0
            rate = (i+1) / elapsed if elapsed > 0 else 0
            eta = (total - i - 1) / rate if rate > 0 else 0
            print(f"[{i+1}/{total}] {name} OK ({elapsed:.0f}s, ETA {eta:.0f}s)")
        else:
            bad.append(name)
            print(f"[{i+1}/{total}] {name} INSTALL FAILED")
        
        # Delay to avoid rate limiting
        time.sleep(0.15)
    
    print(f"\nbatch a-e done: {ok} translations")
    if bad:
        print(f"Failed ({len(bad)}): {', '.join(bad[:15])}...")

if __name__ == "__main__":
    main()
