#include <iostream>

  // 先声明：告诉编译器有这个东西
  int add(int x, int y);
  void greet(std::string name);
  double square(double x);

  int main() {
      std::cout << add(3, 7) << std::endl;
      greet("Clawy");
      std::cout << square(5) << std::endl;
      return 0;
  }

  // 再定义：具体实现写在 main 后面
  int add(int x, int y) {
      return x + y;
  }

  void greet(std::string name) {
      std::cout << "Hello, " << name << "!" << std::endl;
  }

  double square(double x) {
      return x * x;
  }
