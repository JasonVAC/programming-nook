#include <iostream>
#include <string>
#include <vector>
#include <filesystem>
#include <fstream>

struct Task {
    std::string title;
    bool completed;
};

void showMenu() {
    std::cout << "=====TODO=====" << std::endl;
    std::cout << "1. Add Task" << std::endl;
    std::cout << "2. List Tasks" << std::endl;
    std::cout << "3. Complete Task" << std::endl;
    std::cout << "4. Delete Task" << std::endl;
    std::cout << "5. Quit" << std::endl;
    std::cout << "Choice: ";
}

void addTask(std::vector<Task>& tasks) {
    std::string title;
    std::cout << "Enter title: ";
    std::cin.ignore();
    std::getline(std::cin, title);
    tasks.push_back({title, false});
    std::cout << "Added!" << std::endl << std::endl;
}

void listTasks(const std::vector<Task>& tasks) {
    if (tasks.empty()) {
        std::cout << "No tasks" << std::endl << std::endl;
        return;
    }

    std::cout << "Tasks (" << tasks.size() << "):" << std::endl;
    for (size_t i = 0; i < tasks.size(); i++){
        std::cout << "  " << i + 1 << ". ";
        std::cout << (tasks[i].completed ? "[OKAY]" : "[]");
        std::cout << " " << tasks[i].title << std::endl;
    }
    std::cout << std::endl;
}

void completeTask(std::vector<Task>& tasks) {
    int index;
    std::cout << "Enter number: ";
    std::cin >> index;

    if (index < 1 || index > static_cast<int>(tasks.size())) {
        std::cout << "Invalid!" << std::endl << std::endl;
        return;
    }

    tasks[index - 1].completed = true;
    std::cout << "Completed!" << std::endl << std::endl;
}

void deleteTask(std::vector<Task>& tasks) {
    int index;
    std::cout << "Enter number: ";
    std::cin >> index;

    if (index < 1 || index > static_cast<int>(tasks.size())) {
        std::cout << "Invalid!" << std::endl << std::endl;
        return;
    }

    tasks.erase(tasks.begin() + index - 1);
    std::cout << "Deleted!" << std::endl << std::endl;
}

// Save to tasks.txt (status|title format)
void saveTasks(const std::vector<Task>& tasks) {
    std::ofstream file("tasks.txt");
    if (!file.is_open()) {
        std::cerr << "Error: cannot open tasks.txt!" << std::endl;
        return;
    }

    for (const auto& task : tasks) {
        file << (task.completed ? "1" : "0") << "|" << task.title << "\n";
    }

    file.close();
    std::cout << "Saved to tasks.txt" << std::endl;
}

// Load from tasks.txt on startup
void loadTasks(std::vector<Task>& tasks) {
    std::ifstream file("tasks.txt");
    if (!file.is_open()) return;

    tasks.clear();
    std::string line;

    while (std::getline(file, line)) {
        if (line.empty()) continue;

        size_t pos = line.find('|');
        if (pos == std::string::npos) {
            std::cerr << "Warning: invalid line, skipped: " << line << std::endl;
            continue;
        }

        std::string statusStr = line.substr(0, pos);
        std::string title = line.substr(pos + 1);
        bool completed = (statusStr == "1");
        
        tasks.push_back({title, completed});
    }

    file.close();
    std::cout << "Loaded " << tasks.size() << " tasks from tasks.txt" << std::endl;
}

int main() {
    std::vector<Task> tasks;
    int choice;

    loadTasks(tasks);

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
                saveTasks(tasks);
                std::cout << "Goodbye!" << std::endl;
                return 0;
            default:
                std::cout << "Invalid choice!" << std::endl << std::endl;
                break;
        }
    }

    return 0;
}
