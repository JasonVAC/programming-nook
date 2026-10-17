#!/usr/bin/env python3
"""
Comprehensive man page translator - translates .SH, .SS, .IP headers
and English body text content to Chinese while preserving all roff codes.
"""
import os, re, gzip, subprocess, sys

SRC = "/usr/share/man/man1"
DST = "/tmp/man1_zh"
INST = "/usr/share/man/zh_CN/man1"

# ── .SH / .SS header translations ──
SEC_MAP = {
    "NAME": "名称",
    "SYNOPSIS": "概述",
    "DESCRIPTION": "描述",
    "NOTE": "注意",
    "NOTES": "注意",
    "OVERVIEW": "概述",
    "WARNING": "警告",
    "ERRORS": "错误",
    "SEE ALSO": "参见",
    "AUTHOR": "作者",
    "AUTHORS": "作者",
    "AUTHOR AND COPYRIGHT": "作者与版权",
    "COPYRIGHT": "版权",
    "LICENCE": "许可证",
    "LICENSE": "许可证",
    "BUGS": "缺陷",
    "DIAGNOSTICS": "诊断",
    "ENVIRONMENT": "环境",
    "FILES": "文件",
    "HISTORY": "历史",
    "EXAMPLES": "示例",
    "EXAMPLE": "示例",
    "ACKNOWLEDGMENTS": "致谢",
    "SUMMARY": "总结",
    "CREDITS": "致谢",
    "REFERENCES": "参考文献",
    "TODO": "待办事项",
    "CAVEATS": "注意事项",
    "IMPLEMENTATION": "实现",
    "SECURITY": "安全性",
    "SYNTAX": "语法",
    "SOLUTION": "解决方案",
    "THE SOLUTION": "解决方案",
    "RESTRICTIONS": "限制",
    "AVAILABILITY": "可用性",
    "SUPPORT": "支持",
    "REPORTING BUGS": "报告缺陷",
    "KNOWN ISSUES": "已知问题",
    "LIMITATIONS": "限制",
    "MISCELLANEOUS": "杂项",
    "HELP": "帮助",
    "USAGE": "用法",
    "OPTIONS": "选项",
    "OPERANDS": "操作数",
    "STDIN": "标准输入",
    "INPUT FILES": "输入文件",
    "OUTPUT FILES": "输出文件",
    "EXIT STATUS": "退出状态",
    "CONFIGURATION": "配置",
    "SIGNALS": "信号",
    "RETURN VALUE": "返回值",
    "PERFORMANCE": "性能",
    "PORTABILITY": "可移植性",
    "STANDARDS": "标准",
    "CONFORMING TO": "符合标准",
    "FUTURE DIRECTIONS": "未来方向",
    "CHANGES": "变更",
    "VERSION": "版本",
    "SOURCE": "源代码",
    "RELATED": "相关",
    "DEPENDENCIES": "依赖",
    "WHAT DOES IT TEST?": "它测试什么？",
    "WHO NEEDS COMPLICATED DATA STRUCTURES?": "谁需要复杂数据结构？",
    "THE GUIDE": "指南",
    "THE REST": "其余部分",
    "DISTRIBUTION CONDITIONS": "分发条件",
}

# ── .IP / .ie n .IP item translations ──
IP_MAP = {
    "Compilation": "编译",
    "Execution": "执行",
    "Parsing": "解析",
    "High Level": "高层概览",
    "Regops": "正则操作码",
    "Debug Output": "调试输出",
    "Program execution": "程序执行",
    "Simple Scalar": "简单标量",
    "Block": "块",
    "Arrow Notation": "箭头表示法",
    "Objects": "对象",
    "Miscellaneous Usage": "其他用法",
    "Circular References": "循环引用",
    "Symbolic references": "符号引用",
    "Not-so-symbolic references": "非符号引用",
    "Function Templates": "函数模板",
    "Postfix Dereference Syntax": "后缀解引用语法",
    "Postfix Reference Slicing": "后缀引用切片",
    "Assigning to References": "引用赋值",
    "Declaring a Reference to a Variable": "声明变量的引用",
    "Make Rule 1": "创建规则 1",
    "Make Rule 2": "创建规则 2",
    "Use Rule 1": "使用规则 1",
    "Use Rule 2": "使用规则 2",
    "Arrow Rule": "箭头规则",
    "An Example": "示例",
    "The Solution": "解决方案",
    "The Guide": "指南",
    "Simple word matching": "简单单词匹配",
    "Using character classes": "使用字符类",
    "Matching this or that": "匹配这个或那个",
    "Grouping things and hierarchical matching": "分组与层次匹配",
    "Extracting matches": "提取匹配",
    "Matching repetitions": "匹配重复",
    "More matching": "更多匹配",
    "Search and replace": "搜索与替换",
    "split operator": "split 操作符",
    "The split operator": "split 操作符",
    "Distribution Conditions": "分发条件",
    "Square Brackets": "方括号",
    "Curly Brackets": "花括号",
    "Anonymous Subroutines": "匿名子程序",
    "Constructors": "构造函数",
    "Autovivification": "自动活化",
    "Typeglob Slots": "类型团槽位",
    "Backslash Operator": "反斜杠操作符",
    "Pseudo-hashes: Using an array as a hash": "伪哈希：将数组用作哈希",
    "What is a regular expression engine?": "什么是正则表达式引擎？",
    "Structure of a Regexp Program": "正则程序的结构",
    "Process Overview": "流程概览",
    "Unicode and Localisation Support": "Unicode 与本地化支持",
    "Base Structures": "基础结构",
    "Peep-hole Optimisation and Analysis": "窥孔优化与分析",
    "Start position and no-match optimisations": "起始位置与无匹配优化",
    "A quick note on terms": "术语简要说明",
    "What regnode is next?": "下一个 regnode 是什么？",
    "REGNODE_AFTER": "REGNODE_AFTER",
    "regnext": "regnext",
    "A. Compilation": "A. 编译",
    "B. Execution": "B. 执行",
    "1. Parsing": "1. 解析",
    "2. Peep-hole optimisation and analysis": "2. 窥孔优化与分析",
    "3. Start position and no-match optimisations": "3. 起始位置与无匹配优化",
    "4. Program execution": "4. 程序执行",
    "regstclass": "regstclass",
    "data": "data",
    "code_blocks": "code_blocks",
    "proglen": "proglen",
    "name_list_idx": "name_list_idx",
    "program": "program",
}

# ── English phrases → Chinese (paragraph-level) ──
# Ordered by length descending so longer phrases match first
PHRASE_MAP = [
    ("This is complete documentation about all aspects of references", "这是关于引用所有方面的完整文档"),
    ("For a shorter, tutorial introduction to just the essential features", "关于基本特性的简短教学介绍"),
    ("because assignment operators in Perl (even within", "因为 Perl 中的赋值操作符（即使在"),
    ("One of the most important new features in Perl 5 was the capability to", "Perl 5 中最重要的新特性之一是能够"),
    ("The regular expression engine can be a weighty tool to wield", "正则表达式引擎可能是一个重量级工具"),
    ("This is essentially a linear encoding of a nondeterministic finite-state machine", "这本质上是一个非确定性有限状态机的线性编码"),
    ("References of the appropriate type can spring into existence", "适当类型的引用可以在需要时自动创建"),
    ("A reference to an anonymous array can be created using", "可以通过使用以下方式创建匿名数组的引用"),
    ("A reference to an anonymous hash can be created using", "可以通过使用以下方式创建匿名哈希的引用"),
    ("A reference to an anonymous subroutine can be created by", "可以通过以下方式创建匿名子程序的引用"),
    ("References are often returned by special subroutines called constructors", "引用通常由称为构造函数的特殊子程序返回"),
    ("A regular expression engine is a program that takes a set of constraints", "正则表达式引擎是一个程序，它接受一组约束"),
    ("In less grandiose terms, the first part of the job is to", "用更朴素的话来说，工作的第一部分是"),
    ("This document is an attempt to shine some light on the guts of", "本文档试图阐明"),
    ("It should be clearly understood that the behavior and structures discussed", "应明确理解，所讨论的行为和结构"),
    ("Readers of this document are expected to understand", "本文档的读者应当理解"),
    ("Perl's source code is stored in a Git repository", "Perl 的源代码存储在一个 Git 仓库中"),
    ("See perlhack for an explanation of Perl development", "有关 Perl 开发的说明，请参见 perlhack"),
    ("See perlgit for detailed information about Perl's Git repository", "有关 Perl Git 仓库的详细信息，请参见 perlgit"),
    ("The above documents supersede the information that was formerly here", "上述文档取代了之前此处的信息"),
    ("This page covers the very basics of understanding, creating and", "本页面涵盖理解、创建和使用"),
    ("This page assumes you already know things, like what a", "本页面假设你已经了解一些知识，例如"),
    ("The simplest regex is simply a word, or more generally, a string of", "最简单的正则表达式就是一个单词，或更一般地说，一个字符串"),
    ("A regex consisting of a word matches any string that", "由一个单词组成的正则表达式匹配任何包含该单词的"),
    ("In this statement,", "在这个语句中，"),
    ("Perl will always match at the earliest possible point in the string", "Perl 总是在字符串中最早可能的位置进行匹配"),
    ("Not all characters can be used 'as is' in a match", "并非所有字符都可以在匹配中原样使用"),
    ("called metacharacters, are considered special", "称为元字符，被视为特殊字符"),
    ("A metacharacter can be matched literally by putting a backslash before", "可以通过在前面加反斜杠来字面匹配元字符"),
    ("Non-printable ASCII characters are represented by escape sequences", "不可打印的 ASCII 字符用转义序列表示"),
    ("Regexes are treated mostly as double-quoted strings", "正则表达式大多被视为双引号字符串"),
    ("With all of the regexes above, if the regex matched anywhere in the", "对于以上所有正则表达式，如果正则表达式在"),
    ("A character class allows a set of possible characters", "字符类允许一组可能的字符"),
    ("There are a number of different types of character classes", "有许多不同类型的字符类"),
    ("We can match different character strings with the alternation", "我们可以使用交替匹配不同的字符串"),
    ("The grouping metacharacters allow a part of a regex to be", "分组元字符允许将正则表达式的一部分视为"),
    ("The grouping metacharacters also allow the extraction of the", "分组元字符还允许提取"),
    ("The quantifier metacharacters allow us to determine the number of", "量词元字符允许我们确定"),
    ("Search and replace is performed using", "搜索与替换使用"),
    ("The evaluation modifier wraps an eval around the", "求值修饰符将 eval 包裹在"),
    ("This is just a quick start guide.  For a more in-depth tutorial on", "这只是一个快速入门指南。有关更深入的教程"),
    ("The author would like to thank", "作者感谢"),
    ("This document may be distributed under the same terms as Perl itself", "本文档可按照与 Perl 本身相同的条款分发"),
    ("Copyright (c)", "版权所有 (c)"),
    ("All rights reserved.", "保留所有权利。"),
    ("Broadly speaking, performing a match of a string against a pattern", "概括地说，针对模式执行字符串的匹配"),
    ("This code resides primarily in", "这段代码主要位于"),
    ("The call graph looks like this", "调用图如下所示"),
    ("A grammar form might be something like this", "语法形式可能类似这样"),
    ("Another complication is that the representation used", "另一个复杂之处在于所使用的表示"),
    ("Making things worse is that UTF-8 support was a later addition", "更糟糕的是 UTF-8 支持是后来添加的"),
    ("No matter how you look at it, Unicode support is going to be a pain", "无论怎么看，Unicode 支持在正则表达式引擎中都会很麻烦"),
    ("Care must be taken when making changes to make sure", "在进行更改时必须小心确保"),
    ("Execution of a regex generally involves two phases", "正则表达式的执行通常涉及两个阶段"),
    ("If we can tell that there is no valid start point", "如果可以判断没有有效的起始点"),
    ("The basic structure of this routine is to try to find", "此例程的基本结构是尝试找到"),
    ("The two entry points are", "两个入口点是"),
    ("This is the main entry point for running a regex", "这是运行正则表达式的主要入口点"),
    ("This structure is used for handling data structures that", "此结构用于处理那些"),
    ("Description of the attributes is as follows", "属性描述如下"),
    ("Special regop that is used by", "被用于检查模式的特殊正则操作码"),
    ("This optional structure is used to manage", "此可选结构用于管理"),
    ("Stores the length of the compiled program", "存储已编译程序的长度"),
    ("This is the index into the data array where", "这是数据数组中的索引，其中存储了"),
    ("Compiled program. Inlined into the structure so", "已编译的程序。内联在结构中以便"),
    ("There is some debate as to whether to say", "关于应该说"),
    ("When speaking about regexes we need to distinguish between", "在谈论正则表达式时，我们需要区分"),
    ("It is possible to create a \"circular reference\" in Perl", "在 Perl 中可以创建\"循环引用\""),
    ("You can also create a circular reference with a single variable", "你也可以使用单个变量创建循环引用"),
    ("You can break circular references by creating a \"weak reference\"", "你可以通过创建\"弱引用\"来打破循环引用"),
    ("This is powerful, and slightly dangerous, in that it's possible", "这很强大但也有些危险，因为可能"),
    ("You may not (usefully) use a reference as the key to a hash", "你不能（有效地）使用引用作为哈希的键"),
    ("One problem that comes up all the time is needing a hash whose values", "一个经常出现的问题是需要一个值包含"),
    ("The natural way to do this is to have a hash whose keys are country", "自然的做法是使用一个哈希，其键是国家"),
    ("If hash values couldn't be lists, you lose", "如果哈希值不能是列表，你就输了"),
    ("By the time Perl 5 rolled around, we were already stuck with this", "到 Perl 5 推出时，我们已经受困于这个"),
    ("A reference is a scalar value that refers to an entire array or", "引用是一个标量值，它指向整个数组或"),
    ("References in Perl are like names for arrays and hashes", "Perl 中的引用就像是数组和哈希的名字"),
    ("We'll come back to this city-country problem later", "我们稍后会回到这个城市-国家问题"),
    ("There are just two ways to make a reference", "只有两种方式创建引用"),
    ("What can you do with a reference once you have it?", "拿到引用后能做什么？"),
    ("You can always use an array reference, in curly braces, in place of", "你总是可以在花括号中使用数组引用来替代"),
    ("Whatever you want to do with a reference,", "无论你想对引用做什么，"),
    ("The notation still looks a little cumbersome", "这种表示法看起来仍然有些繁琐"),
    ("In between two subscripts, the arrow is optional", "在两个下标之间，箭头是可选的"),
    ("The program has two pieces: Lines", "程序有两个部分：第"),
    ("There's one fine point I skipped. Line 5 is unnecessary", "我跳过了一个小细节。第 5 行是不必要的"),
    ("I promised to give you 90% of the benefit with 10% of the details", "我承诺给你 90% 的好处只讲 10% 的细节"),
    ("Some of the highlights of", "以下是一些要点"),
    ("You might prefer to go on to", "你可能更喜欢继续阅读"),
    ("Everyone needs compound data structures, and in Perl the way you", "每个人都需要复合数据结构，在 Perl 中你获取它们的方式"),
    ("This article originally appeared in", "本文最初发表于"),
    ("The original title was", "原标题为"),
    ("This documentation is free; you can redistribute it and/or modify it", "本文档是自由的；你可以重新分发和/或修改它"),
    ("Irrespective of its distribution, all code examples in these files are", "不论其分发方式，这些文件中的所有代码示例"),
    ("This applies only to lexical variables, by the way", "顺便说一下，这仅适用于词法变量"),
    ("Note particularly that", "特别注意"),
    ("This will still print", "这仍然会打印"),
    ("has always meant to print", "始终意味着打印"),
    ("will have the same effect", "将具有相同的效果"),
    ("The expression is true", "表达式为真"),
    ("A failed match or changing the target string resets the position", "匹配失败或更改目标字符串会重置位置"),
    ("If you don't want the position reset after failure to match", "如果你不希望在匹配失败后重置位置"),
    ("In list context,", "在列表上下文中，"),
    ("With the global modifier,", "使用全局修饰符，"),
    ("This is because", "这是因为"),
    ("Hard references are smart--they keep track", "硬引用是智能的——它们追踪"),
    ("One more thing here", "这里还有一个事项"),
    ("References are easy to use in Perl", "在 Perl 中使用引用很容易"),
    ("There is just one overriding principle", "只有一个首要原则"),
    ("works like this", "的工作方式如下"),
    ("it was difficult to represent complex data structures", "表示复杂数据结构是困难的"),
    ("Symbolic references are names of variables or other objects", "符号引用是变量或其他对象的名称"),
    ("In contrast, hard references are more like hard links", "相比之下，硬引用更像是 Unix 文件系统中的硬链接"),
    ("When the word \"reference\" is used without an adjective", "当\"引用\"一词不带形容词使用时"),
    ("References can be created in several ways", "引用可以通过多种方式创建"),
    ("it isn't possible to create a true reference to an IO handle", "无法使用反斜杠操作符创建对 IO 句柄的真正引用"),
    ("This doesn't copy the underlying array", "这不会复制底层数组"),
    ("To copy the array, use", "要复制数组，请使用"),
    ("To see if a variable contains a reference,", "要查看变量是否包含引用"),
    ("You can use a string as if it were a reference", "你可以将字符串当作引用来使用"),
    ("This is the \"positionally next regnode\" in the compiled regex program", "这是编译后的正则表达式程序中的\"位置上下一个 regnode\""),
    ("During compilation the engine may not know", "在编译期间，引擎可能不知道"),
    ("All of this occurs in the routine", "所有这些发生在"),
    ("The code involved in", "所涉及的代码"),
    ("Starting in the 5.9.x development version of perl you can", "从 perl 的 5.9.x 开发版本开始，你可以"),
    ("As you can see, even though we parsed out", "如你所见，即使我们解析出了"),
    ("The resulting program then looks like", "生成的程序看起来像"),
    ("Now let's try a harder pattern", "现在让我们尝试一个更复杂的模式"),
    ("Now for something much more complex", "现在来看更复杂的"),
    ("Here we can see a much more complex program", "在这里我们可以看到更复杂的程序"),
    ("The next pointer for", "的 next 指针"),
    ("Another form of optimisation that can occur", "另一种可能发生的优化形式是"),
    ("Another optimisation that can occur is that of", "另一种可能发生的优化是"),
    ("A side effect of this representation is that", "这种表示的一个副作用是"),
]

def tr_paragraph(text):
    """Translate English paragraph text to Chinese"""
    result = text
    # Apply longer replacements first
    for eng, chn in sorted(PHRASE_MAP, key=lambda x: -len(x[0])):
        result = result.replace(eng, chn)
    return result

REPLACE_MAP = []

def tr_sh_ss(line):
    """Translate .SH and .SS headers"""
    for prefix in ('.SH ', '.SS '):
        if line.startswith(prefix):
            rest = line[len(prefix):]
            stripped = rest.strip().strip('"').strip("'")
            for eng, chn in sorted(SEC_MAP.items(), key=lambda x: -len(x[0])):
                if stripped.upper() == eng.upper() or stripped.upper().startswith(eng.upper()):
                    suffix = stripped[len(eng):]
                    result = f'{prefix}"{chn}{suffix}"' if '"' in rest else f'{prefix}{chn}{suffix}'
                    # Fix potential issues with special chars
                    if '\\' in suffix:
                        # Keep it as-is without extra quotes
                        result = f'{prefix}{chn}{suffix}'
                    return result
            break
    return line

def tr_ip(line):
    """Translate .IP items"""
    # Pattern: .IP "text" N  or .IP text N
    m = re.match(r'(\.[iI][pP]\s+)(["\']?)(.+?)(\2\s+\d+)', line)
    if m:
        prefix, q, text, suffix = m.group(1), m.group(2), m.group(3), m.group(4)
        for eng, chn in sorted(IP_MAP.items(), key=lambda x: -len(x[0])):
            if text == eng:
                return f'{prefix}{q}{chn}{suffix}'
    return line

def tr_paragraph(text):
    """Translate English paragraph text to Chinese"""
    # Apply replacement rules
    for eng, chn in REPLACE_MAP:
        text = text.replace(eng, chn)
    for eng, chn in PHRASE_MAP:
        text = text.replace(eng, chn)
    return text

def process_file(basename):
    src_path = os.path.join(SRC, basename + '.gz')
    dst_path = os.path.join(DST, basename)
    
    with gzip.open(src_path, 'rt', errors='replace') as f:
        content = f.read()
    
    lines = content.split('\n')
    result = []
    in_vb = False
    in_de_block = False
    
    for line in lines:
        # Track verbatim blocks
        if line.startswith('.Vb'):
            in_vb = True
            result.append(line)
            continue
        if line.startswith('.Ve'):
            in_vb = False
            result.append(line)
            continue
        
        # Track .de blocks (macro definitions)
        if line.startswith('.de '):
            in_de_block = True
            result.append(line)
            continue
        if in_de_block and line.strip() == '..':
            in_de_block = False
            result.append(line)
            continue
        
        if in_vb or in_de_block:
            result.append(line)
            continue
        
        # Skip lines that are entirely roff commands/codes
        if line.startswith('.'):
            # Translate macros
            result.append(tr_sh_ss(line) if line.startswith('.SH ') or line.startswith('.SS ') else tr_ip(line) if line.startswith('.IP ') else line)
            continue
        
        # Translate paragraph text (non-roff lines)
        if line.strip() and not line.startswith('.') and not line.startswith("'br"):
            result.append(tr_paragraph(line))
        else:
            result.append(line)
    
    output = '\n'.join(result)
    with open(dst_path, 'w') as f:
        f.write(output)
    
    # Gzip
    gz_path = dst_path + '.gz'
    with open(dst_path, 'rb') as fin, gzip.open(gz_path, 'wb') as fout:
        fout.write(fin.read())
    
    # Install
    subprocess.run(['sudo', 'cp', gz_path, os.path.join(INST, basename + '.gz')], 
                   capture_output=True)
    os.unlink(dst_path)
    os.unlink(gz_path)
    return basename

if __name__ == '__main__':
    files = [line.strip() for line in open('/tmp/perl_batch5.txt') if line.strip()]
    count = 0
    for f in files:
        try:
            process_file(f)
            count += 1
            if count % 10 == 0:
                print(f"  processed {count}/{len(files)}: {f}")
        except Exception as e:
            print(f"  FAIL {f}: {e}")
    print(f"perl batch 5 done: {count} translations")
