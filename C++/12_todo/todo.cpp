#include <iostream>
#include <string>
#include <vector>

struct Task {
    std::string title;
    bool completed;
};

//menu
void showMenu() {
    std::cout << "=====TODO=====" << std::endl;
    std::cout << "1. 添加任务" << std::endl;
    std::cout << "2. 列出任务" << std::endl;
    std::cout << "3. 完成任务" << std::endl;
    std::cout << "4. 删除任务" << std::endl;
    std::cout << "5. Quit" << std::endl;
    std::cout << "请选择：";
}

//add todo
void addTask(std::vector<Task>& tasks) {
    std::string title;
    std::cout << "请输入任务标题：";
    std::cin.ignore();
    std::getline(std::cin, title);
    tasks.push_back({title, false});
    std::cout << "已添加！" << std::endl << std::endl;
    
}

//listTasks
void listTasks(const std::vector<Task>& tasks) {
    if (tasks.empty()) {
        std::cout << "当前没有任务" << std::endl << std::endl;
        return;
    }

    std::cout << "当前任务（" << tasks.size() << "项）：" << std::endl;
    for (size_t i = 0; i < tasks.size(); i++){
        std::cout << "  " << i + 1 << ". ";
        if (tasks[i].completed) {
            std::cout << "[OKAY]";
        }else {
            std::cout << "[]";
        }
        std::cout << tasks[i].title << std::endl;
    }
}

// 完成任务
void completeTask(std::vector<Task>& tasks) {
    int index;
    std::cout << "输入编号: ";
    std::cin >> index;

    if (index < 1 || index > static_cast<int>(tasks.size())) {
        std::cout << "无效编号！" << std::endl << std::endl;
        return;
    }

    tasks[index - 1].completed = true;
    std::cout << "已完成！" << std::endl << std::endl;
}

// 删除任务
void deleteTask(std::vector<Task>& tasks) {
    int index;
    std::cout << "输入编号: ";
    std::cin >> index;

    if (index < 1 || index > static_cast<int>(tasks.size())) {
        std::cout << "无效编号！" << std::endl << std::endl;
        return;
    }

    tasks.erase(tasks.begin() + index - 1);
    std::cout << "已删除！" << std::endl << std::endl;
}

int main() {
    std::vector<Task> tasks;
    int choice;

    while (true) {
        showMenu();
        std::cin >> choice;
        std::cout << std::endl;

        switch (choice) {
            case 1:
                addTask(tasks);
                break;
            case 2:
                listTasks(tasks);
                break;
            case 3:
                completeTask(tasks);
                break;
            case 4:
                deleteTask(tasks);
                break;
            case 5:
                std::cout << "再见！" << std::endl;
                return 0;
            default:
                std::cout << "无效选择，请重新输入！" << std::endl << std::endl;
                break;
        }
    }

    return 0;
}
