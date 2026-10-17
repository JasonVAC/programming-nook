// 13_fileio - 文件读写
// g++ -std=c++23 -Wall -Wextra 13_fileio.cpp -o 13_fileio

#include <iostream>
#include <fstream>   // 文件读写核心头文件
#include <filesystem>  // 文件系统操作（C++17）
#include <string>
#include <vector>

void separator(const std::string& title) {
    std::cout << "\n========== " << title << " ==========\n\n";
}

int main() {
    // ============================================
    // 1. 写文件 — ofstream
    // ============================================
    separator("写文件 (ofstream)");

    std::ofstream fout("test.txt");  // 打开文件准备写入（默认覆盖）

    if (!fout.is_open()) {           // 检查是否成功打开
        std::cerr << "❌ 无法打开文件写入！\n";
        return 1;
    }

    // 像操作 cout 一样写文件
    fout << "Hello, 文件!\n";
    fout << "这是第二行\n";
    fout << "Pi ≈ " << 3.14159 << "\n";

    fout.close();  // 关闭文件（不关也行，析构函数自动关）
    std::cout << "✅ 写入完成\n";

    // ============================================
    // 2. 读文件 — ifstream
    // ============================================
    separator("读文件 (ifstream)");

    std::ifstream fin("test.txt");

    if (!fin) {  // !fin 等价于 !fin.is_open()
        std::cerr << "❌ 无法打开文件读取！\n";
        return 1;
    }

    std::string line;
    while (std::getline(fin, line)) {  // 逐行读取
        std::cout << "📖 " << line << "\n";
    }

    fin.close();

    // ============================================
    // 3. 读单词 vs 读行
    // ============================================
    separator("读单词 vs 读行");

    std::ofstream("words.txt") << "apple banana cherry\n"
                               << "dog elephant fox\n";
    // ↑ 临时构造 ofstream 对象写文件

    std::ifstream finWord("words.txt");
    std::string word;

    // >> 运算符读单词（按空格/换行分隔）
    std::cout << "按单词读: ";
    while (finWord >> word) {
        std::cout << "[" << word << "] ";
    }
    std::cout << "\n";
    finWord.close();

    // ============================================
    // 4. 追加模式 (app)
    // ============================================
    separator("追加模式");

    std::ofstream fapp("log.txt", std::ios::app);  // 追加模式

    fapp << "[" << __TIME__ << "] 程序启动了\n";  // __TIME__ 是编译时间
    fapp << "[" << __TIME__ << "] 又写了一行日志\n";

    fapp.close();
    std::cout << "✅ 日志已追加\n";

    // 读出来看看
    std::ifstream flog("log.txt");
    std::cout << "--- log.txt ---\n";
    std::string logLine;
    while (std::getline(flog, logLine)) {
        std::cout << logLine << "\n";
    }
    std::cout << "---------------\n";

    // ============================================
    // 5. 检查文件状态
    // ============================================
    separator("文件状态检查");

    std::ifstream fcheck("不存在的文件.txt");

    std::cout << "打开结果:\n";
    std::cout << "  is_open(): " << fcheck.is_open() << "\n";   // false
    std::cout << "  fail():    " << fcheck.fail() << "\n";      // true
    // 也可以用 !fcheck 快速检查

    // 读取完后的状态
    std::ifstream fok("test.txt");
    std::string dummy;
    while (fok >> dummy) {}  // 读到结束

    std::cout << "\n读取完后:\n";
    std::cout << "  eof():  " << fok.eof() << "\n";   // true (到文件尾)
    std::cout << "  good(): " << fok.good() << "\n";  // false (因为eof了)
    std::cout << "  fail(): " << fok.fail() << "\n";  // true (因为eof)

    // 注意: eof() 是正常的文件结束，fail() 表示操作失败
    // 读完后通常 eof()=true, fail()=true, good()=false

    // ============================================
    // 6. 二进制文件读写
    // ============================================
    separator("二进制读写");

    struct Player {
        char name[32];
        int hp;
        int level;
    };

    Player hero{"勇士", 100, 1};

    // 写二进制
    std::ofstream fbin("player.bin", std::ios::binary);
    fbin.write(reinterpret_cast<const char*>(&hero), sizeof(hero));
    fbin.close();
    std::cout << "✅ 二进制写入: " << hero.name << "\n";

    // 读二进制
    Player loaded{};
    std::ifstream fbinIn("player.bin", std::ios::binary);
    fbinIn.read(reinterpret_cast<char*>(&loaded), sizeof(loaded));
    fbinIn.close();

    std::cout << "✅ 二进制读取: " << loaded.name
              << " | HP: " << loaded.hp
              << " | Lv." << loaded.level << "\n";

    // ============================================
    // 7. 综合示例：保存/读取任务列表
    // ============================================
    separator("综合：保存/读取任务");

    struct Task {
        std::string title;
        bool done;
    };

    // 写任务到文件
    std::vector<Task> todos = {
        {"学 C++", true},
        {"做项目", false},
        {"打游戏", false},
    };

    std::ofstream ftodo("todos.txt");
    for (const auto& t : todos) {
        ftodo << t.done << "|" << t.title << "\n";
        // 格式: 状态|标题
        // 1|学 C++
        // 0|做项目
    }
    ftodo.close();
    std::cout << "✅ 任务已保存\n";

    // 从文件读取任务
    std::vector<Task> loadedTodos;
    std::ifstream ftodoIn("todos.txt");
    std::string todoLine;

    while (std::getline(ftodoIn, todoLine)) {
        // 解析 "1|学 C++"
        size_t pipe = todoLine.find('|');
        if (pipe == std::string::npos) continue;

        bool done = (todoLine[0] == '1');
        std::string title = todoLine.substr(pipe + 1);

        loadedTodos.push_back({title, done});
    }
    ftodoIn.close();

    std::cout << "📋 读取到的任务:\n";
    for (size_t i = 0; i < loadedTodos.size(); ++i) {
        std::cout << "  " << i + 1 << ". "
                  << (loadedTodos[i].done ? "[✓]" : "[ ]")
                  << " " << loadedTodos[i].title << "\n";
    }

    // ============================================
    // 8. 一次性读入所有文本
    // ============================================
    separator("一次性读入");

    std::ofstream("poem.txt") << "床前明月光\n疑是地上霜\n";

    std::ifstream fpoem("poem.txt");
    // 把整个文件读到一个 string 里
    std::string content(
        (std::istreambuf_iterator<char>(fpoem)),
        std::istreambuf_iterator<char>()
    );
    fpoem.close();

    std::cout << "整个文件内容:\n" << content;

    // ============================================
    // 9. 实用技巧
    // ============================================
    separator("实用技巧");

    // 检查文件是否存在（不开文件）
    std::ifstream fcheckExist("test.txt");
    std::cout << "test.txt 存在? " << (fcheckExist.good() ? "是 ✅" : "否 ❌") << "\n";
    fcheckExist.close();

    // 获取文件大小
    std::ifstream fsize("test.txt", std::ios::ate | std::ios::binary);
    // ate = 打开后定位到文件尾
    std::streampos size = fsize.tellg();
    fsize.close();
    std::cout << "test.txt 大小: " << size << " 字节\n";

    // 删除文件 (C++17)
    if (std::filesystem::exists("test.txt")) {
        std::cout << "test.txt 存在，可以用 std::filesystem::remove 删除\n";
    }

    std::cout << "\n🔑 核心思路: 文件操作三步走\n";
    std::cout << "  1. 打开 (open / 构造函数)\n";
    std::cout << "  2. 读写 (<< / >> / getline / read / write)\n";
    std::cout << "  3. 关闭 (close / 析构函数自动关)\n";

    return 0;
}
