#include <iostream>

// ===== 函数声明 / 定义 =====
// 返回类型  函数名 (参数列表)

void say_hello() {
    std::cout << "Hello!" << std::endl;
}

int add(int x, int y) {
    return x + y;
}

double square(double x) {
    return x * x;
}

// ===== 函数重载（同名不同参）=====
int max(int a, int b) {
    return (a > b) ? a : b;
}

double max(double a, double b) {
    return (a > b) ? a : b;
}

// ===== 默认参数 =====
void greet(std::string name = "World") {
    std::cout << "Hello, " << name << "!" << std::endl;
}

// ===== 传值 vs 传引用 =====
void by_value(int x) {
    x = 999;
    std::cout << "  inside by_value: x = " << x << std::endl;
}

void by_reference(int &x) {
    x = 999;  // 改了外面的变量
}

// ===== 主函数 =====
int main() {
    say_hello();

    int sum = add(3, 7);
    std::cout << "3 + 7 = " << sum << std::endl;

    std::cout << "5 的平方 = " << square(5) << std::endl;

    // 重载：编译器根据参数类型自动选
    std::cout << "max(3, 7) = "      << max(3, 7)      << std::endl;
    std::cout << "max(3.14, 2.71) = " << max(3.14, 2.71) << std::endl;

    // 默认参数：不传就用默认值
    greet();
    greet("Clawy");

    // 传值 vs 传引用
    int n = 10;
    by_value(n);
    std::cout << "after by_value:  " << n << std::endl;   // 还是 10

    by_reference(n);
    std::cout << "after by_reference: " << n << std::endl; // 变成 999

    return 0;
}
