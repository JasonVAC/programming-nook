# CSP-J 初赛模拟卷（第三套·C++）

> 时间：120 分钟 ｜ 满分：100 分
> 试题结构：一、单项选择题（30 分）　二、阅读程序（40 分）　三、完善程序（30 分）

---

## 一、单项选择题（共 15 题，每题 2 分，共 30 分）

**1.** 一个字节（byte）由多少位（bit）组成？
A) 4　　B) 8　　C) 16　　D) 32

**2.** 十进制数 45 转换为二进制数是？
A) 101101　　B) 110101　　C) 101011　　D) 111001

**3.** 表达式 `'A' + 1` 的类型是？
A) `char`　　B) `int`　　C) `string`　　D) `bool`

**4.** 以下哪个是 C++ 中合法的变量名？
A) `2sum`　　B) `int`　　C) `my_var`　　D) `a-b`

**5.** 以下代码的输出是？
```cpp
#include <iostream>
using namespace std;
int main() {
    int a = 7, b = 2;
    cout << a / b << " " << a % b << endl;
    return 0;
}
```
A) 3 1　　B) 3.5 1　　C) 3 0　　D) 4 1

**6.** 一棵深度为 4 的满二叉树（根节点深度为 1）共有多少个叶子节点？
A) 4　　B) 8　　C) 15　　D) 16

**7.** 对于含 n 个顶点的无向完全图，边的总数为？
A) n(n-1)/2　　B) n(n-1)　　C) n²　　D) n²/2

**8.** 下列排序算法中，最坏时间复杂度为 `O(n log n)` 的是？
A) 冒泡排序　　B) 快速排序　　C) 归并排序　　D) 直接插入排序

**9.** 关于栈和队列，下列说法正确的是？
A) 栈是先进先出，队列是先进后出
B) 栈是先进后出，队列是先进先出
C) 两者都是先进先出
D) 两者都是先进后出

**10.** 入栈顺序固定为 1, 2, 3, 4，以下哪种**不可能**成为合法的出栈序列？
A) 1, 2, 3, 4　　B) 4, 3, 2, 1　　C) 3, 1, 2, 4　　D) 2, 3, 4, 1

**11.** 以下代码的输出是？
```cpp
#include <iostream>
using namespace std;
int main() {
    string s = "ABCDEF";
    cout << s.substr(1, 2) + s[5] << endl;
    return 0;
}
```
A) BCF　　B) BCDF　　C) BCFE　　D) ABCF

**12.** 用邻接表存储含 n 个顶点、m 条边的无向图，其空间复杂度为？
A) O(n)　　B) O(m)　　C) O(n+m)　　D) O(n²)

**13.** 以下哪个不是 C++ 的循环控制语句？
A) `for`　　B) `while`　　C) `do-while`　　D) `repeat`

**14.** 递归求解斐波那契数列 `f(n)=f(n-1)+f(n-2)` 的时间复杂度约为？
A) O(n)　　B) O(n²)　　C) O(2ⁿ)　　D) O(log n)

**15.** 定义 `int a[10][10];`，`&a[3][2]` 与 `&a[0][0]` 之间相差多少个元素？
A) 30　　B) 32　　C) 23　　D) 34

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
            if (x % 10 == 1) cnt++;
            x /= 10;
        }
    }
    cout << cnt << endl;
    return 0;
}
```

- 判断题：
  1. 程序统计的是 `1~n` 中所有数字里数字 1 出现的总次数。（　　）
  2. 当 `n = 9` 时，输出为 `1`。（　　）
  3. 该程序的时间复杂度为 `O(n log n)`。（　　）

- 选择题：
  4. 当 `n = 20` 时，输出为？
     A) 11　　B) 12　　C) 13　　D) 21
  5. 当 `n = 100` 时，输出为？
     A) 20　　B) 21　　C) 19　　D) 22

### 第 2 题（共 14 分）

```cpp
#include <iostream>
using namespace std;
int gcd(int a, int b) {
    if (b == 0) return a;
    return gcd(b, a % b);
}
int main() {
    int a, b;
    cin >> a >> b;
    cout << gcd(a, b) << endl;
    return 0;
}
```

- 判断题：
  1. 该程序求的是 a 与 b 的最大公约数。（　　）
  2. 当 `a = b` 时，函数一定返回 `a`。（　　）
  3. 函数 `gcd` 是尾递归，可改写为循环。（　　）

- 选择题：
  4. 若输入 `12 18`，输出为？
     A) 2　　B) 3　　C) 6　　D) 36
  5. 若输入 `17 5`，输出为？
     A) 1　　B) 2　　C) 5　　D) 17
  6. 该算法的时间复杂度约为？
     A) O(a + b)　　B) O(log min(a,b))　　C) O(a × b)　　D) O(√a)

### 第 3 题（共 14 分）

```cpp
#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    int a[105];
    for (int i = 1; i <= n; i++) cin >> a[i];
    int ans = 0, cur = 0;
    for (int i = 1; i <= n; i++) {
        if (a[i] >= 0) cur++;
        else cur = 0;
        if (cur > ans) ans = cur;
    }
    cout << ans << endl;
    return 0;
}
```

- 判断题：
  1. 程序求的是数组中最长的连续非负元素个数。（　　）
  2. 若数组元素全为负数，输出为 `0`。（　　）
  3. 程序会修改数组 `a` 的内容。（　　）

- 选择题：
  4. 若输入 `5` 和 `1 -2 3 4 -1`，输出为？
     A) 1　　B) 2　　C) 3　　D) 5
  5. 若输入 `6` 和 `0 1 -1 2 3 4`，输出为？
     A) 2　　B) 3　　C) 4　　D) 6
  6. 该程序的时间复杂度为？
     A) O(1)　　B) O(log n)　　C) O(n)　　D) O(n²)
  7. 若把 `if (a[i] >= 0)` 改为 `if (a[i] > 0)`，则统计的是？
     A) 最长连续非负段长度
     B) 最长连续正数段长度
     C) 数组中正数的总个数
     D) 最大元素的值

---

## 三、完善程序（共 2 大题，共 30 分，每空 3 分）

### 第 1 题：判断回文串（15 分）

下面程序读入一个不含空格的字符串 `s`，判断它是否为回文串（正读反读相同），是输出 `YES`，否则输出 `NO`。请完善程序。

```cpp
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    cin >> s;
    int L = 0, R = ____①____;
    bool ok = true;
    while (L < R) {
        if (____②____) {
            ok = false;
            break;
        }
        ____③____;
    }
    cout << (ok ? "YES" : "NO") << endl;
    return 0;
}
```

1. ①处应填：____
   A) `s.length()`　　B) `s.length() - 1`　　C) `s.length() + 1`　　D) `0`

2. ②处应填：____
   A) `s[L] == s[R]`　　B) `s[L] != s[R]`　　C) `s[L] < s[R]`　　D) `L == R`

3. ③处应填：____
   A) `L++; R--;`　　B) `L--; R++;`　　C) `L++; R++;`　　D) `L--; R--;`

4. 若输入 `abcba`，输出为：____
   A) YES　　B) NO　　C) 程序出错　　D) 不确定

5. 若输入 `abcc`，输出为：____
   A) YES　　B) NO　　C) 程序死循环　　D) 不确定

### 第 2 题：判断素数（15 分）

输入一个正整数 n（n ≥ 2），判断 n 是否为素数，是输出 `YES`，否则输出 `NO`。请完善程序。

```cpp
#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    bool isPrime = ____①____;
    for (int i = 2; ____②____; i++) {
        if (____③____) {
            isPrime = false;
            break;
        }
    }
    cout << (isPrime ? "YES" : "NO") << endl;
    return 0;
}
```

1. ①处应填：____
   A) `true`　　B) `false`　　C) `0`　　D) `n`

2. ②处应填：____
   A) `i <= n`　　B) `i < n`　　C) `i * i <= n`　　D) `i * i < n`

3. ③处应填：____
   A) `n % i == 0`　　B) `n % i != 0`　　C) `i % n == 0`　　D) `n / i == 0`

4. 若输入 `97`，输出为：____
   A) YES　　B) NO　　C) 程序出错　　D) 不确定

5. 若输入 `91`（= 7 × 13），输出为：____
   A) YES　　B) NO　　C) 程序死循环　　D) 不确定

---

## 📝 参考答案

<details>
<summary>点击查看答案</summary>

### 一、单项选择题
1. B　2. A　3. B　4. C　5. A　6. B　7. A　8. C　9. B　10. C　11. A　12. C　13. D　14. C　15. B

### 二、阅读程序
- 第 1 题：1.√　2.√　3.√　4.B　5.B
- 第 2 题：1.√　2.√　3.√　4.C　5.A　6.B
- 第 3 题：1.√　2.√　3.×　4.B　5.B　6.C　7.B

### 三、完善程序
- 第 1 题：1.B　2.B　3.A　4.A　5.B
- 第 2 题：1.A　2.C　3.A　4.A　5.B

</details>
