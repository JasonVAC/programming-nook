#include <iostream>

int main(){
    int a = 10;
    //if判断
    if (a == 10)
        printf("a == %d \n", a);
    //for循环
    for (int a =10; a < 15; a++)
        printf("for: %d\n", a);
    //while 循环
    a = 10;
    while (a < 20) {    
        printf("while: %d\n", a);
        a++;           
    }
}
