#include <QApplication>
#include <QWidget>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    QWidget window;
    window.setWindowTitle("Jason's Window");

    QLabel *label = new QLabel("请输入你的名字");
    QLineEdit *edit = new QLineEdit();
    QPushButton *btn = new QPushButton("问候");
    QLabel *result = new QLabel();

    QVBoxLayout *layout = new QVBoxLayout(&window);
    layout->addWidget(label);
    layout->addWidget(edit);
    layout->addWidget(btn);
    layout->addWidget(result);
    window.setLayout(layout);

    // 连接1：点击按钮 → 读取输入并显示问候
    QObject::connect(btn, &QPushButton::clicked, [edit, result]() {
        QString name = edit->text().trimmed();
        if (name.isEmpty())
            result->setText("名字不能为空！");
        else
            result->setText("你好，" + name + "！");
    });

    // 连接2：输入框回车 → 模拟按钮点击（复用上述逻辑）
    QObject::connect(edit, &QLineEdit::returnPressed, btn, &QPushButton::click);

    window.show();
    return app.exec();
}
