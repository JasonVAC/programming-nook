#include <iostream>
#include <vector>
#include <cstdlib>   // rand(), srand()
#include <ctime>     // time()

int generate_number(int max) {
    return rand() % max + 1;
}

void print_history(const std::vector<int> &guesses) {
    std::cout << "你猜过的: ";
    for (int g : guesses)
        std::cout << g << " ";
    std::cout << std::endl;
}

int main() {
    srand(time(0));  // 随机种子

    const int MAX = 100;
    char play_again = 'y';

    while (play_again == 'y' || play_again == 'Y') {
        int target = generate_number(MAX);
        std::vector<int> guesses;
        int guess;
        int attempts = 0;

        std::cout << "\n===== 猜数字游戏！（1~" << MAX << "）=====" << std::endl;

        while (true) {
            std::cout << "输入你的猜测: ";
            std::cin >> guess;

            if (std::cin.fail()) {  // 输入不是数字
                std::cin.clear();
                std::cin.ignore(10000, '\n');
                std::cout << "请输入数字！" << std::endl;
                continue;
            }

            guesses.push_back(guess);
            attempts++;

            if (guess == target) {
                std::cout << "🎉 猜对了！共用了 " << attempts << " 次" << std::endl;
                print_history(guesses);
                break;
            } else if (guess < target) {
                std::cout << "太小了" << std::endl;
            } else {
                std::cout << "太大了" << std::endl;
            }
        }

        std::cout << "再来一局？(y/n): ";
        std::cin >> play_again;
    }

    std::cout << "再见！👋" << std::endl;
    return 0;
}
