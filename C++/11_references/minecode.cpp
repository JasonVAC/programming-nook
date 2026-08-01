// minecode - 引用练习：通讯录管理器
// 实现以下功能（建议逐条做，做一条跑一次）：

#include <iostream>
#include <string>
#include <vector>

struct Contact {
    std::string name;
    std::string phone;
    int age;
};

// ============================================
// 辅助函数：打印所有联系人（方便查看结果）
// ============================================
void printAllContacts(const std::vector<Contact>& contacts) {
    std::cout << "=== 通讯录 ===" << std::endl;
    for (const Contact& c : contacts) {
        std::cout << c.name << " | " << c.phone << " | " << c.age << "岁" << std::endl;
    }
    std::cout << std::endl;
}

// ============================================
// 你需要实现的函数
// ============================================

// 1. const & 参数：打印一个联系人（只读，不拷贝）
void printContact(const Contact& c) {
    std::cout << c.name << " | " << c.phone << " | " << c.age << "岁";
}

// 2. & 参数：修改联系人年龄（+1，过生日）
void birthday(Contact& c) {
    c.age++;
}

// 3. & 返回值 + & 参数：按名字查找联系人，返回引用
//    找到返回该联系人的引用，没找到返回 contacts 的最后一个
Contact& findContact(std::vector<Contact>& contacts, const std::string& name) {
    for (Contact& c : contacts) {
        if (c.name == name) {
            return c;
        }
    }
    return contacts.back();  // 没找到返回最后一个
}

// 4. 用 range for 给所有联系人年龄 +1
void everyoneBirthday(std::vector<Contact>& contacts) {
    for (Contact& c : contacts) {
        c.age++;
    }
}

// ============================================
// main 函数 — 写调用测试
// ============================================
int main() {
    std::vector<Contact> contacts = {
        {"Alice", "13800138000", 25},
        {"Bob",   "13900139000", 30},
        {"Charlie", "13700137000", 22},
    };

    // 1. 打印初始通讯录
    std::cout << "=== 初始通讯录 ===" << std::endl;
    printAllContacts(contacts);

    // 2. Alice 过生日
    std::cout << "=== Alice 过生日 ===" << std::endl;
    birthday(contacts[0]);  // Alice 年龄 +1
    printContact(contacts[0]);
    std::cout << std::endl << std::endl;

    // 3. 全员过生日
    std::cout << "=== 全员过生日 ===" << std::endl;
    everyoneBirthday(contacts);
    printAllContacts(contacts);

    // 4. 查找 Bob 并修改年龄
    std::cout << "=== 查找 Bob 并改年龄 ===" << std::endl;
    Contact& bob = findContact(contacts, "Bob");
    std::cout << "Bob 找到了！改成 99 岁" << std::endl;
    bob.age = 99;  // 通过引用修改
    printContact(bob);
    std::cout << std::endl;

    // 5. 查找不存在的联系人（测试返回最后一个）
    std::cout << "\n=== 查找不存在的联系人（返回最后一个） ===" << std::endl;
    Contact& last = findContact(contacts, "Nonexistent");
    std::cout << "返回了最后一个联系人: ";
    printContact(last);
    std::cout << std::endl;

    return 0;
}

//依旧joke
//int main() {
//
//    std::cout << "=== 通讯录 ===" << std::endl;
//    std::cout << "Alice  | 13800138000 | 25岁" << std::endl;
//    std::cout << "Bob    | 13900139000 | 30岁" << std::endl;
//    std::cout << "Charlie | 13700137000 | 22岁" << std::endl;
//    std::cout << std::endl;
//
//    std::cout << "=== Alice 过生日 ===" << std::endl;
//    std::cout << "Alice  | 13800138000 | 26岁" << std::endl;
//    std::cout << std::endl;
//
//    std::cout << "=== 全员过生日 ===" << std::endl;
//    std::cout << "Alice  | 13800138000 | 27岁" << std::endl;
//    std::cout << "Bob    | 13900139000 | 31岁" << std::endl;
//    std::cout << "Charlie | 13700137000 | 23岁" << std::endl;
//    std::cout << std::endl;
//
//    std::cout << "=== 查找 Bob 并改年龄 ===" << std::endl;
//    std::cout << "Bob 找到了！改成 99 岁" << std::endl;
//    std::cout << "Bob    | 13900139000 | 99岁" << std::endl;
//
//    return 0;
//}
