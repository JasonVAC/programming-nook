// ========== 所有权（Ownership）演示 ==========

fn main() {
    // ===== 1. 移动（Move）：一个值只有一个主人 =====
    let s1 = String::from("hello");
    let s2 = s1;              // 所有权从 s1 "移动" 给 s2（不是复制！）
    println!("{s2}");
    // println!("{s1}");      // ❌ 试试取消注释：s1 已被移动，编译错误！

    // ===== 2. Copy 类型：整数/bool/char/浮点 =====
    let a = 42;
    let b = a;                // ✅ 这些是 Copy 类型，真复制一份
    println!("a = {a}, b = {b}");  // 两个都能用

    // ===== 3. 借用（Borrowing）：& 只读借用 =====
    let s3 = String::from("rust");
    let len = calc_len(&s3);  // &s3 借出去，不转移所有权
    println!("{s3} 的长度是 {len}");  // s3 还能用 ✅

    // ===== 4. &mut 可变借用：独占 =====
    let mut s4 = String::from("你好");
    add_world(&mut s4);       // 可变借用
    println!("{s4}");

    // ===== 5. 作用域结束 = 自动释放（RAII 内置版）=====
    {
        let temp = String::from("临时数据");
        println!("{temp}");
    } // temp 在这里自动销毁，不需要 free/delete
}

// 参数是 &String（借用）——函数用完不会销毁它
fn calc_len(s: &String) -> usize {
    s.len()
}

// 参数是 &mut String（可变借用）——可以修改调用者的数据
fn add_world(s: &mut String) {
    s.push_str("，世界！");
}
