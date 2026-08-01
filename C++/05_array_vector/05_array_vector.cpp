#include <iostream>
#include <vector>   // vector 的头文件

int main() {
    // ==================== 数组（固定大小） ====================
    int arr[5] = {10, 20, 30, 40, 50};

    std::cout << "数组: ";
    for (int i = 0; i < 5; i++) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;

    // 越界访问（危险！不会报错）
    // arr[5] = 999;  // 编译能过，但运行时会出问题

    // ==================== vector（动态数组） ====================
    std::vector<int> v = {1, 2, 3, 4, 5};

    std::cout << "vector: ";
    for (size_t i = 0; i < v.size(); i++) {
        std::cout << v[i] << " ";
    }
    std::cout << std::endl;

    // 尾部添加
    v.push_back(6);
    v.push_back(7);

    std::cout << "添加后: ";
    for (size_t i = 0; i < v.size(); i++) {
        std::cout << v[i] << " ";
    }
    std::cout << std::endl;

    // 删除尾部
    v.pop_back();
    std::cout << "删除尾部后 size = " << v.size() << std::endl;

    // 遍历方式2：范围 for（C++11 起）
    std::cout << "范围 for: ";
    for (int x : v) {
        std::cout << x << " ";
    }
    std::cout << std::endl;

    // ==================== 字符串（本质是 vector<char>） ====================
    std::string s = "Hello";
    s += " Clawy";
    std::cout << "string: " << s << std::endl;
    std::cout << "字符串长度: " << s.size() << std::endl;

    // ==================== 二维 vector（矩阵） ====================
    std::vector<std::vector<int>> matrix = {
        {1, 2, 3},
        {4, 5, 6}
    };

    std::cout << "矩阵:" << std::endl;
    for (auto &row : matrix) {
        for (int x : row) {
            std::cout << x << " ";
        }
        std::cout << std::endl;
    }

    // ==================== size vs capacity ====================
    std::vector<int> vec;
    std::cout << "空 vector: size=" << vec.size()
              << " capacity=" << vec.capacity() << std::endl;

    vec.push_back(1);
    std::cout << "加1个:    size=" << vec.size()
              << " capacity=" << vec.capacity() << std::endl;

    vec.push_back(2);
    vec.push_back(2);
    vec.push_back(2);
    std::cout << "加满:     size=" << vec.size()
              << " capacity=" << vec.capacity() << std::endl;

    return 0;
}
