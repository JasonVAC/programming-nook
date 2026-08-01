// 11_references - 引用 &（References）
// g++ -std=c++23 -Wall -Wextra 11_references.cpp -o 11_references

#include <iostream>
#include <string>
#include <vector>

void separator(const std::string& title) {
    std::cout << "\n========== " << title << " ==========\n\n";
}

// ============================================
// 引用作为参数 — 避免拷贝（最常见用法）
// ============================================
void printMessage(const std::string& msg) {
    // const & = 只读引用，不拷贝，安全
    std::cout << "📨 " << msg << "\n";
}

void makeExciting(std::string& msg) {
    // 非常量引用 — 可以修改原变量
    msg += "!!!";
}

// ============================================
// 引用作为返回值
// ============================================
int& getElement(std::vector<int>& vec, size_t index) {
    return vec[index];  // 返回引用，可以当左值用
}

// ============================================
// 指针 vs 引用 对比示例
// ============================================
void swapWithPtr(int* a, int* b) {
    if (!a || !b) return;       // 需要检查空指针
    int temp = *a;
    *a = *b;
    *b = temp;
}

void swapWithRef(int& a, int& b) {
    // 不需要检查 — 引用不能为空，保证有效
    int temp = a;
    a = b;
    b = temp;
}

// ============================================
// 引用和 const 的组合
// ============================================
struct BigData {
    int id;
    std::string content;
    double values[100];
};

// ✅ const & — 不拷贝，只读访问
void printBigData(const BigData& data) {
    std::cout << "BigData #" << data.id << "\n";
}

// ❌ 传值 — 拷贝整个结构，浪费性能
void printBigDataCopy(BigData data) {
    std::cout << "BigData #" << data.id << "\n";
}


int main() {
    // ============================================
    // 1. 基本用法：引用就是别名
    // ============================================
    separator("基本引用");

    int original = 42;
    int& ref = original;     // ref 是 original 的别名

    std::cout << "original: " << original << "\n";
    std::cout << "ref:      " << ref << "\n";

    ref = 100;               // 通过引用修改原变量
    std::cout << "修改 ref 后 original: " << original << "\n";
    std::cout << "&original == &ref? " << (&original == &ref) << " ✅\n";

    // 引用必须初始化，不能为空
    // int& bad;   // ❌ 编译错误：引用必须初始化
    // int& null = nullptr;  // ❌ 编译错误

    // ============================================
    // 2. 引用 vs 指针 — 关键区别
    // ============================================
    separator("引用 vs 指针");

    int x = 10, y = 20;

    // 指针
    int* ptr = &x;
    ptr = &y;                // 可以改指向
    *ptr = 30;               // 改值

    // 引用
    int& ref2 = x;
    // ref2 = &y;            // ❌ 不能改指向
    ref2 = y;                // ✅ 这是赋值，不是改指向！此操作把 y 的值赋给 x
    std::cout << "赋值后 x = " << x << ", y = " << y << "\n";  // x=20, y=20

    // 重新初始化 x
    x = 10; y = 20;

    std::cout << "\n区别总结:\n";
    std::cout << "  指针: 可以为空 | 可以重新指向 | 需要 * 解引用\n";
    std::cout << "  引用: 不能为空 | 不能改指向 | 直接用\n";

    // ============================================
    // 3. 引用参数 — 最实用的场景
    // ============================================
    separator("引用参数");

    std::string greeting = "Hello";
    
    // const & — 不拷贝，不改原值
    printMessage(greeting);

    // & — 允许修改原值
    makeExciting(greeting);
    std::cout << "makeExciting 后: " << greeting << "\n";

    // 交换演示
    int p = 100, q = 200;

    swapWithPtr(&p, &q);
    std::cout << "指针版交换: p=" << p << ", q=" << q << "\n";

    swapWithRef(p, q);
    std::cout << "引用版交换: p=" << p << ", q=" << q << "\n";

    // ============================================
    // 4. 引用返回值 — 可当左值
    // ============================================
    separator("引用返回值");

    std::vector<int> nums = {10, 20, 30, 40, 50};

    std::cout << "原始: ";
    for (int n : nums) std::cout << n << " ";
    std::cout << "\n";

    // 函数返回引用，可以赋值
    getElement(nums, 2) = 999;
    
    std::cout << "修改后: ";
    for (int n : nums) std::cout << n << " ";
    std::cout << "\n";

    // ============================================
    // 5. 范围 for 循环中的引用
    // ============================================
    separator("范围 for + 引用");

    std::vector<int> scores = {60, 75, 80, 95};

    // 不加引用 — 副本，改不了原数组
    for (int s : scores) {
        s += 5;  // 没用！s 是拷贝
    }
    std::cout << "不加引用（没改变）: ";
    for (int s : scores) std::cout << s << " ";
    std::cout << "\n";

    // 加引用 — 直接修改原数组
    for (int& s : scores) {
        s += 5;  // ✅ 直接修改 scores 里的元素
    }
    std::cout << "加引用（修改成功）: ";
    for (int s : scores) std::cout << s << " ";
    std::cout << "\n";

    // const & — 只读，避免拷贝大对象
    for (const int& s : scores) {
        std::cout << s << " ";  // 只读，不能修改
    }
    std::cout << "\n";

    std::vector<std::string> names = {"Alice", "Bob", "Charlie"};
    
    // const std::string& — 避免拷贝字符串
    for (const std::string& name : names) {
        std::cout << name[0] << " ";
    }
    std::cout << "\n";

    // ============================================
    // 6. 何时用引用 vs 指针 vs 值
    // ============================================
    separator("选择指南");

    std::cout << "                |   传值   |   引用   |   指针   \n";
    std::cout << "────────────────┼──────────┼──────────┼──────────\n";
    std::cout << "读数据          │ 小对象🆗 | ✅ 推荐  |  可以    \n";
    std::cout << "                │ 大对象❌ |          |          \n";
    std::cout << "修改数据        │ ❌       | ✅ 推荐  |  可以    \n";
    std::cout << "可为空 / 可选   │ N/A      | ❌       | ✅ 推荐  \n";
    std::cout << "重指向          │ N/A      | ❌       | ✅       \n";
    std::cout << "RAII / 智能指针  │ N/A      | N/A      | ✅ 推荐  \n";

    // ============================================
    // 7. 引用和 constexpr
    // ============================================
    separator("constexpr 引用");

    constexpr int ARRAY_SIZE = 100;
    int big[ARRAY_SIZE] = {};  // 零初始化

    // const 引用绑定到字面量
    const int& refConst = 42;
    std::cout << "const引用绑定字面量: " << refConst << "\n";

    // 数组引用
    int (&arrRef)[ARRAY_SIZE] = big;  // 引用整个数组
    arrRef[0] = 1;
    std::cout << "数组引用: big[0] = " << big[0] << "\n";

    // ============================================
    // 8. 小心：悬挂引用
    // ============================================
    separator("⚠️ 危险：悬挂引用");

    // 返回局部变量的引用 = 悬空引用（危险！）
    auto badRef = []() -> const int& {
        int local = 42;
        return local;  // local 出作用域就销毁了
    };
    // const int& dangling = badRef();  // ❌ 未定义行为！
    
    std::cout << "永远不要返回局部变量的引用！\n";
    std::cout << "返回引用时确保引用对象的生命周期足够长\n";

    return 0;
}
