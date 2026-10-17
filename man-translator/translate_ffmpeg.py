import sys, re

# Read the English ffmpeg man page
import subprocess
src = subprocess.check_output(['zcat', '/usr/share/man/man1/ffmpeg.1.gz']).decode('utf-8')

# Translation dictionary for section headers
sect_trans = {
    '.SH NAME': '.SH 名称',
    '.SH SYNOPSIS': '.SH 语法',
    '.SH DESCRIPTION': '.SH 描述',
    '.SH OPTIONS': '.SH 选项',
    '.SH "SEE ALSO"': '.SH "参见"',
    '.SH AUTHORS': '.SH 作者',
    '.SH EXAMPLES': '.SH 示例',
    '.SH TIMECODE': '.SH 时间码',
}

# Translation dictionary for subsection headers
ss_trans = {
    '.SS "Stream specifiers"': '.SS "流说明符"',
    '.SS "Generic options"': '.SS "通用选项"',
    '.SS "Main options"': '.SS "主要选项"',
    '.SS "Advanced options"': '.SS "高级选项"',
    '.SS "Audio Options"': '.SS "音频选项"',
    '.SS "Advanced Audio options"': '.SS "高级音频选项"',
    '.SS "Subtitle options"': '.SS "字幕选项"',
    '.SS "Advanced Subtitle options"': '.SS "高级字幕选项"',
    '.SS "Video Options"': '.SS "视频选项"',
    '.SS "Advanced Video options"': '.SS "高级视频选项"',
    '.SS "Preset files"': '.SS "预设文件"',
    '.SS "vstats file format"': '.SS "vstats 文件格式"',
    '.SS "Video and Audio grabbing"': '.SS "视频和音频抓取"',
    '.SS "X11 grabbing"': '.SS "X11 抓取"',
    '.SS "Video and Audio file format conversion"': '.SS "视频和音频文件格式转换"',
    '.SS "Tips"': '.SS "提示"',
    '.SS "While playing"': '.SS "播放时"',
    '.SS "Advanced options"': '.SS "高级选项"',
    '.SS "Stream selection"': '.SS "流选择"',
    '.SS "Stream handling"': '.SS "流处理"',
    '.SS "Examples"': '.SS "示例"',
    '.SS "Example: automatic stream selection"': '.SS "示例：自动流选择"',
    '.SS "Example: automatic subtitles selection"': '.SS "示例：自动字幕选择"',
    '.SS "Example: unlabeled filtergraph outputs"': '.SS "示例：未标记的滤镜图输出"',
    '.SS "Example: labeled filtergraph outputs"': '.SS "示例：已标记的滤镜图输出"',
}

lines = src.split('\n')

# Process line by line to find text that needs translation
in_prose = False
output_lines = []

for line in lines:
    ol = line
    # Translate section headers
    if line.startswith('.SH '):
        for k, v in sect_trans.items():
            if line.startswith(k):
                ol = v + line[len(k):]
                break
    # Translate subsection headers
    if line.startswith('.SS '):
        for k, v in ss_trans.items():
            if line.startswith(k):
                ol = v + line[len(k):]
                break
    
    output_lines.append(ol)

# Print result
sys.stdout.write('\n'.join(output_lines))
