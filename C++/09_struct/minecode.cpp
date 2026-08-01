#include <iostream>
#include <string>
#include <vector>

struct Num {
    double a;
    double b;
};

class BankAccount {
private:
    std::string owner;
    double balance;

public:
    BankAccount(const std::string& owner_name, double initial_balance)
        : owner(owner_name), balance(initial_balance) {}

    void deposit(double amount) {
        if (amount > 0) balance += amount;
    }

    double getBalance() const {
        return balance;
    }
};

int main() {
    // struct — 要先创建变量实例
    Num n;
    n.a = 10;
    n.b = 20;
    std::cout << "struct: \n" << n.a << std::endl << n.b << std::endl;

    // class — 同样创建实例
    BankAccount acc("Jason", 1000);
    acc.deposit(10);
    acc.deposit(20);
    std::cout << "class: " << std::endl << acc.getBalance() << std::endl;

    return 0;
}
