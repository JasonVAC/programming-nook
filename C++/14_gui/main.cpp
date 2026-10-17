// 14_gui - Qt6 图形界面入门
// Qt 的信号与槽 (Signal & Slot) 机制
// 编译: cd 14_gui && cmake -B build && cmake --build build && ./build/gui_app

#include <QApplication>
#include <QWidget>
#include <QPushButton>
#include <QLabel>
#include <QLineEdit>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QMessageBox>
#include <QFont>

int main(int argc, char *argv[]) {
    // === 每个 Qt 程序必须有且只有一个 QApplication ===
    QApplication app(argc, argv);
    app.setApplicationName("我的第一个 Qt 程序");

    // === 主窗口 ===
    QWidget window;
    window.setWindowTitle("🦀 Clawy 的 Qt 工具箱");
    window.resize(400, 300);

    // === 创建部件 (Widgets) ===
    auto* label = new QLabel("你好，C++ 世界！");
    label->setAlignment(Qt::AlignCenter);
    label->setStyleSheet("font-size: 18px; color: #333;");

    auto* button = new QPushButton("点我！");
    button->setStyleSheet(R"(
        QPushButton {
            font-size: 16px;
            padding: 8px 24px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3d8b40;
        }
    )");

    // === 输入框 + 发送按钮 ===
    auto* input = new QLineEdit();
    input->setPlaceholderText("输入你的名字...");
    input->setStyleSheet("font-size: 14px; padding: 6px;");

    auto* sendBtn = new QPushButton("打招呼");
    sendBtn->setStyleSheet(R"(
        QPushButton {
            font-size: 14px;
            padding: 6px 16px;
            background-color: #2196F3;
            color: white;
            border: none;
            border-radius: 4px;
        }
        QPushButton:hover { background-color: #1976D2; }
    )");

    auto* greetLabel = new QLabel();
    greetLabel->setAlignment(Qt::AlignCenter);
    greetLabel->setStyleSheet("font-size: 16px; color: #666;");

    // === 布局 (Layout) 把部件排列好 ===
    auto* inputLayout = new QHBoxLayout();
    inputLayout->addWidget(input, 1);  // 1 = 拉伸比例
    inputLayout->addWidget(sendBtn);

    auto* mainLayout = new QVBoxLayout();
    mainLayout->addStretch(2);
    mainLayout->addWidget(label);
    mainLayout->addWidget(button, 0, Qt::AlignCenter);
    mainLayout->addSpacing(20);
    mainLayout->addLayout(inputLayout);
    mainLayout->addWidget(greetLabel);
    mainLayout->addStretch(2);

    window.setLayout(mainLayout);

    // === 信号与槽 (Signal & Slot) ===
    // Qt 的核心机制：按钮点击 → 执行某个函数

    // "点我"按钮 → 改文字
    // connect(信号发送者, 信号, 信号接收者, 槽函数)
    // [](){} 是 C++ Lambda 表达式（匿名函数）
    QObject::connect(button, &QPushButton::clicked, [label]() {
        label->setText("🎉 你点了我！好痛！");
        label->setStyleSheet("font-size: 20px; color: #e91e63; font-weight: bold;");
    });

    // 第二个按钮 → 从输入框取文字显示
    QObject::connect(sendBtn, &QPushButton::clicked, [input, greetLabel]() {
        QString name = input->text().trimmed();
        if (name.isEmpty()) {
            greetLabel->setText("🤔 你还没输入名字呢！");
            greetLabel->setStyleSheet("font-size: 14px; color: #f44336;");
        } else {
            greetLabel->setText(QString("👋 你好，%1！欢迎来到 C++ 的世界！").arg(name));
            greetLabel->setStyleSheet("font-size: 16px; color: #4CAF50;");
        }
    });

    // 回车键也可以触发打招呼
    QObject::connect(input, &QLineEdit::returnPressed, sendBtn, &QPushButton::click);

    // === 显示窗口 ===
    window.show();

    // === 进入事件循环（程序一直跑，直到窗口关闭）===
    return app.exec();
}
