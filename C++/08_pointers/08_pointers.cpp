#include <iostream>

int main() {
    // ===== 1. 指针是什么？ =====
    // 变量存值，指针存地址

    int a = 42;
    int *p = &a;  // p 存了 a 的地址

    std::cout << "a 的值:   " << a     << std::endl;
    std::cout << "a 的地址: " << &a    << std::endl;
    std::cout << "p 的值:   " << p     << std::endl;  // 跟 &a 一样
    std::cout << "p 指向的值: " << *p  << std::endl;  // 42

    // 通过指针改值
    *p = 99;
    std::cout << "通过指针改后 a = " << a << std::endl;  // 99

    // ===== 2. 指针 vs 引用 =====
    int b = 10;
    int &ref = b;   // 引用：b 的别名
    int *ptr = &b;  // 指针：存 b 的地址

    ref = 20;       // 改引用的值 → b 变成 20
    *ptr = 30;      // 改指针指向的值 → b 变成 30

    // 引用不能改绑，指针可以改指
    int c = 50;
    ptr = &c;       // ✅ 指针改指 c
    // ref = c;     // ❌ 这不是改绑，是把 c 的值赋给 b

    // ===== 3. nullptr =====
    int *n = nullptr;  // 空指针，指向"没有"
    if (n == nullptr) {
        std::cout << "这是空指针，不能解引用！" << std::endl;
    }

    // ===== 4. 指针和数组 =====
    int arr[3] = {10, 20, 30};
    int *arr_ptr = arr;  // 数组名就是首元素地址

    std::cout << "arr[0] = " << *arr_ptr       << std::endl;  // 10
    std::cout << "arr[1] = " << *(arr_ptr + 1) << std::endl;  // 20
    std::cout << "arr[2] = " << *(arr_ptr + 2) << std::endl;  // 30

    // arr_ptr[2] 等价于 *(arr_ptr + 2)
    std::cout << "arr_ptr[2] = " << arr_ptr[2] << std::endl;  // 30

    // ===== 5. 指针做函数参数（改外面的变量） =====
    auto set_to_zero = [](int *x) {
        *x = 0;
    };

    int value = 999;
    set_to_zero(&value);  // 传地址
    std::cout << "after set_to_zero: " << value << std::endl;  // 0

    return 0;
}
