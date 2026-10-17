#!/usr/bin/env python3
"""
Translate git man pages from English to Chinese, preserving roff formatting.
Protects option names and roff codes before translating.
"""
import re, sys, os

# ── Section headers (exact match) ──
EXACT_MAP = {
    '.SH "NAME"': '.SH "名称"',
    '.SH "SYNOPSIS"': '.SH "概述"',
    '.SH "DESCRIPTION"': '.SH "描述"',
    '.SH "OPTIONS"': '.SH "选项"',
    '.SH "COMMANDS"': '.SH "命令"',
    '.SH "EXAMPLES"': '.SH "示例"',
    '.SH "AUTHOR"': '.SH "作者"',
    '.SH "SEE ALSO"': '.SH "另请参见"',
    '.SH "REPORTING BUGS"': '.SH "报告错误"',
    '.SH "COPYRIGHT"': '.SH "版权"',
    '.SH "GIT"': '.SH "GIT"',
    '.SH "GIT COMMANDS"': '.SH "GIT 命令"',
    '.SH "HIGH-LEVEL COMMANDS (PORCELAIN)"': '.SH "高级命令 (PORCELAIN)"',
    '.SH "LOW-LEVEL COMMANDS (PLUMBING)"': '.SH "低级命令 (PLUMBING)"',
    '.SH "DEPRECATED MODES"': '.SH "已弃用的模式"',
    '.SH "FILES"': '.SH "文件"',
    '.SH "ENVIRONMENT"': '.SH "环境变量"',
    '.SH "ENVIRONMENT VARIABLES"': '.SH "环境变量"',
    '.SH "CONFIGURATION MECHANISM"': '.SH "配置机制"',
    '.SH "CONFIGURATION FILE"': '.SH "配置文件"',
    '.SH "VARIABLES"': '.SH "变量"',
    '.SH "BUGS"': '.SH "错误"',
    '.SH "NOTES"': '.SH "注释"',
    '.SH "DIAGNOSTICS"': '.SH "诊断"',
    '.SH "DISCUSSION"': '.SH "讨论"',
    '.SH "OVERVIEW"': '.SH "概述"',
    '.SH "RETURN VALUES"': '.SH "返回值"',
    '.SH "EXIT STATUS"': '.SH "退出状态"',
    '.SH "PRETTY FORMATS"': '.SH "美化格式"',
    '.SH "CONFIGURATION"': '.SH "配置"',
    '.SH "INCLUDES"': '.SH "包含"',
    '.SH "CONDITIONAL INCLUDES"': '.SH "条件包含"',
    '.SH "VALUES"': '.SH "值"',
    '.SH "SCOPES"': '.SH "作用域"',
    '.SH "SYNTAX"': '.SH "语法"',
}

# ── SS section match patterns (prefix match) ──
SS_MAP = [
    (r'.SS "Main porcelain commands"', '.SS "主要 porcelain 命令"'),
    (r'.SS "Ancillary Commands"', '.SS "辅助命令"'),
    (r'.SS "Interrogators"', '.SS "查询工具"'),
    (r'.SS "Interacting with Others"', '.SS "与外部交互"'),
    (r'.SS "Low-level commands \(plumbing\)"', '.SS "低级命令 (plumbing)"'),
    (r'.SS "Manipulators"', '.SS "操作工具"'),
    (r'.SS "Commit Limiting"', '.SS "提交限制"'),
    (r'.SS "Commit Ordering"', '.SS "提交排序"'),
    (r'.SS "Commit Formatting"', '.SS "提交格式化"'),
    (r'.SS "History Simplification"', '.SS "历史简化"'),
    (r'.SS "Diff Formatting"', '.SS "差异格式化"'),
    (r'.SS "Common diff options"', '.SS "通用差异选项"'),
    (r'.SS "PRETTY FORMATS"', '.SS "美化格式"'),
    (r'.SS "Forbidden formatting"', '.SS "禁止的格式"'),
    (r'.SS "GENERATING PATCH TEXT WITH -P"', '.SS "使用 -P 生成补丁文本"'),
    (r'.SS "GENERATING PATCH TEXT WITH -p"', '.SS "使用 -p 生成补丁文本"'),
    (r'.SS "COMBINED DIFF FORMAT"', '.SS "合并差异格式"'),
    (r'.SS "Raw output format"', '.SS "原始输出格式"'),
    (r'.SS "diff format for merges"', '.SS "合并的差异格式"'),
    (r'.SS "Examples"', '.SS "示例"'),
    (r'.SS "Boolean"', '.SS "布尔值"'),
    (r'.SS "Variables"', '.SS "变量"'),
    (r'.SS "Values"', '.SS "值"'),
    (r'.SS "Pathnames"', '.SS "路径名"'),
    (r'.SS "Other"', '.SS "其他"'),
    (r'.SS "Includes"', '.SS "包含"'),
    (r'.SS "Conditional includes"', '.SS "条件包含"'),
    (r'.SS "SCOPES"', '.SS "作用域"'),
    (r'.SS "SYNTAX"', '.SS "语法"'),
    (r'.SS "INCLUDES"', '.SS "包含"'),
    (r'.SS "CONDITIONAL INCLUDES"', '.SS "条件包含"'),
    (r'.SS "VALUES"', '.SS "值"'),
    (r'.SS "ENVIRONMENT"', '.SS "环境变量"'),
    (r'.SS "BUGS"', '.SS "错误"'),
    (r'.SS "GIT"', '.SS "GIT"'),
    (r'.SS "SEE ALSO"', '.SS "另请参见"'),
    (r'.SS "NOTES"', '.SS "注释"'),
]

# ── Translation rules: (pattern, replacement) ──
# These are applied to the FULL LINE, including roff codes.
# The patterns use regex with escaped roff special chars.
RULES = [
    # ─── Long specific descriptions (applied first) ───
    (r'git \- the stupid content tracker', 'git \- 愚蠢的内容跟踪器'),

    (r'Show changes between the working tree and the index or a tree, changes between the index and a tree, changes between two trees, changes resulting from a merge, changes between two blob objects, or changes between two files on disk', '显示工作树与暂存区或树之间的更改、暂存区与树之间的更改、两棵树之间的更改、合并产生的更改、两个 blob 对象之间的更改，或者磁盘上两个文件之间的更改'),

    (r'Shows the commit logs', '显示提交日志'),
    (r'Show commit logs\b', '显示提交日志'),

    # ─── Git command description translations ───
    (r'Add file contents to the index', '将文件内容添加到暂存区'),
    (r'Apply a series of patches from a mailbox', '从邮箱应用一系列补丁'),
    (r'Create an archive of files from a named tree', '从命名的树创建文件归档'),
    (r'Download missing objects in a partial clone', '在部分克隆中下载缺失的对象'),
    (r'Use binary search to find the commit that introduced a bug', '使用二分查找定位引入错误的提交'),
    (r'List, create, or delete branches', '列出、创建或删除分支'),
    (r'Move objects and refs by archive', '通过归档传输对象和引用'),
    (r'Switch branches or restore working tree files', '切换分支或恢复工作树文件'),
    (r'Apply the changes introduced by some existing commits', '应用某些现有提交引入的更改'),
    (r'Graphical alternative to git-commit', 'git-commit 的图形化替代工具'),
    (r'Graphical alternative to git\-commit', 'git-commit 的图形化替代工具'),
    (r'Remove untracked files from the working tree', '从工作树中移除未跟踪的文件'),
    (r'Clone a repository into a new directory', '将仓库克隆到新目录'),
    (r'Record changes to the repository', '将更改记录到仓库'),
    (r'Give an object a human readable name based on an available ref', '基于可用引用为对象赋予人类可读的名称'),
    (r'Show changes between commits, commit and working tree, etc', '显示提交之间、提交与工作树之间的更改等'),
    (r'Download objects and refs from another repository', '从另一个仓库下载对象和引用'),
    (r'Prepare patches for e-mail submission', '准备用于电子邮件提交的补丁'),
    (r'Prepare patches for e\-mail submission', '准备用于电子邮件提交的补丁'),
    (r'Cleanup unnecessary files and optimize the local repository', '清理不必要的文件并优化本地仓库'),
    (r'Print lines matching a pattern', '打印匹配指定模式的行'),
    (r'A portable graphical interface to Git', 'Git 的便携式图形界面'),
    (r'EXPERIMENTAL: Rewrite history', '实验性功能：重写历史'),
    (r'Create an empty Git repository or reinitialize an existing one', '创建空 Git 仓库或重新初始化现有仓库'),
    (r'Run tasks to optimize Git repository data', '运行任务以优化 Git 仓库数据'),
    (r'Join two or more development histories together', '合并两个或多个开发历史'),
    (r'Move or rename a file, a directory, or a symlink', '移动或重命名文件、目录或符号链接'),
    (r'Add or inspect object notes', '添加或检查对象注释'),
    (r'Fetch from and integrate with another repository or a local branch', '从另一个仓库或本地分支获取并集成'),
    (r'Update remote refs along with associated objects', '更新远程引用及其关联对象'),
    (r'Compare two commit ranges \(e\.g\. two versions of a branch\)', '比较两个提交范围（例如一个分支的两个版本）'),
    (r'Reapply commits on top of another base tip', '在另一个基础顶端重新应用提交'),
    (r'Set HEAD or the index to a known state', '将 HEAD 或暂存区设置为已知状态'),
    (r'Restore working tree files', '恢复工作树文件'),
    (r'Revert some existing commits', '撤销某些现有提交'),
    (r'Remove files from the working tree and from the index', '从工作树和暂存区移除文件'),
    (r'Summarize git log output', '汇总 git log 的输出'),
    (r'Reduce your working tree to a subset of tracked files', '将工作树缩减为已跟踪文件的子集'),
    (r'Stash the changes in a dirty working directory away', '将脏工作目录中的更改暂存起来'),
    (r'Show the working tree status', '显示工作树状态'),
    (r'Initialize, update or inspect submodules', '初始化、更新或检查子模块'),
    (r'Switch branches\b', '切换分支'),
    (r'Create, list, delete or verify tags', '创建、列出、删除或验证标签'),
    (r'Manage multiple working trees', '管理多个工作树'),
    (r'The Git repository browser', 'Git 仓库浏览器'),
    (r'A tool for managing large Git repositories', '管理大型 Git 仓库的工具'),

    # Ancillary commands
    (r'Get and set repository or global options', '获取和设置仓库或全局选项'),
    (r'Git data exporter', 'Git 数据导出器'),
    (r'Git data importer', 'Git 数据导入器'),
    (r'Backend for fast Git data importers', '快速 Git 数据导入器的后端'),
    (r'Rewrite branches', '重写分支'),
    (r'Run merge conflict resolution tools to resolve merge conflicts', '运行合并冲突解决工具以解决合并冲突'),
    (r'Pack heads and tags for efficient repository access', '打包头引用和标签以实现高效的仓库访问'),
    (r'Prune all unreachable objects from the object database', '从对象数据库中修剪所有不可达对象'),
    (r'Manage reflog information', '管理引用日志信息'),
    (r'Hardlink common objects in local repositories', '在本地仓库之间硬链接共同对象'),
    (r'Create, list, delete refs to replace objects', '创建、列出、删除用于替换对象的引用'),
    (r'Low-level data transfers and history visualization', '低级数据传输和历史可视化'),
    (r'Low\-level data transfers and history visualization', '低级数据传输和历史可视化'),
    (r'Add or read or remove extended attributes', '添加、读取或移除扩展属性'),
    (r'Apply a patch to files and/or to the index', '将补丁应用到文件和/或暂存区'),
    (r'Verifies the connectivity and validity of the objects in the database', '验证数据库中对象的连通性和有效性'),
    (r'Provide content or type and size information for repository objects', '提供仓库对象的内容或类型和大小信息'),
    (r'Compute object ID and optionally create an object from a file', '计算对象 ID 并可选择从文件创建对象'),
    (r'Find commits yet to be applied to upstream', '查找尚未应用到上游的提交'),
    (r'Show the most recent tag that is reachable from a commit', '显示从提交可达的最近标签'),
    (r'Show changes using common diff tools', '使用通用差异工具显示更改'),
    (r'Extract commit ID from an archive created using git-archive', '从 git-archive 创建的归档中提取提交 ID'),
    (r'Print lines matching a pattern in tracked files', '在已跟踪文件中打印匹配模式的行'),
    (r'Show information about files in the index and the working tree', '显示暂存区和工作树中文件的信息'),
    (r'Display version information about Git', '显示关于 Git 的版本信息'),
    (r'Retrieve web pages that are stored in a remote repository', '检索存储在远程仓库中的网页'),
    (r'Find as good common ancestor as possible for a merge', '为合并找到尽可能好的共同祖先'),
    (r'Provides an overview of the working tree status', '提供工作树状态的概述'),
    (r'Check if two \.gitignore files are equivalent', '检查两个 .gitignore 文件是否等价'),
    (r'Show logs with differences each commit introduces', '显示每个提交引入差异的日志'),
    (r'Show the changes to a file that is not yet committed', '显示尚未提交的文件更改'),
    (r'Send a collection of patches from stdin to an IMAP folder', '从标准输入发送一组补丁到 IMAP 文件夹'),
    (r'Import an SVN repository into Git', '将 SVN 仓库导入 Git'),
    (r'Bidirectional operation between a Subversion repository and Git', 'Subversion 仓库与 Git 之间的双向操作'),
    (r'Send email with commits generated by git-format-patch', '使用 git-format-patch 生成的提交发送电子邮件'),
    (r'Instantly browse your working repository in gitweb', '在 gitweb 中即时浏览您的工作仓库'),
    (r'List the contents of a tree object', '列出树对象的内容'),
    (r'Display help information about Git', '显示关于 Git 的帮助信息'),
    (r'merge two files interactively', '交互式合并两个文件'),
    (r'Show three-way merge without touching index', '显示三路合并而不修改暂存区'),
    (r'Create a tag object with extra validation', '创建带有额外验证的标签对象'),
    (r'Update auxiliary index file to record tree changes', '更新辅助暂存区文件以记录树更改'),
    (r'Check and verify the connectivity and validity of the objects', '检查验证对象的连通性和有效性'),
    (r'Find symbolic names for given revs', '查找给定修订的符号名称'),
    (r'Pick out and mangle arguments to be used elsewhere', '提取和处理用于其他地方传递的参数'),
    (r'Show the difference between the index and a tree, changes between two trees, changes between two blob objects, or changes between two files on disk', '显示暂存区与树之间的差异、两棵树之间的更改、两个 blob 对象之间的更改或磁盘上两个文件之间的更改'),

    # ─── Option description translations (common single-line patterns) ───
    (r'Prints the synopsis and a list of the most commonly used commands', '打印概述和最常用命令的列表'),
    (r'If the option .*? is given then all available commands are printed', '如果给出的选项包括所有可用命令则打印'),
    (r'If a Git command is named this option will bring up the manual page for that command', '如果指定了 Git 命令名称，此选项将显示该命令的手册页'),
    (r'Other options are available to control how the manual page is displayed', '还有其他选项可用于控制手册页的显示方式'),
    (r'Run as if git was started in .*? instead of the current working directory', '如同 Git 是在指定路径中启动的，而非当前工作目录'),
    (r'Pass a configuration parameter to the command', '向命令传递一个配置参数'),
    (r'The value given will override values from configuration files', '给定的值将覆盖配置文件中的值'),
    (r'For example the following invocations are equivalent', '例如以下调用是等价的'),
    (r'Path to wherever your core Git programs are installed', '核心 Git 程序的安装路径'),
    (r'Print the path, without trailing slash, where Git\b', '打印路径（不含末尾斜杠），指向 Git'),
    (r'\bHTML documentation is installed and exit', 'HTML 文档的安装位置，然后退出'),
    (r'Set the path to the repository \([^)]*\)', '设置仓库目录的路径 '),
    (r'Do not pipe Git output into a pager', '不要将 Git 输出管道到分页器'),
    (r'Set the path to the working tree', '设置工作树的路径'),
    (r'It can be an absolute path or a path relative to the current working directory', '它可以是绝对路径或相对于当前工作目录的路径'),
    (r'It can be an absolute path or relative path to current working directory', '它可以是绝对路径或相对于当前工作目录的路径'),
    (r'Set the Git namespace', '设置 Git 命名空间'),
    (r'for more details', '了解更多详情'),
    (r'Equivalent to setting the', '等同于设置'),
    (r'Treat the repository as a bare repository', '将仓库视为裸仓库'),
    (r'If GIT_DIR environment is not set, it is set to the current working directory', '如果 GIT_DIR 环境变量未设置，则将其设置为当前工作目录'),
    (r'Do not use replacement refs to replace Git objects', '不使用替换引用来替换 Git 对象'),
    (r'Do not fetch missing objects from the promisor remote on demand', '不按需从提供者远程获取缺失的对象'),
    (r'Useful together with', '与...一起使用'),
    (r'to see if the object is locally available', '查看对象是否在本地可用'),
    (r'Do not perform optional operations that require locks', '不执行需要锁的可选操作'),
    (r'Disable all advice hints from being printed', '禁用所有建议提示的输出'),
    (r'Treat pathspecs literally', '按字面意义处理路径规格'),
    (r'no globbing, no pathspec magic', '不使用通配符，不使用路径规格魔法'),
    (r'Add "glob" magic to all pathspec', '为所有路径规格添加 "glob" 魔法'),
    (r'Add "literal" magic to all pathspec', '为所有路径规格添加 "literal" 魔法'),
    (r'Add "icase" magic to all pathspec', '为所有路径规格添加 "icase" 魔法'),
    (r'List commands by group', '按组列出命令'),
    (r'This is an internal/experimental option and may change or be removed in the future', '这是一个内部/实验性选项，将来可能更改或删除'),
    (r'Read gitattributes from .* instead of the worktree', '从指定源读取 gitattributes，而不是从工作树'),

    # ─── git-diff description translations ───
    (r'Generate patch', '生成补丁'),
    (r'This is the default', '这是默认值'),
    (r'Suppress all output from the diff machinery', '抑制差异机制的所有输出'),
    (r'Generate diffs with .* lines of context', '生成带上下文行的差异'),
    (r'Output to a specific file instead of stdout', '输出到指定文件而非标准输出'),
    (r'Specify the character used to indicate new, old or context lines in the generated patch', '指定生成的补丁中用于表示新、旧或上下文行的字符'),
    (r'Generate the diff in raw format', '以原始格式生成差异'),
    (r'Enable the heuristic that shifts diff hunk boundaries to make patches easier to read', '启用调整差异块边界的启发式算法，使补丁更易读'),
    (r'Disable the indent heuristic', '禁用缩进启发式算法'),
    (r'Spend extra time to make sure the smallest possible diff is produced', '花费额外时间确保生成最小的差异'),
    (r'Generate a diff using the "patience diff" algorithm', '使用"耐心差异"算法生成差异'),
    (r'Generate a diff using the "histogram diff" algorithm', '使用"直方图差异"算法生成差异'),
    (r'Choose a diff algorithm', '选择差异算法'),
    (r'The basic greedy diff algorithm', '基本贪心差异算法'),
    (r'Use "patience diff" algorithm when generating patches', '生成补丁时使用"耐心差异"算法'),
    (r'This algorithm extends the patience algorithm to "support low-occurrence common elements"', '该算法扩展了耐心算法以"支持低频公共元素"'),
    (r'Generate a diffstat', '生成差异统计'),
    (r'Output a condensed summary of extended header information', '输出扩展头部信息的简洁摘要'),
    (r'new\b.* or .*gone.* optionally .* if it', '新建或删除（可选地，如果是符号链接则'),
    (r'mode changes .* for adding or removing executable bit', '模式更改，用于添加或移除可执行位'),
    (r'Similar to .*stat, but shows number of added and deleted lines in decimal notation', '类似于统计，但以十进制表示显示添加和删除的行数'),
    (r'Output only the last line of the', '仅输出最后一行'),
    (r'format containing total number of modified files, as well as number of added and deleted lines', '格式，包含修改文件的总数以及添加和删除的行数'),
    (r'Output the distribution of relative amount of changes for each sub-directory', '输出每个子目录的相对更改量分布'),
    (r'Show only the name of each changed file in the post-image tree', '仅显示后镜像树中每个已更改文件的名称'),
    (r'Show only the name\(s\) and status of each changed file', '仅显示每个已更改文件的名称和状态'),
    (r'Specify how differences in submodules are shown', '指定如何显示子模块中的差异'),
    (r'Show colored diff', '显示彩色差异'),
    (r'Turn off colored diff', '关闭彩色差异'),
    (r'Moved lines of code are colored differently', '移动的代码行以不同颜色显示'),
    (r'Moved lines are not highlighted', '移动的行不高亮显示'),
    (r'Is a synonym for', '是的同义词'),
    (r'This may change to a more sensible mode in the future', '将来可能更改为更合理的模式'),
    (r'Blocks of moved text', '移动的文本块'),
    (r'Similar to .* in that', '类似于'),
    (r'augments the output', '增强输出'),

    # ─── git-log specific ───
    (r'Continue listing the history of a file beyond renames', '继续列出文件的历史，跨越重命名'),
    (r'Print out the ref names of any commits that are shown', '打印显示的任何提交的引用名称'),
    (r'Possible values are', '可能的值为'),
    (r'the ref name prefixes.*are not printed', '不打印引用名称前缀'),
    (r'the full ref name.*is printed', '打印完整的引用名称（包括前缀）'),
    (r'if the output is going to a terminal', '如果输出到终端'),
    (r'Print out the ref name given on the command line by which each commit was reached', '打印命令行上给出的用于到达每个提交的引用名称'),
    (r'Use mailmap file to map author and committer names', '使用 mailmap 文件将作者和提交者名称'),
    (r'to canonical real names and email addresses', '映射为规范的真名和电子邮件地址'),
    (r'Include a line .*log.*size.* in the output for each commit', '在每个提交的输出中包含一行日志大小信息'),
    (r'Intended to speed up tools that read log messages', '旨在加速读取日志消息的工具'),
    (r'Trace the evolution of the line range', '追踪行范围的演变'),
    (r'Show only commits in the specified revision range', '仅显示指定修订范围内的提交'),
    (r'Show only commits that are enough to explain how the files that match the specified paths came to be', '仅显示足以解释匹配指定路径的文件如何演变的提交'),
    (r'Paths may need to be prefixed with', '路径可能需要加上前缀'),

    # ─── git-config specific ───
    (r'List all variables set in config file, along with their values', '列出配置文件中设置的所有变量及其值'),
    (r'Emits the value of the specified key', '输出指定键的值'),
    (r'If key is present multiple times in the configuration, emits the last value', '如果键在配置中出现多次，则输出最后一个值'),
    (r'If .* is specified, emits all values associated with key', '如果指定则输出与键关联的所有值'),
    (r'Returns error code 1 if key is not present', '如果键不存在，则返回错误码 1'),
    (r'Set value for one or more config options', '为一个或多个配置选项设置值'),
    (r'By default, this command refuses to write multi-valued config options', '默认情况下，此命令拒绝写入多值配置选项'),
    (r'Passing .* will replace all multi-valued config options with the new value', '传递指定选项将用新值替换所有多值配置选项'),
    (r'whereas .* will replace all config options whose values match the given pattern', '而指定选项将替换所有值匹配给定模式的配置选项'),
    (r'Unset value for one or more config options', '取消设置一个或多个配置选项的值'),
    (r'By default, this command refuses to unset multi-valued keys', '默认情况下，此命令拒绝取消设置多值键'),
    (r'Passing .* will unset all multi-valued config options', '传递指定选项将取消设置所有多值配置选项'),
    (r'whereas .* will unset all config options whose values match the given pattern', '而指定选项将取消设置所有值匹配给定模式的配置选项'),
    (r'Rename the given section to a new name', '将给定节重命名为新名称'),
    (r'Remove the given section from the configuration file', '从配置文件中移除给定节'),
    (r'Opens an editor to modify the specified config file', '打开编辑器以修改指定的配置文件'),
    (r'Default behavior is to replace at most one line', '默认行为是至多替换一行'),
    (r'This replaces all lines matching the key', '这将替换所有匹配键的行'),
    (r'Adds a new line to the option without altering any existing values', '向选项添加新行，不修改任何现有值'),
    (r'Append a comment at the end of new or modified lines', '在新行或修改行的末尾追加注释'),
    (r'The following modes have been deprecated in favor of subcommands', '以下模式已弃用，推荐使用子命令'),
    (r'It is recommended to migrate to the new syntax', '建议迁移到新语法'),

    # ─── Generic multi-word phrases (more specific first) ───
    (r'current working directory', '当前工作目录'),
    (r'working directory', '工作目录'),
    (r'working tree', '工作树'),
    (r'standard output is a terminal', '标准输出是一个终端'),
    (r'standard output', '标准输出'),
    (r'standard input', '标准输入'),
    (r'standard error', '标准错误'),
    (r'command line', '命令行'),
    (r'environment variable', '环境变量'),
    (r'environment variables', '环境变量'),
    (r'configuration file', '配置文件'),
    (r'configuration files', '配置文件'),
    (r'config file', '配置文件'),
    (r'config option', '配置选项'),
    (r'config variable', '配置变量'),
    (r'repository local', '仓库本地'),
    (r'merge base', '合并基'),
    (r'regular expression', '正则表达式'),
    (r'regular expressions', '正则表达式'),
    (r'extended regular expression', '扩展正则表达式'),
    (r'basic regular expression', '基本正则表达式'),
    (r'fixed string', '固定字符串'),
    (r'patience diff', '耐心差异算法'),
    (r'histogram diff', '直方图差异算法'),
    (r'diff algorithm', '差异算法'),
    (r'raw format', '原始格式'),
    (r'human readable', '人类可读'),
    (r'revision range', '修订范围'),
    (r'commit logs', '提交日志'),
    (r'commit log', '提交日志'),
    (r'log message', '日志消息'),
    (r'merge commit', '合并提交'),
    (r'staging area', '暂存区'),
    (r'combined diff', '合并差异'),
    (r'binary file', '二进制文件'),
    (r'topic branch', '主题分支'),
    (r'remote branch', '远程分支'),
    (r'remote-tracking branch', '远程跟踪分支'),
    (r'bare repository', '裸仓库'),
    (r'promisor remote', '提供者远程'),
    (r'partial clone', '部分克隆'),
    (r'root commit', '根提交'),
    (r'merge strategy', '合并策略'),
    (r'shell glob', 'shell 通配符'),
    (r'case-sensitive', '区分大小写'),
    (r'case-insensitive', '不区分大小写'),
    (r'exit code', '退出码'),
    (r'exit status', '退出状态'),
    (r'error code', '错误码'),
    (r'true value', '真值'),
    (r'empty string', '空字符串'),
    (r'newline character', '换行符'),
    (r'null character', '空字符'),
    (r'null byte', '空字节'),
    (r'ref name', '引用名称'),
    (r'debug output', '调试输出'),
    (r'verbose output', '详细输出'),
    (r'pathspec magic', '路径规格魔法'),
    (r'answer file', '应答文件'),
    (r'stored in', '存储在'),
    (r'placed in', '放置于'),
    (r'found in', '位于'),
    (r'located in', '位于'),
    (r'installed in', '安装于'),

    # ─── Common phrases ───
    (r'instead of', '而不是'),
    (r'rather than', '而非'),
    (r'by default', '默认情况下'),
    (r'By default', '默认情况下'),
    (r'in other words', '换句话说'),
    (r'In other words', '换句话说'),
    (r'for example', '例如'),
    (r'For example', '例如'),
    (r'for instance', '例如'),
    (r'such as', '例如'),
    (r'for more information', '了解更多信息'),
    (r'for more details', '了解更多详情'),
    (r'for details', '了解详情'),
    (r'see also', '另请参见'),
    (r'See also', '另请参见'),
    (r'at least', '至少'),
    (r'at most', '最多'),
    (r'more than', '多于'),
    (r'less than', '少于'),
    (r'in addition', '此外'),
    (r'equivalent to', '等同于'),
    (r'as well as', '以及'),
    (r'note that', '请注意'),
    (r'Note that', '请注意'),
    (r'please note', '请注意'),
    (r'based on', '基于'),
    (r'depending on', '取决于'),
    (r'according to', '根据'),
    (r'together with', '与...一起'),
    (r'along with', '与...一起'),
    (r'similar to', '类似于'),
    (r'is set to', '设置为'),
    (r'defaults to', '默认为'),
    (r'Synonym for', '等同于'),
    (r'synonym for', '等同于'),
    (r'short-hand for', '简写形式'),
    (r'is a synonym of', '是的同义词'),
    (r'corresponds to', '对应于'),
    (r'points to', '指向'),
    (r'refers to', '指的是'),
    (r'applies to', '适用于'),
    (r'can be used', '可用于'),
    (r'may be used', '可用于'),
    (r'must be', '必须是'),
    (r'should be', '应该是'),
    (r'is used to', '用于'),
    (r'is used for', '用于'),
    (r'takes precedence', '优先'),
    (r'is internally converted to', '内部转换为'),
    (r'is equivalent to', '等同于'),
    (r'This is equivalent to', '这等同于'),
    (r'this is equivalent to', '这等同于'),

    # Cleanup double spaces from translations
    (r'  +', ' '),
]


def protect_options(text):
    """Replace option patterns (--option, --option=value, -x) with placeholders
    to prevent word-level translation of parts of option names."""
    placeholders = {}
    counter = [0]

    def replace_option(match):
        opt = match.group(0)
        key = f'__OPT_{counter[0]}__'
        counter[0] += 1
        placeholders[key] = opt
        return key

    # Protect --option-name=value patterns
    # These are roff-escaped in the text: \-\-option etc.
    # Pattern: \-\-word, --word, -x (single letter options)
    text = re.sub(r'(?:\\-){2}[\w\\\-.]+(?:=\S+)?', replace_option, text)
    text = re.sub(r'(?:--)[\w\-]+(?:=\S+)?', replace_option, text)
    text = re.sub(r'(?:\\-)[a-zA-Z](?:\s|$|,|\.)', replace_option, text)
    text = re.sub(r'(?:\\-)s(?:?:\s|$|,|\.)', replace_option, text)

    # Also protect config keys like core.worktree
    text = re.sub(r'\b[\w]+\\&\.[\w]+', replace_option, text)

    return text, placeholders


def restore_options(text, placeholders):
    """Restore placeholders to original option names."""
    for key, val in placeholders.items():
        text = text.replace(key, val)
    return text


def is_roff_directive(line):
    """Check if line is a pure roff formatting directive."""
    stripped = line.strip()
    if not stripped:
        return True
    if re.match(r'^\\?(\.(?:if|ie|el|sp|RS|RE|PP|fi|nf|nh|ad|de|TH|ss|SH|SS|de|ds|rm|hy|nr|ps|vs|ll|in|ti|po|na|so|mso|tr|char|fchar|ec|eo|ul|cu|mc|bp|ne|br|ft|cs|os|hb|wh|pl|pn|po|pf|lt|ev|ab|am))', stripped):
        return True
    if re.match(r'^\\\.\}', stripped):
        return True
    if re.match(r'^\'\\."', stripped):
        return True
    if re.match(r'^\\f[RIB]', stripped) and re.search(r'\\f[RIP]$', stripped):
        return True
    return False


def is_code_block(text):
    """Check if text is a source code block."""
    return bool(re.match(r'^\s+\$?\s*(git |cat |echo |ls |cd )', text))


def process_line(line):
    """Process a single line - translate English text to Chinese."""
    stripped = line.strip()

    # Exact section header match
    if stripped in EXACT_MAP:
        return EXACT_MAP[stripped]

    # SS subsection match
    for pattern, replacement in SS_MAP:
        if re.match(pattern, stripped):
            return replacement

    # Pure roff directives - pass through
    if is_roff_directive(line):
        return line

    # Code/example blocks - don't translate
    if is_code_block(stripped):
        return line

    # Blank lines
    if not stripped:
        return line

    # For everything else - translate
    result = line
    for pattern, replacement in RULES:
        result = re.sub(pattern, replacement, result)

    # Clean up excessive spaces
    result = re.sub(r'  +', ' ', result)

    return result


def process_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    result = []
    for line in lines:
        original = line.rstrip('\n')
        translated = process_line(original)
        result.append(translated)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result) + '\n')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 translate_man.py <input> <output>", file=sys.stderr)
        sys.exit(1)
    process_file(sys.argv[1], sys.argv[2])
    print(f"OK: {sys.argv[1]} -> {sys.argv[2]}")
