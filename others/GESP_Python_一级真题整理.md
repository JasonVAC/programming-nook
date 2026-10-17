# GESP Python 一级 · 历年真题整理

> **考试说明：** CCF 编程能力等级认证（GESP）Python 一级  
> 考试形式：选择题 + 判断题 + 编程题  
> 考试时间：90 分钟  
> 满分：100 分

---

## 📌 考点大纲

| 知识点 | 要求 |
|--------|------|
| Python 基本概念（程序、解释器、IDE） | 了解 |
| 变量与数据类型（int, float, str, bool） | 掌握 |
| 输入输出（`print()`、`input()`） | 掌握 |
| 运算符（算术、比较、逻辑） | 掌握 |
| 条件语句（`if` / `elif` / `else`） | 掌握 |
| 循环（`for`、`while`） | 掌握 |
| 列表（创建、索引、`append()`、`len()`） | 掌握 |
| 字符串（`len()`、拼接、索引） | 掌握 |
| `range()`、`in` 运算符 | 掌握 |
| 简单算法（求和、计数、找最大/最小） | 掌握 |

---

## 📝 选择题（每题 2 分）

### 考点：基本语法与数据类型

**1. 以下哪段代码能正确输出 `Hello, World!`？**

A. `print("Hello, World!")`  
B. `print(Hello, World!)`  
C. `printf("Hello, World!")`  
D. `echo("Hello, World!")`

<details>
<summary>答案</summary>
A
</details>

---

**2. Python 中，`type(3.14)` 的返回值是什么？**

A. `<class 'int'>`  
B. `<class 'float'>`  
C. `<class 'str'>`  
D. `<class 'number'>`

<details>
<summary>答案</summary>
B
</details>

---

**3. 以下哪个是合法的变量名？**

A. `2nd_place`  
B. `my-var`  
C. `_name`  
D. `class`

<details>
<summary>答案</summary>
C（变量名不能以数字开头，不能包含连字符，不能是关键字）
</details>

---

**4. `bool("False")` 的值是什么？**

A. `True`  
B. `False`  
C. 报错  
D. `None`

<details>
<summary>答案</summary>
A（非空字符串都是 True）
</details>

---

### 考点：运算符

**5. `17 // 5` 的结果是？**

A. 3.4  
B. 3  
C. 2  
D. 4

<details>
<summary>答案</summary>
B（`//` 是整除，向下取整）
</details>

---

**6. `17 % 5` 的结果是？**

A. 3  
B. 2  
C. 5  
D. 1

<details>
<summary>答案</summary>
B（`%` 是取余，17 ÷ 5 = 3 余 2）
</details>

---

**7. `2 ** 3 ** 2` 的结果是？**

A. 64  
B. 512  
C. 256  
D. 12

<details>
<summary>答案</summary>
B（`**` 是右结合，先算 `3 ** 2 = 9`，再算 `2 ** 9 = 512`）
</details>

---

**8. `not (3 > 5) and (4 == 4)` 的结果是？**

A. `True`  
B. `False`  
C. 报错  
D. `None`

<details>
<summary>答案</summary>
A（`not (3 > 5) → not False → True`；`4 == 4 → True`；`True and True → True`）
</details>

---

### 考点：条件语句

**9. 以下代码输出什么？**

```python
x = 10
if x > 5:
    print("A")
elif x > 8:
    print("B")
else:
    print("C")
```

A. A  
B. B  
C. C  
D. AB

<details>
<summary>答案</summary>
A（`x > 5` 为 True，执行后跳出，不会判断 elif）
</details>

---

**10. 以下代码输出什么？**

```python
score = 85
if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
elif score >= 70:
    print("中等")
else:
    print("加油")
```

A. 优秀  
B. 良好  
C. 中等  
D. 加油

<details>
<summary>答案</summary>
B
</details>

---

### 考点：循环

**11. 以下代码输出什么？**

```python
for i in range(3):
    print(i, end=" ")
```

A. `1 2 3`  
B. `0 1 2`  
C. `0 1 2 3`  
D. `1 2`

<details>
<summary>答案</summary>
B（`range(3)` 生成 0, 1, 2）
</details>

---

**12. 以下代码输出什么？**

```python
s = 0
for i in range(1, 6):
    s += i
print(s)
```

A. 10  
B. 15  
C. 21  
D. 6

<details>
<summary>答案</summary>
B（1+2+3+4+5 = 15）
</details>

---

**13. 以下 `while` 循环执行几次？**

```python
i = 1
while i < 10:
    i *= 2
```

A. 3 次  
B. 4 次  
C. 5 次  
D. 无限循环

<details>
<summary>答案</summary>
B（i 值变化：1→2→4→8→16，第 4 次后 i=16 ≥ 10 退出，循环体执行了 4 次）
</details>

---

### 考点：列表

**14. `len([10, 20, 30, 40])` 的结果是？**

A. 3  
B. 4  
C. 10  
D. 40

<details>
<summary>答案</summary>
B
</details>

---

**15. 以下代码输出什么？**

```python
a = [3, 1, 4, 1, 5]
a.append(9)
print(len(a))
```

A. 4  
B. 5  
C. 6  
D. 9

<details>
<summary>答案</summary>
C（原 5 个元素，append 后变成 6 个）
</details>

---

**16. `[1, 2, 3] + [4, 5]` 的结果是？**

A. `[5, 7, 3]`  
B. `[1, 2, 3, 4, 5]`  
C. `[1, 2, 3, [4, 5]]`  
D. 报错

<details>
<summary>答案</summary>
B（`+` 对列表做拼接）
</details>

---

### 考点：字符串

**17. `"Hello" + " " + "World"` 的结果是？**

A. `"Hello World"`  
B. `"HelloWorld"`  
C. `"Hello World "`  
D. 报错

<details>
<summary>答案</summary>
A
</details>

---

**18. `len("Hello\nWorld")` 的结果是？**

A. 10  
B. 11  
C. 12  
D. 13

<details>
<summary>答案</summary>
B（`\n` 是一个换行符，算 1 个字符；H e l l o 换行 W o r l d = 5+1+5 = 11）
</details>

---

## 🔘 判断题（每题 2 分）

**19. Python 中 `input()` 函数返回的是数值类型。**  
A. 正确  
B. 错误

<details>
<summary>答案</summary>
B（`input()` 始终返回字符串）
</details>

---

**20. `for i in range(5, 0, -1)` 可以生成序列 5, 4, 3, 2, 1。**  
A. 正确  
B. 错误

<details>
<summary>答案</summary>
A
</details>

---

**21. Python 中列表的元素可以是不同类型。**  
A. 正确  
B. 错误

<details>
<summary>答案</summary>
A
</details>

---

**22. `3 == "3"` 的结果是 `True`。**  
A. 正确  
B. 错误

<details>
<summary>答案</summary>
B（int 和 str 永远不相等）
</details>

---

**23. `break` 语句可以用于退出当前循环。**  
A. 正确  
B. 错误

<details>
<summary>答案</summary>
A
</details>

---

## 💻 编程题

### 题 1：输出问候（20 分）

**题目描述：**  
输入一个名字，输出 `"你好, [名字]!"`。

**输入格式：**  
一行，一个字符串，表示名字。

**输出格式：**  
一行，`"你好, [名字]!"`。

**样例输入：**
```
小明
```

**样例输出：**
```
你好, 小明!
```

<details>
<summary>参考代码</summary>

```python
name = input()
print("你好, " + name + "!")
```
</details>

---

### 题 2：判断奇偶数（20 分）

**题目描述：**  
输入一个整数，判断它是奇数还是偶数。如果是偶数输出 `even`，奇数输出 `odd`。

**输入格式：**  
一行，一个整数。

**输出格式：**  
一行，`even` 或 `odd`。

**样例：**

| 输入 | 输出 |
|------|------|
| 4 | even |
| 7 | odd |

<details>
<summary>参考代码</summary>

```python
n = int(input())
if n % 2 == 0:
    print("even")
else:
    print("odd")
```
</details>

---

### 题 3：求 1 到 N 的和（20 分）

**题目描述：**  
输入一个正整数 N，计算 1 + 2 + 3 + ... + N 的值。

**输入格式：**  
一行，一个正整数 N（1 ≤ N ≤ 1000）。

**输出格式：**  
一行，一个整数，表示和。

**样例：**

| 输入 | 输出 |
|------|------|
| 100 | 5050 |

<details>
<summary>参考代码</summary>

```python
n = int(input())
total = 0
for i in range(1, n + 1):
    total += i
print(total)
```
</details>

---

### 题 4：求最大值（20 分）

**题目描述：**  
输入三个整数，输出其中的最大值。

**输入格式：**  
一行，三个整数，用空格分隔。

**输出格式：**  
一行，一个整数，表示最大值。

**样例输入：**
```
3 7 5
```

**样例输出：**
```
7
```

<details>
<summary>参考代码</summary>

```python
a, b, c = map(int, input().split())
print(max(a, b, c))
```
</details>

---

### 题 5：统计字符个数（20 分）

**题目描述：**  
输入一个字符串，统计其中数字字符（'0'-'9'）的个数。

**输入格式：**  
一行，一个字符串（长度 ≤ 100）。

**输出格式：**  
一行，一个整数，表示数字字符的个数。

**样例输入：**
```
a1b2c3d4
```

**样例输出：**
```
4
```

<details>
<summary>参考代码</summary>

```python
s = input()
count = 0
for ch in s:
    if '0' <= ch <= '9':
        count += 1
print(count)
```
</details>

---

### 题 6：乘法表（20 分）

**题目描述：**  
输入一个正整数 N，输出 N 的乘法表（1 × N 到 N × N）。

**输入格式：**  
一行，一个正整数 N（1 ≤ N ≤ 9）。

**输出格式：**  
N 行，每行格式为 `i * N = i*N`。

**样例输入：**
```
3
```

**样例输出：**
```
1 * 3 = 3
2 * 3 = 6
3 * 3 = 9
```

<details>
<summary>参考代码</summary>

```python
n = int(input())
for i in range(1, n + 1):
    print(f"{i} * {n} = {i * n}")
```
</details>

---

### 题 7：倒序输出（20 分）

**题目描述：**  
输入一个正整数 N，然后输入 N 个整数，将它们倒序输出。

**输入格式：**  
第一行，一个正整数 N。  
第二行，N 个整数，用空格分隔。

**输出格式：**  
一行，倒序排列的 N 个整数，用空格分隔。

**样例输入：**
```
5
1 2 3 4 5
```

**样例输出：**
```
5 4 3 2 1
```

<details>
<summary>参考代码</summary>

```python
n = int(input())
nums = list(map(int, input().split()))
for i in range(n - 1, -1, -1):
    print(nums[i], end=" " if i > 0 else "")
```
</details>

---

## 📚 备考建议

1. **手写代码能力** — 考试是上机编程，平时要多自己敲，不要光看
2. **`input()` 返回的是字符串** — 要算数必须 `int()` 或 `float()` 转换
3. **`range()` 左闭右开** — `range(1, 5)` 只有 1, 2, 3, 4
4. **缩进就是一切** — Python 靠缩进识别代码块，4 个空格
5. **`//` 整除 vs `/` 除法** — `17 // 5 = 3`，`17 / 5 = 3.4`
6. **列表索引从 0 开始** — `a[0]` 是第一个元素
7. **字符串也能索引和遍历** — `s[0]` 取第一个字符，`for ch in s` 遍历
8. **`print()` 的 `end` 参数** — `print(x, end=" ")` 不换行，用空格结尾

---

## 🔗 参考链接

- GESP 官网：https://gesp.ccf.org.cn/
- CCF 官网：https://www.ccf.org.cn/
- Python 官方文档：https://docs.python.org/zh-cn/3/tutorial/
