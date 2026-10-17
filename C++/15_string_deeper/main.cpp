// 15_string_deeper — String View & String Stream
// std::string_view (C++17): 轻量只读视图，零拷贝
// std::stringstream: 字符串的流式拼装/解析

#include <iostream>
#include <string>
#include <string_view>
#include <sstream>
#include <iomanip>
#include <vector>

// ============================================================
// 1. std::string_view — 看看就行，不拷贝
// ============================================================
void demo_string_view() {
    std::cout << "=== std::string_view ===\n";

    std::string s = "Hello, C++23!";
    const char* cstr = "Raw C string";
    std::string_view sv1 = s;       // 从 std::string 构造
    std::string_view sv2 = cstr;    // 从 const char* 构造
    std::string_view sv3 = "字面量"; // 从字面量构造——全零拷贝！

    std::cout << "sv1: " << sv1 << " (size=" << sv1.size() << ")\n";
    std::cout << "sv2: " << sv2 << " (size=" << sv2.size() << ")\n";
    std::cout << "sv3: " << sv3 << " (size=" << sv3.size() << ")\n";

    // 子串——不拷贝
    std::string_view sub = sv1.substr(7, 5);  // "C++23"
    std::cout << "substr(7, 5): " << sub << "\n";

    // 查找
    if (sv1.find("C++") != std::string_view::npos) {
        std::cout << "Found 'C++' in sv1\n";
    }

    // ⚠️ 注意：不拥有数据，源数据销毁后悬空
    std::string_view danger;
    {
        std::string temp = "I'll be gone soon";
        danger = temp;
    } // temp 销毁
    // std::cout << danger;  // ❌ 未定义行为！悬空指针！
    std::cout << "(danger is now dangling - don't use it!)\n\n";
}

// ============================================================
// 2. std::ostringstream — 拼字符串
// ============================================================
void demo_ostringstream() {
    std::cout << "=== std::ostringstream ===\n";

    std::ostringstream oss;

    std::string name = "小明";
    int age = 16;
    double score = 92.5;

    oss << "姓名: " << name << "\n";
    oss << "年龄: " << age << " 岁\n";
    oss << "成绩: " << std::fixed << std::setprecision(1) << score << "\n";

    std::string result = oss.str();  // 取出拼好的完整字符串
    std::cout << result;
}

// ============================================================
// 3. std::istringstream — 解析字符串，支持数组
// ============================================================
void demo_istringstream() {
    std::cout << "=== std::istringstream (parse) ===\n";

    std::string data = "42 3.14 hello 99";

    std::istringstream iss(data);

    std::vector<int>    ints;
    std::vector<double> doubles;
    std::vector<std::string> strings;

    int    i;
    double d;
    std::string s;

    // 逐个读取直到末尾
    while (iss >> i) {
        ints.push_back(i);
    }

    // 重置流状态，继续读取
    iss.clear();
    // 跳过整数
    for (size_t j = 0; j < ints.size(); ++j) {
        iss >> d >> s;
        doubles.push_back(d);
        strings.push_back(s);
    }

    std::cout << "第一轮解析有点tricky, 不如逐词判断类型...\n\n"
              << "更实用的做法：按行+分隔符拆分 (见下一个demo)\n";
}

// ============================================================
// 4. 按分隔符拆分字符串 (综合应用)
// ============================================================
std::vector<std::string> split(const std::string& str, char delimiter) {
    std::vector<std::string> result;
    std::istringstream iss(str);
    std::string token;

    while (std::getline(iss, token, delimiter)) {
        result.push_back(token);
    }

    return result;
}

void demo_split() {
    std::cout << "=== Split string by delimiter ===\n";

    std::string fruits = "apple,banana,cherry,grape,orange";

    std::vector<std::string> items = split(fruits, ',');

    std::cout << "Original: " << fruits << "\n\n";
    for (size_t i = 0; i < items.size(); ++i) {
        std::cout << "  [" << i + 1 << "] " << items[i] << "\n";
    }
    std::cout << "\n";
}

// ============================================================
// 5. 综合练习
// ============================================================
void exercise_hint() {
    std::cout << "=== 练习 ===\n";
    std::cout << "文件 'data.txt' 里有学生成绩:\n";
    std::cout << "  张三,85,92,78\n";
    std::cout << "  李四,90,88,95\n";
    std::cout << "  ...\n\n";
    std::cout << "用 getline + istringstream 读取并计算平均分!\n";
    std::cout << "(等学到 fileio 就能真的读文件了, 先用字符串模拟)\n\n";
}

// ============================================================
int main() {
    demo_string_view();
    demo_ostringstream();
    demo_istringstream();
    demo_split();
    exercise_hint();

    return 0;
}
