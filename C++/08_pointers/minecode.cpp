#include <iostream>

int main(){
    int *p = nullptr;
    int a = 0;
    printf("%p\n", p);
    printf("%p\n", &a);

    p = &a;
    printf("%p\n", p);

    return 0;
    
}
