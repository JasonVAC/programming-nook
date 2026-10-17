// ========== 02_guess 猜数字游戏（实战课） ==========
// 知识点：loop 循环 / match 模式匹配 / Result 错误处理 / rand 随机数
// 对照 C++：这就是"猜数字"综合项目（07_guess）的 Rust 版

use rand::RngExt;         // rand 0.10：random_range 在 RngExt trait 里（0.9 以前是 Rng）
use std::cmp::Ordering;     // 比较结果：Less / Greater / Equal
use std::io;                // 标准输入

fn main() {
    println!("🎮 猜数字游戏！");

    // rand 0.10 新 API：rand::rng()（旧版叫 thread_rng()）
    // random_range(1..=100)：生成 1~100（含两端）的随机数
    let secret = rand::rng().random_range(1..=100);

    // println!("(调试) 答案是 {secret}");   // 想偷看就取消注释

    // ---- 主循环：loop 是无限循环，break 退出 ----
    loop {
        println!("请输入你的猜测（1~100）：");

        // ---- 读输入：Result 登场 ----
        // 每次循环都新建一个 String（旧值会被覆盖，省内存）
        let mut guess = String::new();

        // read_line 返回 Result：Ok(读了多少字节) / Err(出错了)
        // 教学版用 .expect()（出错就 panic）；但 EOF（管道输入结束，Ok(0)）
        // 会导致空字符串 parse 失败 → continue → 无限空转！所以要处理：
        let bytes = match io::stdin().read_line(&mut guess) {
            Ok(n) => n,
            Err(_) => {
                println!("⚠️ 读取输入出错，退出。");
                break;
            }
        };
        if bytes == 0 {
            // EOF：没有更多输入了（比如管道/重定向结束），别再死循环
            println!("👋 没有更多输入，退出。答案是 {secret}。");
            break;
        }

        // ---- 字符串转数字：Result 的实战用法 ----
        // parse::<u32>() 返回 Result<u32, ParseIntError>
        // match 分支：Ok(数字) 就用；Err(错误) 就提示并 continue 下一轮
        // 注意：u32 自动拒绝负数，所以 "0" 也进不了游戏（1~100）
        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => {
                println!("❌ 那不是数字！再试一次。");
                continue;   // 跳过本轮，回到 loop 开头
            }
        };

        // ---- 比较：match 让三个分支一目了然 ----
        // cmp 需要借用 &guess，因为 compare 不拿走值
        match guess.cmp(&secret) {
            Ordering::Less => println!("📉 太小了！"),
            Ordering::Greater => println!("📈 太大了！"),
            Ordering::Equal => {
                println!("🎉 猜对了！答案是 {secret}。");
                break;      // 退出 loop
            }
        }
    }
}
