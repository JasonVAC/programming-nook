fn main() {
    // println! 是宏（macro），不是函数 —— 结尾的 ! 就是标志
    println!("Hello, world!");
    println!("你好，Rust！🦀");

    // Rust 变量默认不可变（immutable）—— 想改必须声明 mut
    let x = 5;          // 不可变绑定
    let mut y = 10;     // 可变绑定
    y += x;

    // {} 是占位符，类似 C 的 %d 但类型安全
    println!("x = {x}, y = {y}");

    // 数组越界在 Rust 里是受控错误，不是 C 的未定义行为
    let nums = [1, 2, 3];
    println!("nums[0] = {}", nums[0]);
}
