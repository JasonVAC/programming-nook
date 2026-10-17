# CSP-J 初赛全真模拟卷（C++）

> 时间：120 分钟 ｜ 满分：100 分
> 试题结构：一、单项选择题（30 分）　二、阅读程序（40 分）　三、完善程序（30 分）

---

## 一、单项选择题（共 15 题，每题 2 分，共 30 分）

**1.** 在计算机内部，统一使用 ____ 来表示数据和指令。
A) 十进制　　 B) 二进制　　C) 八进制　　D) 十六进制

**2.** 十进制数 27 转换为二进制数是？
A) 10011　　 B) 11011　　C) 11101　　D) 10101

**3.** C++ 中，以下哪种类型占用的字节数在不同编译器下通常是不确定的？
A) `char`　　 B) `short`　　C) `int`　　D) `long`

**4.** 若某程序的时间复杂度为 `O(n²)`，当 n 增大一倍时，其运行时间大约变为原来的 ____。
A) 2 倍　　 B) 1.5 倍　　C) 4 倍　　D) 不变

**5.** 以下代码的输出是？
```cpp
#include <iostream>
using namespace std;
int main() {
    int a = 6, b = 4;
    cout << (a ^ b) + (a & b) * 2 << endl;
    return 0;
}
```
A) 12　　 B) 10　　C) 8　　D) 14

**6.** 一棵深度为 3 的满二叉树，其节点总数是？（根节点深度为 1）
A) 6　　 B) 7　　C) 8　　D) 15

**7.** 对于含 n 个顶点的有向完全图，边的总数是？
A) n(n-1)/2　　 B) n(n-1)　　C) n²　　D) n²/2

**8.** 下列排序算法中，平均时间复杂度为 `O(n log n)` 且**不稳定**的是？
A) 归并排序　　 B) 冒泡排序　　C) 堆排序　　D) 直接插入排序

**9.** 关于队列，下列说法正确的是？
A) 先进后出（FILO）
B) 先进先出（FIFO）
C) 只能在队尾取元素
D) 是一种非线性结构

**10.** 将 5 个不同元素入栈，入栈顺序固定为 1,2,3,4,5，以下哪种**不可能**成为合法的出栈序列？
A) 2,1,3,5,4　　 B) 3,4,5,2,1　　C) 4,5,3,1,2　　D) 5,4,3,2,1

**11.** 以下代码的输出是？
```cpp
#include <iostream>
using namespace std;
int main() {
    string s = "NOIP2026";
    cout << s.substr(2, 3) + s[0] << endl;
    return 0;
}
```
A) IPN　　 B) IP2026N　　C) IP2N　　D) IPP

**12.** 若用邻接矩阵存储含 n 个顶点、m 条边的图，该矩阵的空间复杂度为？
A) O(n)　　 B) O(m)　　C) O(n+m)　　D) O(n²)

**13.** 以下哪个不是 C++ 中的合法标识符？
A) `_count`　　 B) `count2`　　C) `2count`　　D) `c_ount`

**14.** 对于递归实现的归并排序，递归调用时的额外空间复杂度为？
A) O(1)　　 B) O(n)　　C) O(log n)　　D) O(n log n)

**15.** `int a[10][10];` 数组中，`&a[2][3]` 与 `&a[0][0]` 之间相差多少个元素？
A) 13　　 B) 23　　C) 25　　D) 30

---

## 二、阅读程序（共 3 大题，共 40 分）

> 说明：判断题每空 1 分（正确填“√”，错误填“×”），选择题每题 2 分。

### 第 1 题（共 12 分）

```cpp
#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    int cnt = 0;
    for (int i = 1; i <= n; i++) {
        int x = i;
        while (x) {
            if (x % 10 == 0) cnt++;
            x /= 10;
        }
    }
    cout << cnt << endl;
    return 0;
}
```

- 判断题：
  1. 程序统计的是 `1~n` 中所有数字里数字 0 出现的总次数。（　　）
  2. 当 `n = 9` 时，输出为 `0`。（　　）
  3. 该程序的时间复杂度为 `O(n)`。（　　）

- 选择题：
  4. 当 `n = 100` 时，输出为？
     A) 11　　 B) 10　　C) 12　　D) 21
  5. 当 `n = 101` 时，比 `n = 100` 多出的次数是？
     A) 1　　 B) 2　　C) 3　　D) 0

### 第 2 题（共 14 分）

```cpp
#include <iostream>
using namespace std;
int f(int n) {
    if (n <= 1) return n;
    return f(n - 1) + f(n - 2);
}
int main() {
    int n;
    cin >> n;
    cout << f(n) << endl;
    return 0;
}
```

- 判断题：
  1. 当 `n = 0` 时，程序会输出 `0`。（　　）
  2. 若 `n` 很大（如 50），程序可能运行得非常慢。（　　）
  3. `f(6)` 与 `f(4) + f(5)` 结果相等。（　　）

- 选择题：
  4. 当 `n = 7` 时，输出为？
     A) 8　　 B) 13　　C) 21　　D) 34
  5. 计算 `f(n)` 的时间复杂度约为？
     A) O(n)　　 B) O(n²)　　C) O(2ⁿ)　　D) O(log n)
  6. 若用循环递推代替递归计算 `f(n)`，时间复杂度为？
     A) O(n)　　 B) O(2ⁿ)　　C) O(n²)　　D) O(1)

### 第 3 题（共 14 分）

```cpp
#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    int a[105];
    for (int i = 1; i <= n; i++) cin >> a[i];
    int mx = a[1], idx = 1;
    for (int i = 2; i <= n; i++) {
        if (a[i] > mx) {
            mx = a[i];
            idx = i;
        }
    }
    int mn = a[idx];
    for (int i = 1; i <= n; i++)
        if (a[i] < mn) mn = a[i];
    cout << mx - mn << endl;
    return 0;
}
```

- 判断题：
  1. 该程序求出数组中最大元素与最小元素的差值。（　　）
  2. 若数组中有多个相同的最大值，`idx` 指向第一个最大值位置。（　　）
  3. 程序对空数组（n = 0）也能正确工作。（　　）

- 选择题：
  4. 若输入 `3 1 5 2`（n=3, 数组 1 5 2），输出为？
     A) 4　　 B) 3　　C) 5　　D) 6
  5. 该程序的时间复杂度为？
     A) O(1)　　 B) O(log n)　　C) O(n)　　D) O(n²)
  6. 若所有元素都相等（如 5 个 7），输出为？
     A) 0　　 B) 7　　C) 35　　D) 不确定
  7. 下列代码功能与上面程序整体等价的是？
     A) 输出数组元素个数
     B) 输出最大元素
     C) 输出最小元素
     D) 输出最大与最小元素之差

---

## 三、完善程序（共 2 大题，共 30 分，每空 3 分）

### 第 1 题：二分查找（15 分）

下面程序在有序数组 `a[1..n]`（升序）中查找整数 `x`，返回其下标（若存在多个，返回任一位置；若不存在返回 -1）。请完善程序。

```cpp
#include <iostream>
using namespace std;
int main() {
    int n, x;
    cin >> n;
    int a[100005];
    for (int i = 1; i <= n; i++) cin >> a[i];
    cin >> x;
    int L = 1, R = n, ans = -1;
    while (____①____) {
        int mid = ____②____;
        if (a[mid] == x) {
            ans = mid;
            break;
        }
        if (____③____)
            L = mid + 1;
        else
            R = mid - 1;
    }
    cout << ans << endl;
    return 0;
}
```

1. ①处应填：____
   A) `L < R`　　B) `L <= R`　　C) `L != R`　　D) `L > R`

2. ②处应填：____
   A) `(L + R) / 2`　　B) `(L + R + 1) / 2`　　C) `L + (R - L) / 2`　　D) `(R - L) / 2`

3. ③处应填：____
   A) `a[mid] < x`　　B) `a[mid] > x`　　C) `a[mid] == x`　　D) `a[mid] <= x`

4. 若数组为 `1 3 5 7 9`，查找 `5`，则程序返回（下标从 1 开始）：____
   A) 1　　B) 2　　C) 3　　D) 4

5. 若查找 `6`（不存在），则程序返回：____
   A) -1　　B) 0　　C) 程序会死循环　　D) 不确定

### 第 2 题：求最大子段和（15 分）

给定 n 个整数（可能有负数），求一个连续子段，使该子段的和最大，输出这个最大和（若全为负数则输出最大的那个负数）。

```cpp
#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    int sum = 0, ans = ____①____;   // ans 初始化为一个很小的值
    for (int i = 1; i <= n; i++) {
        int x;
        cin >> x;
        if (sum < 0) sum = 0;         // 前一段和为负则丢弃
        sum = sum + x;
        if (____②____) ans = sum;
    }
    cout << ans << endl;
    return 0;
}
```

1. ①处应填：____
   A) `0`　　B) `-1e9`　　C) `n`　　D) `INT_MAX`

2. ②处应填：____
   A) `sum > ans`　　B) `sum < ans`　　C) `sum == ans`　　D) `sum != ans`

3. 若输入 `4` 和 `-2 1 -3 4`，输出为？
   A) 4　　B) 3　　C) 1　　D) -2

4. 若输入 `3` 和 `-5 -2 -9`，输出为？
   A) 0　　B) -2　　C) -5　　D) -16

5. 若输入 `5` 和 `2 -1 3 -1 2`，输出为？
   A) 4　　B) 5　　C) 6　　D) 7

---

## 📝 参考答案

<details>
<summary>点击查看答案</summary>

### 一、单项选择题
1. B　2. B　3. D　4. C　5. B　6. B　7. B　8. C　9. B　10. C　11. C　12. D　13. C　14. B　15. B

### 二、阅读程序
- 第 1 题：1.√　2.√　3.×　4.A　5.A
- 第 2 题：1.×　2.√　3.√　4.B　5.C　6.A
- 第 3 题：1.√　2.√　3.×　4.A　5.C　6.A　7.D

### 三、完善程序
- 第 1 题：1.B　2.C　3.A　4.C　5.A
- 第 2 题：1.B　2.A　3.A　4.B　5.B

</details>
