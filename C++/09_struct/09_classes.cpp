// 09_classes - 结构体 & 类
// g++ -std=c++23 -Wall -Wextra 09_classes.cpp -o 09_classes

#include <iostream>
#include <string>
#include <vector>

// ============================================
// 1. struct — 把相关数据打包在一起
// ============================================
struct Point {
    double x;
    double y;
};

struct Student {
    std::string name;
    int age;
    double score;
};

// struct 也可以有成员函数 (C++ 特性)
struct Rectangle {
    double width;
    double height;

    // 成员函数：计算面积
    double area() const {
        return width * height;
    }

    // 成员函数：打印信息
    void print() const {
        std::cout << "矩形: " << width << " x " << height
                  << " = " << area() << "\n";
    }
};

// ============================================
// 2. class — 封装 (encapsulation)
// ============================================
// class 和 struct 的唯一区别：默认访问权限不同
// struct 默认 public，class 默认 private
class BankAccount {
private:  // 私有成员 — 外部不能直接访问
    std::string owner;
    double balance;

public:   // 公有接口
    // 构造函数 (constructor)
    BankAccount(const std::string& owner_name, double initial_balance)
        : owner(owner_name), balance(initial_balance) {
        std::cout << "🏦 " << owner << " 的账户已创建，余额: ¥"
                  << balance << "\n";
    }

    // 存款
    void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            std::cout << "💰 存入 ¥" << amount
                      << "，当前余额: ¥" << balance << "\n";
        }
    }

    // 取款（带检查）
    bool withdraw(double amount) {
        if (amount <= 0) {
            std::cout << "❌ 取款金额必须大于 0\n";
            return false;
        }
        if (amount > balance) {
            std::cout << "❌ 余额不足！当前: ¥" << balance
                      << "，想取: ¥" << amount << "\n";
            return false;
        }
        balance -= amount;
        std::cout << "💸 取出 ¥" << amount
                  << "，剩余: ¥" << balance << "\n";
        return true;
    }

    // 查询余额 (const 表示不修改成员变量)
    double getBalance() const {
        return balance;
    }

    // 查询户主
    std::string getOwner() const {
        return owner;
    }
};

// ============================================
// 3. 更实际的例子：游戏中的玩家类
// ============================================
class Player {
    std::string name;
    int health;
    int max_health;
    int level;
    int exp;

public:
    Player(const std::string& player_name)
        : name(player_name), health(100), max_health(100),
          level(1), exp(0) {
        std::cout << "⚔️ " << name << " 加入了游戏！\n";
    }

    void takeDamage(int damage) {
        health -= damage;
        if (health < 0) health = 0;
        std::cout << "💥 " << name << " 受到了 " << damage
                  << " 点伤害！剩余 HP: " << health << "/" << max_health << "\n";
    }

    void heal(int amount) {
        health += amount;
        if (health > max_health) health = max_health;
        std::cout << "❤️ " << name << " 恢复了 " << amount
                  << " HP，当前: " << health << "/" << max_health << "\n";
    }

    void gainExp(int amount) {
        exp += amount;
        std::cout << "✨ 获得 " << amount << " 经验值\n";

        while (exp >= level * 100) {
            exp -= level * 100;
            level++;
            max_health += 20;
            health = max_health;
            std::cout << "🎉 升级！当前等级: " << level
                      << "，最大 HP: " << max_health << "\n";
        }
    }

    void status() const {
        std::cout << "\n=== " << name << " 的状态 ===\n"
                  << "HP: " << health << "/" << max_health << "\n"
                  << "等级: " << level << "\n"
                  << "经验: " << exp << "/" << level * 100 << "\n"
                  << "==================\n\n";
    }
};


int main() {
    std::cout << "=== 结构体 (struct) ===\n\n";

    // Point 结构体
    Point p1{3.0, 4.0};
    std::cout << "Point(" << p1.x << ", " << p1.y << ")\n";

    // Student 结构体
    Student stu{"小明", 18, 95.5};
    std::cout << stu.name << "，"
              << stu.age << "岁，成绩: "
              << stu.score << "\n\n";

    // Rectangle 带成员函数
    Rectangle rect{5.0, 3.0};
    rect.print();

    std::cout << "\n=== 类 (class) ===\n\n";

    // BankAccount — 演示封装
    BankAccount acc("Jason", 1000.0);
    acc.deposit(500.0);
    acc.withdraw(200.0);
    acc.withdraw(2000.0);  // 余额不足

    std::cout << "\n💳 " << acc.getOwner()
              << " 的最终余额: ¥" << acc.getBalance() << "\n";

    std::cout << "\n=== 游戏玩家示例 ===\n\n";

    Player hero("勇士");
    hero.status();

    hero.takeDamage(30);
    hero.heal(10);
    hero.gainExp(150);
    hero.status();

    hero.gainExp(200);  // 再打点怪
    hero.status();

    return 0;
}
