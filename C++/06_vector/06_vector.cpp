#include <iostream>
#include <vector>

int main() {
    // ===== 创建 =====
    std::vector<int> v1;                    // 空 vector
    std::vector<int> v2(5);                 // 5 个 0
    std::vector<int> v3(5, 99);             // 5 个 99
    std::vector<int> v4 = {10, 20, 30};     // 列表初始化

    std::cout << "v2 (5个0):  ";
    for (int x : v2) std::cout << x << " ";
    std::cout << std::endl;

    std::cout << "v3 (5个99): ";
    for (int x : v3) std::cout << x << " ";
    std::cout << std::endl;

    std::cout << "v4:        ";
    for (int x : v4) std::cout << x << " ";
    std::cout << std::endl;

    // ===== 增删改 =====
    std::vector<int> v = {1, 2, 3};

    v.push_back(4);         // 尾部加
    v.push_back(5);         // 尾部再加
    v.pop_back();           // 删尾部（删掉 5）

    v.insert(v.begin() + 1, 99);  // 在第 1 个位置插入 99
    v.erase(v.begin() + 3);       // 删掉第 3 个位置的元素

    std::cout << "增删改后: ";
    for (int x : v) std::cout << x << " ";
    std::cout << std::endl;

    // ===== 访问 =====
    std::cout << "v[0] = "     << v[0]     << std::endl;  // 下标
    std::cout << "v.front() = " << v.front() << std::endl; // 第一个
    std::cout << "v.back() = "  << v.back()  << std::endl; // 最后一个

    // ===== 遍历的三种写法 =====
    std::cout << "遍历1 (下标): ";
    for (size_t i = 0; i < v.size(); i++)
        std::cout << v[i] << " ";

    std::cout << "\n遍历2 (范围 for): ";
    for (int x : v)
        std::cout << x << " ";

    std::cout << "\n遍历3 (引用修改): ";
    for (int &x : v) {   // 注意 &，这样才能改原数组
        x = x * 2;
        std::cout << x << " ";
    }

    std::cout << "\n修改后验证:  ";
    for (int x : v) std::cout << x << " ";

    std::cout << std::endl;

    // ===== size vs empty =====
    std::cout << "size = " << v.size() << std::endl;

    std::vector<int> empty_vec;
    std::cout << "空了吗？ " << (empty_vec.empty() ? "是" : "否") << std::endl;

    return 0;
}
