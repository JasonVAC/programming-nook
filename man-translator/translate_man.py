#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json
import gzip
import os
import re
import sys
import time

API_URL = "https://api.mymemory.translated.net/get"
SRC_DIR = "/usr/share/man/man1/"
DEST_DIR = "/tmp/man1_zh/"
INSTALL_DIR = "/usr/share/man/zh_CN/man1/"
BATCH_FILE = "/tmp/batch_a_e.txt"

SH_TRANSLATIONS = {
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
    "RESOURCES": "资源", "USAGE": "用法",
    "COMMANDS": "命令", "FORMATS": "格式",
    "OVERVIEW": "概述", "DEFAULTS": "默认值",
    "LIMITATIONS": "限制", "TROUBLESHOOTING": "故障排除",
    "WARNING": "警告", "CAVEATS": "注意事项",
    "TIPS": "提示", "SETUP": "设置",
    "DEVICE SUPPORT": "设备支持", "SUPPORTED DEVICES": "支持的设备",
    "FEATURES": "特性", "REQUIREMENTS": "要求",
    "INSTALLATION": "安装", "DEPENDENCIES": "依赖",
    "COMPATIBILITY": "兼容性", "CHANGES": "变更",
    "PORTABILITY": "可移植性", "CONFORMING TO": "符合标准",
    "IMPLEMENTATION NOTES": "实现说明", "RESTRICTIONS": "限制",
    "PERFORMANCE": "性能", "MEMORY USAGE": "内存使用",
    "OUTPUT": "输出", "INPUT": "输入",
    "ARGUMENTS": "参数", "SUBCOMMANDS": "子命令",
    "OPERANDS": "操作数", "STDIN": "标准输入",
    "STDOUT": "标准输出", "STDERR": "标准错误",
    "SIGNALS": "信号", "PROTOCOL": "协议",
    "ALGORITHM": "算法",
}

def translate_block(text):
    """Translate a block of text"""
    if not text or not text.strip():
        return text
    stripped = text.strip()
    if len(stripped) <= 2:
        return text
    if re.match(r'^[\d\s\.\,\;\:\-\(\)\[\]\{\}]+$', stripped):
        return text
    
    # Limit to ~400 chars for API
    chunk = text[:450]
    encoded = urllib.parse.quote(chunk)
    url = f"{API_URL}?q={encoded}&langpair=en|zh-CN"
    
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                translated = data.get('responseData', {}).get('translatedText', text)
                if translated and translated != text:
                    return translated
        except:
            if attempt < 1:
                time.sleep(0.5)
    return text

def translate_line_safe(line):
    """Translate line, preserving all roff formatting codes"""
    if not line or not line.strip():
        return line
    
    # Comments
    if re.match(r'^\.\\"', line):
        return line
    
    # .TH header
    th_match = re.match(r'^\.TH\s+(.*)', line)
    if th_match:
        rest = th_match.group(1)
        rest = rest.replace("User Commands", "用户命令")
        rest = rest.replace("User commands", "用户命令")
        rest = rest.replace("Linux User's Manual", "Linux 用户手册")
        rest = rest.replace("Linux Programmer's Manual", "Linux 程序员手册")
        return ".TH " + rest
    
    # .SH section headers
    sh_match = re.match(r'^\.SH\s+(.+)', line)
    if sh_match:
        raw = sh_match.group(1).strip()
        header = raw.strip('"').strip()
        if header.upper() in SH_TRANSLATIONS:
            return f'.SH "{SH_TRANSLATIONS[header.upper()]}"'
        if re.match(r'^"[^"]+"$', raw):
            return f'.SH "{translate_block(header)}"'
        # Try to translate unquoted
        return f'.SH "{translate_block(header)}"'
    
    # .SS subsection headers
    ss_match = re.match(r'^\.SS\s+(.+)', line)
    if ss_match:
        raw = ss_match.group(1).strip()
        header = raw.strip('"').strip()
        return f'.SS "{translate_block(header)}"'
    
    # Pure roff commands - pass through unchanged
    if line.startswith('.'):
        cmd = line.split()[0] if line.split() else ''
        simple_pass = ('.ad', '.nh', '.hy', '.TP', '.PP', '.IP', '.LP', '.HP',
                       '.RS', '.RE', '.PD', '.sp', '.br', '.fi', '.nf', '.na',
                       '.in', '.ti', '.ps', '.vs', '.ft', '.cs', '.po', '.ll',
                       '.lt', '.ne', '.ie', '.el', '.if', '.de', '.ds', '.nr',
                       '.rm', '.rn', '.so', '.mso', '.tr', '.hc', '.hw', '.ID',
                       '.ce', '.rj', '.ul', '.cu', '.mc', '.bp', '.pm', '.lf',
                       '.tm', '.ig', '.ec', '.eo', '.cc', '.c2', '.do', '.nx',
                       '.ex', '.sy', '.pi', '.cf', '.fc', '.ab', '.os', '.sv',
                       '.ns', '.rs', '.rt', '.pc', '.pn', '.pl', '.wh', '.ch',
                       '.dt', '.it', '.em', '.am', '.as', '.ds1',
                       '.B', '.BI', '.BR', '.I', '.IB', '.IR', '.RB', '.RI',
                       '.SB', '.SM', '.XR', '.MT', '.UR', '.UE',
                       '.r', '.R', '.s', '.S', '.t', '.T', '.v', '.V',
                       '.b', '.i', '.rb', '.bi', '.ib', '.ri', '.ir',
                       '\'lb', '\'lt', '\'nm', '\'nn')
        for sp in simple_pass:
            if cmd.startswith(sp):
                return line
        return line
    
    # Normal text lines - translate
    return translate_block(line)

def process_page(filename, lines):
    """Process all lines of a man page"""
    out = []
    for line in lines:
        line = line.rstrip('\n\r')
        try:
            out.append(translate_line_safe(line))
        except:
            out.append(line)
    return out

def install_page(name, dest_file):
    """Gzip and install man page"""
    gz_dest = dest_file + ".gz"
    install_path = os.path.join(INSTALL_DIR, name + ".gz")
    try:
        # Read source, gzip
        with open(dest_file, 'rb') as f_in:
            with gzip.open(gz_dest, 'wb') as f_out:
                f_out.write(f_in.read())
        # Install
        data = open(gz_dest, 'rb').read()
        with open(install_path, 'wb') as f:
            f.write(data)
        os.remove(gz_dest)
        return True
    except Exception as e:
        print(f"  INSTALL ERROR: {e}")
        return False

def main():
    os.makedirs(DEST_DIR, exist_ok=True)
    
    with open(BATCH_FILE, 'r') as f:
        pages = [l.strip() for l in f if l.strip()]
    
    total = len(pages)
    success = 0
    failed = []
    
    print(f"Starting batch translation of {total} pages...")
    
    for i, page in enumerate(pages):
        name = page
        if name.endswith('.1'):
            basename = name[:-2]
        else:
            basename = name
        
        src = os.path.join(SRC_DIR, name + ".gz")
        dest = os.path.join(DEST_DIR, name)
        
        if not os.path.exists(src):
            print(f"[{i+1}/{total}] {name} - SOURCE MISSING")
            failed.append(name)
            continue
        
        try:
            with gzip.open(src, 'rt', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"[{i+1}/{total}] {name} - READ ERROR: {e}")
            failed.append(name)
            continue
        
        try:
            translated = process_page(name, lines)
            with open(dest, 'w', encoding='utf-8') as f:
                f.write('\n'.join(translated) + '\n')
        except Exception as e:
            print(f"[{i+1}/{total}] {name} - WRITE ERROR: {e}")
            failed.append(name)
            continue
        
        if install_page(name, dest):
            success += 1
            print(f"[{i+1}/{total}] {name} OK")
        else:
            failed.append(name)
            print(f"[{i+1}/{total}] {name} INSTALL FAILED")
        
        if i % 5 == 4:
            time.sleep(0.3)
    
    print(f"\nbatch a-e done: {success} translations")
    if failed:
        print(f"Failed: {len(failed)} - {', '.join(failed[:10])}{'...' if len(failed)>10 else ''}")

if __name__ == "__main__":
    main()
