#include <iostream>
#include <vector>

int main(){
    //数组（普通）
    //int arr[10]; wrong
    //int arr[10] = {};            // ✅ 全 0
    int arr[10] = {10, 20, 30};
    std::cout << "arr: ";
    for (int i = 0; i < 10; i++) {
        std::cout << arr[i] << "\n";
    }
}
