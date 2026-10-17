// 16_review — 综合复习：学生成绩管理系统
// 综合运用：struct / vector / file I/O / stringstream / 排序

// 系统功能：
// 1. 从 CSV 文件读取学生成绩
// 2. 计算总分和平均分
// 3. 按总分排序
// 4. 输出成绩单
// 5. 查询单个学生成绩

// 数据文件格式 (grades.csv):
//   张三,85,92,78
//   李四,90,88,95
//   王五,78,85,80
//   赵六,95,97,93

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <iomanip>
#include <algorithm>

struct Student {
    std::string name;
    std::vector<int> scores;
    int total;
    double average;
};

// ============================================
// 你需要实现的函数（建议逐条实现测试）
// ============================================

// 1. [复习 stringstream + fileio] 从 CSV 文件读取学生数据
//    提示：先用 getline(file, line) 读行，再用 istringstream + getline(iss, token, ',') 拆分
std::vector<Student> loadStudents(const std::string& filename) {
    std::vector<Student> students;
    // ---- 你的代码：读文件，解析 CSV，计算 total 和 average ----
    std::ifstream fin(filename);
    if (!fin.is_open()) return students;

    std::string line;
    while (std::getline(fin, line)) {
        if (line.empty()) continue;
        std::istringstream iss(line);
        std::string token;
        Student s;
        s.total = 0;

        if (!std::getline(iss, token, ',')) continue;
        s.name = token;

        while (std::getline(iss, token, ',')) {
            int score = std::stoi(token);
            s.scores.push_back(score);
            s.total += score;
        }

        s.average = s.scores.empty() ? 0.0 : static_cast<double>(s.total) / s.scores.size();
        students.push_back(s);
    }
    fin.close();
    return students;
}

// 2. [复习 引用] 按引用修改学生成绩（添加一科新的成绩）
void addScore(Student& s, int newScore) {
    // ---- 你的代码 ----
    s.scores.push_back(newScore);
    s.total += newScore;
    s.average = static_cast<double>(s.total) / s.scores.size();
}

// 3. [复习 排序] 按总分降序排列学生
void sortByTotal(std::vector<Student>& students) {
    // 提示：std::sort + lambda 表达式
    // ---- 你的代码 ----
    std::sort(students.begin(), students.end(),
              [](const Student& a, const Student& b) {
                  return a.total > b.total;
              });
}

// 4. [复习 查找] 按姓名查找学生，返回索引。没找到返回 -1
int findStudent(const std::vector<Student>& students, const std::string& name) {
    // ---- 你的代码 ----
    for (std::size_t i = 0; i < students.size(); ++i) {
        if (students[i].name == name) return static_cast<int>(i);
    }
    return -1;
}

// 5. [复习 格式化输出] 打印单个学生成绩条
void printStudent(const Student& s) {
    // 格式： "张三   |  85  92  78  | 总分:255  | 均分:85.0"
    // ---- 你的代码 ----
    std::cout << std::left << std::setw(8) << s.name << " | ";
    for (int score : s.scores) {
        std::cout << " " << std::setw(3) << score << " ";
    }
    std::cout << " | 总分:" << s.total
              << "  | 均分:" << std::fixed << std::setprecision(1) << s.average;
}

// 6. [复习 遍历] 打印完整成绩单（表头 + 所有学生 + 每科平均分）
void printReport(const std::vector<Student>& students) {
    if (students.empty()) return;

    // ---- 找出最大科目数，以便动态生成表头 ----
    int max_subjects = 0;
    for (const auto& s : students) {
        if (static_cast<int>(s.scores.size()) > max_subjects)
            max_subjects = static_cast<int>(s.scores.size());
    }

    // 表头
    std::cout << std::left << std::setw(8) << "姓名" << " | ";
    for (int i = 0; i < max_subjects; ++i) {
        std::cout << " 科目" << i+1 << "  ";
    }
    std::cout << " | 总分 | 均分\n";
    std::cout << std::string(50 + (max_subjects - 3) * 6, '-') << "\n";
    // 注：基础长度50对应3科时的宽度，每多一科增加6个字符（空格+3位数字+空格）

    // ---- 你的代码：打印每个学生（适配不同科目数） ----
    for (const auto& s : students) {
        std::cout << std::left << std::setw(8) << s.name << " | ";
        for (int i = 0; i < max_subjects; ++i) {
            if (i < static_cast<int>(s.scores.size())) {
                std::cout << " " << std::setw(3) << s.scores[i] << " ";
            } else {
                std::cout << "      ";   // 占位6个空格（与正常列宽对齐）
            }
        }
        std::cout << " | 总分:" << s.total
                  << "  | 均分:" << std::fixed << std::setprecision(1) << s.average << "\n";
    }

    // ---- 你的代码：打印分隔线 ----
    std::cout << std::string(50 + (max_subjects - 3) * 6, '-') << "\n";

    // ---- 你的代码：计算并打印各科平均分（只统计有该科目的学生） ----
    std::vector<double> subjectAverages(max_subjects, 0.0);
    std::vector<int> subjectCounts(max_subjects, 0);
    for (const auto& s : students) {
        for (int i = 0; i < static_cast<int>(s.scores.size()); ++i) {
            subjectAverages[i] += s.scores[i];
            subjectCounts[i]++;
        }
    }
    for (int i = 0; i < max_subjects; ++i) {
        if (subjectCounts[i] > 0) {
            subjectAverages[i] /= subjectCounts[i];
        }
    }

    std::cout << std::left << std::setw(8) << "平均分" << " | ";
    for (int i = 0; i < max_subjects; ++i) {
        if (subjectCounts[i] > 0) {
            std::cout << std::setw(6) << std::fixed << std::setprecision(1)
                      << subjectAverages[i] << " ";
        } else {
            std::cout << "      ";   // 无数据时留空
        }
    }
    std::cout << "\n";
}

// ============================================
int main() {
    // 读取数据
    std::vector<Student> students = loadStudents("grades.csv");

    if (students.empty()) {
        std::cerr << "请先创建 grades.csv 文件！\n";
        std::cerr << "格式：姓名,成绩1,成绩2,...\n";
        return 1;
    }

    // 测试：添加新成绩
    std::cout << "为张三添加一门编程课成绩: 98\n";
    int idx = findStudent(students, "张三");
    if (idx != -1) addScore(students[idx], 98);

    // 测试：排序
    sortByTotal(students);

    // 测试：打印成绩单
    std::cout << "\n=== 成绩单（按总分降序）===\n\n";
    printReport(students);

    // 测试：查找单个学生
    std::cout << "\n=== 查找学生 ===\n";
    int found = findStudent(students, "张三");
    if (found != -1) {
        std::cout << "找到张三：\n";
        printStudent(students[found]);
        std::cout << "\n";
    }

    return 0;
}

// ===================== JOKE ====================
//int main() {
//    std::cout << "=== 学生成绩管理系统 v1.0 ===\n\n";
//    std::cout << "张三  | 85 92 78 98  | 总分:353  | 均分:88.2\n";
//    std::cout << "赵六  | 95 97 93     | 总分:285  | 均分:95.0\n";
//    std::cout << "李四  | 90 88 95     | 总分:273  | 均分:91.0\n";
//    std::cout << "王五  | 78 85 80     | 总分:243  | 均分:81.0\n";
//    std::cout << "-----------------------------\n";
//    std::cout << "均分  | 87.0 90.5 86.5 98.0\n";
//    return 0;
//}
