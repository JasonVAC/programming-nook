#include <iostream>

int main() {
    // ==================== if / else ====================
    int score = 85;

    if (score >= 90) {
        std::cout << "A" << std::endl;
    } else if (score >= 80) {
        std::cout << "B" << std::endl;  // ← 走这里
    } else {
        std::cout << "C" << std::endl;
    }

    // 三元运算符（一行版 if-else）
    int age = 20;
    std::string status = (age >= 18) ? "adult" : "minor";
    std::cout << status << std::endl;  // adult

    // ==================== for 循环 ====================
    std::cout << "for: ";
    for (int i = 0; i < 5; i++) {
        std::cout << i << " ";
    }
    std::cout << std::endl;

    // ==================== while 循环 ====================
    std::cout << "while: ";
    int n = 0;
    while (n < 5) {
        std::cout << n << " ";
        n++;
    }
    std::cout << std::endl;

    // ==================== do-while（至少执行一次） ====================
    std::cout << "do-while: ";
    int m = 0;
    do {
        std::cout << m << " ";
        m++;
    } while (m < 5);
    std::cout << std::endl;

    // ==================== break / continue ====================
    std::cout << "break/continue: ";
    for (int i = 0; i < 10; i++) {
        if (i == 3) continue;   // 跳过 3
        if (i == 7) break;       // 到 7 就停
        std::cout << i << " ";
    }
    std::cout << std::endl;

    return 0;
}
