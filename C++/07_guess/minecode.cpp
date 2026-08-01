#include <iostream>
#include <vector>
#include <cstdlib>   // rand(), srand()
#include <ctime>

int random(int num){
    return rand() % num + 1;
}

int main(){
    srand(time(0));

    int NUM = 100;
    int guess = 0;
    int target = random(NUM);

    while(guess != target){
        std::cout << "enter a number:   (1 ~ " << NUM << ")" << std::endl;
        std::cin >> guess;
        if (guess == target) {
            std::cout << "猜对了!" << std::endl;
            break;
        } 
        else if (guess < target) {
            std::cout << "太小了" << std::endl;
            }
        else {
                std::cout << "太大了" << std::endl;
            }
    }
    
    printf("Goodbye!\n");

    return 0;
}
