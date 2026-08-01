// 10_strings - std::string 深入
// g++ -std=c++23 -Wall -Wextra 10_strings.cpp -o 10_strings

#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <algorithm>

void separator(const std::string& title) {
    std::cout << "\n========== " << title << " ==========\n\n";
}

int main() {
    // ============================================
    // 1. 四种构造方式
    // ============================================
    separator("构造方式");

    std::string s1;                          // 空字符串
    std::string s2 = "Hello C++";            // 从字面量
    std::string s3(5, 'A');                  // 重复 5 个 'A' → "AAAAA"
    std::string s4(s2, 0, 5);                // 取 s2 的前 5 个字符 → "Hello"

    std::cout << "s1 (空):     [" << s1 << "]\n";
    std::cout << "s2 (字面量): [" << s2 << "]\n";
    std::cout << "s3 (重复):   [" << s3 << "]\n";
    std::cout << "s4 (子串):   [" << s4 << "]\n";

    // 原始字符串字面量 (Raw string literal) — 不需要转义
    // 格式: R"(内容)"，里面的 \n 就是真的反斜杠+n，不是换行
    std::string path = R"(C:\Program Files\My App\)";
    std::string multiline = R"(第一行
第二行
第三行)";
    std::cout << "Raw path:    [" << path << "]\n";
    std::cout << "Raw multi:   [" << multiline << "]\n";

    // ============================================
    // 2. 大小相关
    // ============================================
    separator("大小 & 容量");

    std::string text = "Hello 世界";

    std::cout << "内容:     " << text << "\n";
    std::cout << "长度:     " << text.length() << "\n";    // 12 (中文占3字节)
    std::cout << "大小:     " << text.size() << "\n";      // 跟 length 一样
    std::cout << "空?       " << (text.empty() ? "是" : "否") << "\n";
    std::cout << "容量:     " << text.capacity() << "\n";  // 预分配的空间

    // 预留空间提升性能
    std::string big;
    big.reserve(1000);  // 提前分好空间，避免多次扩容
    std::cout << "reserve 后容量: " << big.capacity() << "\n";

    // 裁剪多余空间
    big = "很短";
    big.shrink_to_fit();
    std::cout << "shrink 后容量:  " << big.capacity() << "\n";

    // ============================================
    // 3. 访问元素
    // ============================================
    separator("访问元素");

    std::string greet = "Hello";

    // operator[] — 快速，但不做边界检查
    std::cout << "greet[0] = " << greet[0] << "\n";     // H
    std::cout << "greet[4] = " << greet[4] << "\n";     // o

    // at() — 带边界检查，越界抛异常
    std::cout << "greet.at(1) = " << greet.at(1) << "\n";  // e

    // front() / back() — 快速访问首尾
    std::cout << "首字符: " << greet.front() << "\n";   // H
    std::cout << "尾字符: " << greet.back() << "\n";    // o

    // 尝试越界
    // greet[100];                  // ❌ 危险，不会报错
    // greet.at(100);               // ✅ 抛出 std::out_of_range

    // ============================================
    // 4. 追加 & 拼接
    // ============================================
    separator("追加 & 拼接");

    std::string result;

    // += 运算符
    result += "Hello";
    result += ' ';
    result += "World";
    std::cout << "用 +=: " << result << "\n";

    // append() — 更灵活
    result.append("!");                       // 追加字符串
    result.append(3, '!');                    // 追加 3 个 !
    std::cout << "用 append: " << result << "\n";

    // push_back() — 追加单个字符
    result.push_back('!');
    std::cout << "用 push_back: " << result << "\n";

    // + 运算符 — 拼接新字符串
    std::string a = "Hello ";
    std::string b = a + "World!";
    std::cout << "用 +: " << b << "\n";

    // 数字 → 字符串
    int num = 42;
    double pi = 3.14159;
    std::string nums = std::to_string(num) + " " + std::to_string(pi);
    std::cout << "数字转字符串: " << nums << "\n";

    // ============================================
    // 5. 插入 & 删除 & 替换
    // ============================================
    separator("插入 & 删除 & 替换");

    std::string editor = "Good World";

    // insert(pos, str) — 在 pos 位置插入
    editor.insert(5, "Good ");
    std::cout << "insert: " << editor << "\n";  // Good Good World

    // erase(pos, len) — 删除从 pos 起的 len 个字符
    editor.erase(0, 5);   // 删掉第一个 "Good "
    std::cout << "erase:  " << editor << "\n";  // Good World

    // replace(pos, len, str) — 替换
    editor.replace(5, 5, "C++");   // 从位置5开始，替换5个字符
    std::cout << "replace: " << editor << "\n";  // Good C++

    // clear() — 清空
    editor.clear();
    std::cout << "clear 后: [" << editor << "]\n";

    // ============================================
    // 6. 子串
    // ============================================
    separator("子串 (substr)");

    std::string sentence = "The quick brown fox";
    std::string word = sentence.substr(4, 5);   // 从 4 取 5 个 → "quick"
    std::cout << "substr(4, 5): " << word << "\n";

    std::string tail = sentence.substr(10);     // 从 10 取到末尾 → "brown fox"
    std::cout << "substr(10):   " << tail << "\n";

    // ============================================
    // 7. 查找
    // ============================================
    separator("查找");

    std::string text2 = "Hello World, Hello C++";

    // find() — 正向查找，返回首次出现位置
    size_t pos = text2.find("Hello");
    std::cout << "find \"Hello\": " << pos << "\n";  // 0

    // rfind() — 反向查找
    pos = text2.rfind("Hello");
    std::cout << "rfind \"Hello\": " << pos << "\n";  // 13

    // find 不存在时返回 npos
    pos = text2.find("xyz");
    if (pos == std::string::npos) {
        std::cout << "find \"xyz\": 没找到（npos）\n";
    }

    // find_first_of() — 找第一个匹配集合中的字符
    pos = text2.find_first_of(" ,!");
    std::cout << "第一个空格/逗号/感叹号在: " << pos << "\n";  // 5 (空格)

    // find_last_of() — 最后一个匹配集合中的字符
    pos = text2.find_last_of(" ,!");
    std::cout << "最后一个空格/逗号/感叹号在: " << pos << "\n";

    // find_first_not_of() — 第一个不匹配的
    std::string digits = "123abc";
    pos = digits.find_first_not_of("0123456789");
    std::cout << "数字串中第一个非数字在: " << pos << "\n";  // 3 ('a')

    // contains() — C++23 新特性，找不找得到
    if (text2.contains("C++")) {
        std::cout << "包含 \"C++\" ✅\n";
    }

    // starts_with() / ends_with() — C++20
    if (text2.starts_with("Hello")) {
        std::cout << "以 Hello 开头 ✅\n";
    }
    if (text2.ends_with("C++")) {
        std::cout << "以 C++ 结尾 ✅\n";
    }

    // ============================================
    // 8. 比较
    // ============================================
    separator("比较");

    std::string x = "apple";
    std::string y = "banana";

    // operator== 直接比
    std::cout << x << " == " << y << " ? " << (x == y) << "\n";
    std::cout << x << " < "  << y << " ? " << (x < y)  << "\n";   // a < b，true

    // compare() — 更精细的比较
    // 返回: 负数(<), 0(==), 正数(>)
    int cmp = x.compare(y);
    std::cout << "compare 返回: " << cmp << "\n";

    // 比较局部
    std::string z = "applaud";
    cmp = x.compare(0, 5, z, 0, 5);  // x[0:5] "apple" vs z[0:5] "appla"
    std::cout << "局部 compare: " << cmp << "\n";

    // ============================================
    // 9. 字符串 ↔ 数字
    // ============================================
    separator("字符串 ↔ 数字");

    // 字符串 → 数字
    std::string numStr = "  123  ";
    int i = std::stoi(numStr);              // 自动去掉首尾空格
    double d = std::stod("3.14159");
    long l = std::stol("9876543210");
    float f = std::stof("2.71828f");

    std::cout << "stoi(\"  123  \") = "  << i << "\n";
    std::cout << "stod(\"3.14159\")  = "  << d << "\n";
    std::cout << "stol(\"9876543210\") = " << l << "\n";
    std::cout << "stof(\"2.71828\")   = "  << f << "\n";

    // 带错误检查的版本
    try {
        std::string bad = "abc123";
        int n = std::stoi(bad);
        std::cout << "解析成功: " << n << "\n";
    } catch (const std::invalid_argument& e) {
        std::cout << "解析失败（未以数字开头）: " << e.what() << "\n";
    } catch (const std::out_of_range& e) {
        std::cout << "数字溢出: " << e.what() << "\n";
    }

    // 数字 → 字符串（上面已经提过 to_string，这里再演示同类型的用法）
    std::cout << "pi = " << std::to_string(3.14159) << "\n";

    // ============================================
    // 10. C 风格字符串互操作
    // ============================================
    separator("C 风格字符串");

    std::string cpp = "I'm C++";

    // c_str() → const char*（只读，以 '\0' 结尾）
    const char* cstr = cpp.c_str();
    std::cout << "c_str(): " << cstr << "\n";

    // data() → 跟 c_str() 一样，C++17 后也返回 const char*
    const char* data = cpp.data();
    std::cout << "data():  " << data << "\n";

    // 从 C 风格字符串构建 C++ 字符串
    const char* old = "I'm C-style string";
    std::string modern = old;
    std::cout << "从 C 风格构建: " << modern << "\n";

    // ============================================
    // 11. 遍历字符串
    // ============================================
    separator("遍历");

    std::string traversal = "C++";

    // 方式 1: 索引
    std::cout << "索引遍历: ";
    for (size_t i = 0; i < traversal.size(); ++i) {
        std::cout << traversal[i] << " ";
    }
    std::cout << "\n";

    // 方式 2: 范围 for (推荐)
    std::cout << "范围 for: ";
    for (char ch : traversal) {
        std::cout << ch << " ";
    }
    std::cout << "\n";

    // 方式 3: 迭代器
    std::cout << "迭代器:   ";
    for (auto it = traversal.begin(); it != traversal.end(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << "\n";

    // ============================================
    // 12. 实战: 字符串分割器
    // ============================================
    separator("实战: 分割字符串");

    std::string csv = "apple,banana,orange,grape";
    std::vector<std::string> fruits;
    size_t start = 0;
    size_t end = csv.find(',');

    while (end != std::string::npos) {
        fruits.push_back(csv.substr(start, end - start));
        start = end + 1;
        end = csv.find(',', start);
    }
    fruits.push_back(csv.substr(start));  // 最后一段

    std::cout << "分割 [apple,banana,orange,grape]:\n";
    for (const auto& f : fruits) {
        std::cout << "  🍉 " << f << "\n";
    }

    // 用 stringstream 分割（更简洁）
    separator("实战: stringstream 分割");

    std::string input = "How are you today";
    std::vector<std::string> words;
    std::istringstream stream(input);
    std::string token;

    while (stream >> token) {
        words.push_back(token);
    }

    std::cout << "按空格分割: [How are you today]\n";
    for (const auto& w : words) {
        std::cout << "  📝 " << w << "\n";
    }

    // ============================================
    // 13. <algorithm> + string
    // ============================================
    separator("算法 + string");

    std::string messy = "C++_is_FUN!";

    // 转大写
    std::string upper = messy;
    std::ranges::transform(upper, upper.begin(),
                           [](unsigned char c) { return std::toupper(c); });
    std::cout << "转大写:  " << upper << "\n";

    // 转小写
    std::string lower = messy;
    std::ranges::transform(lower, lower.begin(),
                           [](unsigned char c) { return std::tolower(c); });
    std::cout << "转小写:  " << lower << "\n";

    // 去除空格 (trim)
    std::string padded = "   too much space   ";
    // 去掉前导空格
    padded.erase(0, padded.find_first_not_of(' '));
    // 去掉后导空格
    padded.erase(padded.find_last_not_of(' ') + 1);
    std::cout << "trim 后: [" << padded << "]\n\n";

    // ============================================
    // 14. 性能小提示
    // ============================================
    separator("性能提示");

    std::cout << "1. 用 reserve() 预分配: 避免多次重新分配\n";
    std::cout << "2. operator[] 比 at() 快（无边界检查）\n";
    std::cout << "3. += 比 + 好（不会创建临时对象）\n";
    std::cout << "4. 大量拼接用 stringstream 而不是 ++\n";
    std::cout << "5. 传参用 const std::string&，别复制\n";

    return 0;
}
