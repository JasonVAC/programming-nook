#include <iostream>

int main() {
    // ========== 基本类型 ==========

    int age = 25;                   // 整数
    double price = 19.99;           // 浮点数（双精度）
    float pi = 3.14f;               // 浮点数（单精度，注意 f 后缀）
    char grade = 'A';               // 单个字符，用单引号
    bool is_ok = true;              // 布尔值：true / false

    // ========== 输出 ==========
    std::cout << "age: "  << age   << std::endl;
    std::cout << "price: " << price << std::endl;
    std::cout << "pi: "    << pi    << std::endl;
    std::cout << "grade: " << grade << std::endl;
    std::cout << "is_ok: " << is_ok << std::endl;

    // ========== sizeof 看类型占多少字节 ==========
    std::cout << "int 占 "    << sizeof(int)    << " 字节" << std::endl;
    std::cout << "double 占 " << sizeof(double) << " 字节" << std::endl;

    // ========== auto：让编译器自己推断类型 ==========
    auto x = 42;
    auto y = 3.14;
    auto z = "hello";
    std::cout << "auto: " << x << " " << y << " " << z << std::endl;

    // ========== 修改变量 ==========
    int counter = 0;
    counter = counter + 1;
    counter += 5;
    counter++;
    std::cout << "counter: " << counter << std::endl;

    //=========== 输出最后结果 ============
    std::cout << age << std::endl << price << std::endl << pi << std::endl << grade <<std::endl;
    std::cout << is_ok << std::endl << x << " " << y << " " << z;

    return 0;
}
