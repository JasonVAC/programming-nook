// minecode - CSV 成绩统计器
// 综合运用：fstream / stringstream / string 操作 / vector

// grades.csv 格式（请先创建这个文件）：
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

struct Student {
    std::string name;
    std::vector<int> scores;
    int total;
    double average;
};

// ============================================
// 你需要实现的函数
// ============================================

// 1. 读 CSV 文件，返回 Student 数组
//    用 ifstream 逐行读取，用 istringstream + getline 按逗号拆分
//    第一项是姓名，后面的是各科成绩（数量不定）
//    计算 total 和 average 存进去
std::vector<Student> loadGrades(const std::string& filename) {
    std::vector<Student> students;
    std::ifstream file(filename);
    if (!file.is_open()) {
        return students;  // 返回空向量，主函数会判断
    }

    std::string line;
    while (std::getline(file, line)) {
        if (line.empty()) continue;

        std::istringstream iss(line);
        std::string token;
        Student s;
        s.total = 0;

        // 读取姓名
        if (!std::getline(iss, token, ',')) continue;
        s.name = token;

        // 循环读取各科成绩
        while (std::getline(iss, token, ',')) {
            int score = std::stoi(token);
            s.scores.push_back(score);
            s.total += score;
        }

        // 如果没读到成绩，跳过该行
        if (s.scores.empty()) continue;

        // 计算平均分
        s.average = static_cast<double>(s.total) / s.scores.size();
        students.push_back(s);
    }

    file.close();
    return students;
}

// 2. 打印个人成绩条
//    用 ostringstream 拼装："张三  |  85  92  78  | 总分:255  | 均分:85.0"
void printStudent(const Student& s) {
    // 姓名左对齐，宽度8
    std::cout << std::left << std::setw(8) << s.name << " | ";

    // 各科成绩，每个占4位（右对齐）
    for (size_t i = 0; i < s.scores.size(); ++i) {
        std::cout << std::right << std::setw(4) << s.scores[i];
        if (i != s.scores.size() - 1) std::cout << " ";  // 成绩间加空格
    }

    // 总分和平均分
    std::cout << "  | " << std::setw(4) << s.total << " | "
              << std::fixed << std::setprecision(1) << std::setw(4) << s.average
              << std::endl;
}

// 3. 打印全班成绩单
//    表头 + 每人一行 + 每科平均分
void printReport(const std::vector<Student>& students) {
    if (students.empty()) {
        std::cout << "没有学生数据！" << std::endl;
        return;
    }

    int numSubjects = students[0].scores.size();

    // ---- 表头 ----
    std::cout << "  姓名   | 成绩          | 总分 | 均分" << std::endl;
    std::cout << " -------+--------------+------+------" << std::endl;

    // ---- 每个学生 ----
    for (const auto& s : students) {
        printStudent(s);
    }

    // ---- 分隔线 ----
    std::cout << " -------+--------------+------+------" << std::endl;

    // ---- 各科平均分 ----
    // 计算每科总分
    std::vector<double> subjectSums(numSubjects, 0.0);
    for (const auto& s : students) {
        for (int i = 0; i < numSubjects; ++i) {
            subjectSums[i] += s.scores[i];
        }
    }

    // 输出平均分行
    std::cout << std::left << std::setw(8) << "均分" << " | ";
    for (int i = 0; i < numSubjects; ++i) {
        double avg = subjectSums[i] / students.size();
        std::cout << std::right << std::fixed << std::setprecision(1)
                  << std::setw(4) << avg;
        if (i != numSubjects - 1) std::cout << " ";
    }
    std::cout << "  | " << std::setw(4) << "-" << " | " << std::setw(4) << "-"
              << std::endl;
}

// ============================================
int main() {
    std::vector<Student> students = loadGrades("grades.csv");

    if (students.empty()) {
        std::cerr << "请先创建 grades.csv！\n";
        std::cerr << "格式：姓名,语文,数学,英语\n";
        return 1;
    }
    std::cout << "共读取 " << students.size() << " 名学生\n\n";
    printReport(students);

    return 0;
}
