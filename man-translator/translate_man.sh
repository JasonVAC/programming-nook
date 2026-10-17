#!/bin/bash
# Auto-translate man page section headers from EN to zh_CN
INPUT="$1"
OUTPUT="$2"
sed \
  -e 's/^\.SH NAME$/.SH 名称/' \
  -e 's/^\.SH SYNOPSIS$/.SH 概述/' \
  -e 's/^\.SH DESCRIPTION$/.SH 描述/' \
  -e 's/^\.SH OPTIONS$/.SH 选项/' \
  -e 's/^\.SH EXAMPLES$/.SH 示例/' \
  -e 's/^\.SH "EXAMPLES"$/.SH "示例"/' \
  -e 's/^\.SH "EXAMPLE"$/.SH "示例"/' \
  -e 's/^\.SH "EXIT STATUS"$/.SH "退出状态"/' \
  -e 's/^\.SH "EXIT CODES"$/.SH "退出状态"/' \
  -e 's/^\.SH "EXIT CODE"$/.SH "退出状态"/' \
  -e 's/^\.SH EXIT STATUS$/.SH 退出状态/' \
  -e 's/^\.SH "RETURN VALUE"$/.SH "返回值"/' \
  -e 's/^\.SH RETURN VALUE$/.SH 返回值/' \
  -e 's/^\.SH "SEE ALSO"$/.SH "参见"/' \
  -e 's/^\.SH SEE ALSO$/.SH 参见/' \
  -e 's/^\.SH "FILES"$/.SH "文件"/' \
  -e 's/^\.SH FILES$/.SH 文件/' \
  -e 's/^\.SH "ENVIRONMENT"$/.SH "环境变量"/' \
  -e 's/^\.SH ENVIRONMENT$/.SH 环境变量/' \
  -e 's/^\.SH "BUGS"$/.SH "错误"/' \
  -e 's/^\.SH BUGS$/.SH 错误/' \
  -e 's/^\.SH "AUTHOR"$/.SH "作者"/' \
  -e 's/^\.SH AUTHOR$/.SH 作者/' \
  -e 's/^\.SH "AUTHORS"$/.SH "作者"/' \
  -e 's/^\.SH AUTHORS$/.SH 作者/' \
  -e 's/^\.SH "COPYRIGHT"$/.SH "版权"/' \
  -e 's/^\.SH COPYRIGHT$/.SH 版权/' \
  -e 's/^\.SH "NOTES"$/.SH "注释"/' \
  -e 's/^\.SH NOTES$/.SH 注释/' \
  -e 's/^\.SH "REPORTING BUGS"$/.SH "报告错误"/' \
  -e 's/^\.SH REPORTING BUGS$/.SH 报告错误/' \
  -e 's/^\.SH "DIAGNOSTICS"$/.SH "诊断"/' \
  -e 's/^\.SH DIAGNOSTICS$/.SH 诊断/' \
  -e 's/^\.SH "HISTORY"$/.SH "历史"/' \
  -e 's/^\.SH HISTORY$/.SH 历史/' \
  -e 's/^\.SH "CONFIGURATION"$/.SH "配置"/' \
  -e 's/^\.SH USAGE$/.SH 用法/' \
  -e 's/^\.SH "DEPENDENCIES"$/.SH "依赖"/' \
  -e 's/^\.SH OVERVIEW$/.SH 概述/' \
  -e 's/^\.SH "GENERAL OPTIONS"$/.SH "通用选项"/' \
  -e 's/^\.SH SETUP$/.SH 设置/' \
  -e 's/^\.SH "ALTERNATIVE MODES"$/.SH "替代模式"/' \
  -e 's/User Commands/用户命令/g' \
  -e 's/^\.SH CAVEATS$/.SH 注意事项/' \
  -e 's/^\.SH "TROUBLESHOOTING"$/.SH "故障排除"/' \
  -e 's/^\.SH "SECURITY"$/.SH "安全"/' \
  -e 's/^\.SH "STANDARDS"$/.SH "标准"/' \
  -e 's/^\.SH "SYSTEM ADMINISTRATION"$/.SH "系统管理"/' \
  "$INPUT" > "$OUTPUT"
